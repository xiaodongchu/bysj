cp ~/bysj/fastApiProject/ ~/fast_api_pro/ -r
cd ~/fast_api_pro/

pip install -r requirements.txt

pytnon3 ./database/models.py

python3 -m my_test.test_data

# 安装字体
sudo cp ~/fast_api_pro/templates/fonts/ /usr/share/fonts/ -r
sudo fc-cache -f -v

# 设置自启脚本
sudo cp ~/bysj/azure_init/fastapi.service /etc/systemd/system/fastapi.service
sudo chmod 644 /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl start fastapi.service
sudo systemctl status fastapi.service