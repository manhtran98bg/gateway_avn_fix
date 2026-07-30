# CONNECTION BASE CLASS EXPLAIN
## Abstract Method In Base Class
Base class provide general method for all protocol
| Method | Argument | Return | Description |
|-----|----|----|----|
| createConnection | - config (dict): Protocol configuration | bool: True if connect successful | Create connection with device |
| destroyConnection | None | None | Stop connection with device |
| readData | - config (dict): Protocol configuration and registers<br> - monitor_func (callable): return True if device want to monitor | Union[List[dict], None]: return list of register | Read data from device |
| writeData | - config (dict): Protocol configuration and registers<br> - write_data (List[dict]): List of registers and value of them<br> - monitor_func (callable): return True if device want to monitor | bool: True if write data success | Write data to device |

## Abstract Method In Base Ethernet Class
Base class provide general method for Ethernet protocol
| Method | Argument | Return | Description |
|-----|----|----|----|
| read | - start (int): start address<br> - length (int): number of registers to read<br> - config (dict): configuration | Union[List[int], None]: values of registers | Read registers of device |
| write | - start (int): start address<br> - data (List[int]): Data to write<br> - config (dict): configuration | return True if write to device | Write registers of device |

# SUPPORT DEVICE
## MODBUS TCP

## S7 SNAP

## Serial Connection