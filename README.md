# SET UP MARIADB MANUAL (Outdated)
- Install mariadb: https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04
- Access mariadb by: 
```
sudo mysql
```
- create user after access:
```
GRANT ALL ON *.* TO 'rostek'@'localhost' IDENTIFIED BY 'Y1je3aRUjxJ1976' WITH GRANT OPTION;
```
- drop database
```
DROP DATABASE rostek_gateway;
```

# Steps to run program:
user root permission:
```
sudo su
```

- 'SETUP':
```
./run_setup.sh
```
- If want to create linux service:
```
./run_setup.sh --setup_service
#check status of service after run
sudo systemctl status rostek_gateway.service
```
- 'TEST':
```
./run_test.sh #--show (if you want to display in default browser)
```
- 'RUN':
```
./run_app.sh
```

# CONNECTION
## With protocol over ethernet: 
+ dir: app/internal/connection
+ If developer want to update or create new type of device, inheritance base class MonitorConnection
+ In new class, define 'config_required' and all abstract method in base class.
+ 'config_required': there are a list of configurations, that must to be provided by user and validate function for each configuration.
+ 'abstract method': there are 3 method need to define
+ After define all required list and method, indicate new protocol by function '@MonitorConnection.registerProtocol'
+ Import new protocol in f'{dir}/__init__.py'

## With protocol over serial port:
+ dir: app/internal/serial_com
+ Define function for reading data over serial port (and close port after use)
+ Provide name of protocol and list 'config_required' with validate function
+ Indicate function by @ComData.assignSerialProtocol
+ Import new protocol in f'{dir}/__init__.py'

# DEVICE
## How to create new device type:
+ dir: app/internal/device
+ If developer want to update or create new type of device, inheritance base class MonitorDevice
+ In new class, define 'device_configuration', 'register_required' and all abstract method in base class.
+ 'device_configuration': there are a list of configurations, that must to be provided by user and validate function for each configuration.
+ 'register_required': there are a list of register, that must to be provided by user. 
+ After define all required list and method, indicate new device type by function '@MonitorDevice.registerDevice'
+ Import new protocol in f'{dir}/__init__.py'

# SERVICE
## There is a list of process with start with app (They can be a loop thread or not)
+ dir: app/internal/services
+ define process and indicate by '@assignTask'
+ Import new process in f'{dir}/__init__.py'

# DATABASE
## ADD TABLE FOR NEW OPERATION OR DEVICE
+ dir: app/model/databases
+ import new table in f'{dir}/__init__.py'
+ if developer want to delete data on table when user call factory reset, add table to 'TABLE_LIST'

# API
## Add new api
+ dir: app/routers
+ import new api namespace in f'{dir}/__init__.py'
+ swagger: f'http://{host}:5500/' for example 'http://localhost:5500/'

# Step for merge code:
+ Rebase comment (group comment)
```
git rebase -i HEAD~n # n is number of comment must to rebase
```
+ Change commit message with meaning message
```
git commit --ament
```
+ Fetch from v4.1 cloud brach
```
git fetch origin v4.1
```
+ Rebase code in you branch with latest code in v4.1
```
git rebase develop
```
+ Fix conflict and continue: git rebase --continue. If want to pause rebase, git rebase --abort
```
git rebase --continue # or --abort
```
+ Push code to your cloud branch (using -f if conflict with cloud)
```
git push #(-f)
```
+ Create merge request

+ In case rebase and missing code, using 'reflog' for check git history in local
```
git reflog
```


```
terminal show result something like that:
2850dec (HEAD -> v4.1, origin/v4.1) HEAD@{0}: commit (amend): update README v1
349c621 HEAD@{1}: commit: update README v1
dd69227 HEAD@{2}: commit (amend): delete psuit lib
02d6d44 HEAD@{3}: commit: delete psuit lib                     #  <= want to back to this state
03f24c3 HEAD@{4}: commit: update device
bfd56d9 HEAD@{5}: commit: update device
```
+ for example, if you want to bach to delete psuit lib run: git reset --hard HEAD@{3}

# Todo
- [ ] Refactor current code: remove all code from `__init__.py`, all objects must be created in main.py and pass to other objects
- [ ] Re-organized code file to make sure relevant .py files are placed together in the same folder, with relevant nameming
- [ ] merge all config `.yaml` files to make each config is customer specific. Consider using something like https://pypi.org/project/commentjson/ to avoid writing a whole bunch of custom code for param loading
- [ ] Avoid to use the same `mutex` as variable name, change to `something_mutex` or `mutex_something` for better separation
- [ ] Add pre-commit