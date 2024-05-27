#!/bin/bash
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-ntp true

sudo apt update
sudo apt upgrade
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# 安装MySQL
sudo apt install -y mysql-server
sudo systemctl start mysql.service
sudo systemctl enable mysql.service

# 安装Redis
sudo apt install -y redis-server redis-tools
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 安装Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# 设置字符集
sudo mysql -e "SET GLOBAL explicit_defaults_for_timestamp = 1;"
sudo mysql -e "SET GLOBAL character_set_server = 'utf8mb4';"
sudo mysql -e "CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';"

# 安装GTK
sudo apt install -y libgtk-3-dev

# 安装 Nginx
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
# 配置文件位于 /etc/nginx/nginx.conf

# 安装 Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
nvm install 18

# 终端复用
sudo apt install -y tmux