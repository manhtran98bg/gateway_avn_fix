#!/bin/bash
#set up mariadb

# Install MariaDB
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip python3-venv gunicorn
python3 -m venv venv
if command -v mysql &> /dev/null; then
    echo "MariaDB service is enabled."
else
    # # Start and enable MariaDB service
    sudo apt install -y mariadb-server 
    echo "MariaDB service is setting up..."
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    sudo mysql -e "GRANT ALL ON *.* TO 'rostek'@'localhost' IDENTIFIED BY 'Y1je3aRUjxJ1976' WITH GRANT OPTION;"
fi

# # Get the directory of the Bash script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${SCRIPT_DIR}
venv_folder_name="venv"
if [ -d "$venv_folder_name" ]; then
    source venv/bin/activate
    pip3 install -r requirements.txt
    echo "Virtual environment '$venv_folder_name' found in the current directory."
else
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
fi
create_systemd_service() {
    service_file_content="[Unit]
Description=Run Setup Script

[Service]
Type=simple
ExecStart=/bin/bash -c ${SCRIPT_DIR}\"/run_app.sh\"
User=root
Group=root
Restart=always

[Install]
WantedBy=default.target
"

    echo "$service_file_content" | sudo tee /etc/systemd/system/rostek_gateway.service > /dev/null
    sudo systemctl daemon-reload
    sudo systemctl start rostek_gateway.service

    # Enable the service to start on boot
    sudo systemctl enable rostek_gateway.service

    echo "Systemd unit file created and service started."
}

if [ "$1" == "--setup_service" ]; then
    create_systemd_service
else
    echo "Not setting up systemd service. To setup, run: $0 --setup_service"
fi

echo "Finish setting up the environment"