# 若已配置自启动
# sudo systemctl daemon-reload
# sudo systemctl restart fastapi.service
# sudo systemctl status fastapi.service
# sudo systemctl stop fastapi.service
# sudo systemctl start fastapi.service



# 运行
cd ~/fast_api_pro/
tmux new -s app_session
python3 -m app
# 退出tmux: ctrl+b d
# 重新进入tmux: tmux attach -t app_session
# 删除tmux: tmux kill-session -t app_session

# 初始化数据库
# cd ~/fast_api_pro/
# python3 -m my_test.test_data
# 测试删除18648268144
# python3 -m user