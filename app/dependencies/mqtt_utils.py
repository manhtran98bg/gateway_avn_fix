from typing import Union
from dataclasses import dataclass, field
from queue import Empty, Full

import threading
from collections import deque
from time import monotonic as time
from .type_define import MqttInternalTopic

class MqttQueue(object):
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._init()
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0
        self.block_normal_msg = False

    def block(self):
        #block sending message and clear current message
        self.block_normal_msg = True
        self.queue.clear()

    def unblock(self):
        #allow sending message put to queue
        self.block_normal_msg = False

    def task_done(self):
        with self.all_tasks_done:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished

    def join(self):
        with self.all_tasks_done:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()

    def qsize(self):
        with self.mutex:
            return self._qsize()

    def empty(self):
        with self.mutex:
            return not self._qsize()

    def full(self):
        with self.mutex:
            return 0 < self.maxsize <= self._qsize()

    def put(self, item: 'MqttTopic',block=True, timeout=None):
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    self.wait(timeout, Full)
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def wait(self, timeout: float, error: Union[Full, Empty]):
        end_time = time() + timeout
        while self._qsize() >= self.maxsize:
            remaining = end_time - time()
            if remaining <= 0.0:
                raise error
            self.not_full.wait(remaining)

    def sleep(self, timeout: float):
        with self.not_full:
            self.not_full.wait(timeout)

    def get(self, block=True, timeout=None)->'MqttTopic':
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                self.wait(timeout, Empty)
            item = self._get()
            self.not_full.notify()
            return item

    def put_nowait(self, item):
        return self.put(item, block=False)

    def get_nowait(self):
        return self.get(block=False)

    def _init(self):
        self.queue = deque()
        self.internal_queue = deque()

    def _qsize(self):
        return len(self.queue) + len(self.internal_queue)

    def _put(self, item: 'MqttTopic'):
        if item.internal:
            self.internal_queue.append(item)
        elif not self.block_normal_msg:
            self.queue.append(item)

    def _get(self):
        if len(self.internal_queue):
            return self.internal_queue.popleft()
        else:
            return self.queue.popleft()


@dataclass
class MqttTopic(object):
    topic: str
    data: Union[str, dict]
    internal: bool = False
    qos: int = 0
    send_queue: MqttQueue = field(default=MqttQueue())
    mutex: threading.Lock = field(default=threading.Lock())

    @classmethod
    def putToQueue(cls, topic: str, msg: Union[str, dict], qos: int = 0,internal: bool = False)->bool:
        with cls.mutex:
            if ((isinstance(topic, str) or isinstance(topic, MqttInternalTopic)) 
                and (isinstance(msg, str) or isinstance(msg, dict))):
                msg = cls(topic, msg, internal, qos)
                cls.send_queue.put(msg)
                return True
            else:
                return False
            
    @staticmethod
    def reconnectMqtt():
        return MqttTopic.putToQueue(MqttInternalTopic.UPDATE, "", internal=True)

    @staticmethod
    def subNewDevice(id: str):
        return MqttTopic.putToQueue(MqttInternalTopic.SUB, id, internal=True)
    
    @staticmethod
    def unsubDevice(id: str):
        return MqttTopic.putToQueue(MqttInternalTopic.UNSUB, id, internal=True)