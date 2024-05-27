cd /etc/nginx
sudo chmod 775 nginx.conf
sudo chmod 775 conf.d -R
sudo cp ~/bysj/azure_init/fastapi.conf conf.d/fastapi.conf
sudo chmod 777 conf.d/fastapi.conf
mkdir ~/pem
cd ~/pem/
sudo cp ~/bysj/azure_init/cloudflare.pem ~/pem/cloudflare.pem
sudo cp ~/bysj/azure_init/cloudflare-key.pem ~/pem/cloudflare-key.pem

sudo nginx -t # 检查配置文件是否正确
sudo systemctl restart nginx
