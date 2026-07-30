import logging, threading
from ..services import assignTask, BaseService
from app.dependencies.logger_manager import deleteOutdatedLogs
import os, shutil

@assignTask('delete_log_server', "Delete log process")
class DeleteLogService(BaseService):
    def _loop(self):
        try:
            while self.keep_run:
                system_info = f"\tSystem info:\nNumber of thread: {threading.active_count()}\n"
                
                data = os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()
                CPU_Pct=str(round(float(data),2))
                system_info += f"The CPU usage is: {CPU_Pct}\n"
                
                tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
                system_info += f"Used memory is: {used_m}\n"
                system_info += f"Free memory is: {free_m}\n"

                total, used, free = shutil.disk_usage("/")
                system_info += "Disk Total: %d MiB\n" % (total // (2**20))
                system_info += "Disk Used: %d MiB\n" % (used // (2**20))
                system_info += "Disk Free: %d MiB\n" % (free // (2**20))
                logging.info(system_info)
               
                deleteOutdatedLogs()
                self.wait(3600)
        except Exception as e:
            logging.error(e)