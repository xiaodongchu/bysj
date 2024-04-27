import os
from shutil import rmtree
from loguru import logger
from starlette.templating import Jinja2Templates

path_now = str(os.path.dirname(os.path.abspath(__file__)))
if path_now[-1] != '/':
    path_now += '/'

temp_dir = path_now + 'temp/'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
log_dir = temp_dir + 'log/'
# 删除log
if os.path.exists(log_dir):
    rmtree(log_dir, ignore_errors=True)
os.makedirs(log_dir, exist_ok=True)
logger.add(
    log_dir + "log_{time}.log", level="INFO", encoding="utf-8", enqueue=True,  # 异步写入
    rotation="500 MB",  # 每个文件的大小
    retention="7 days"  # 保留7天
)
pdf_dir = temp_dir + 'pdf/'
if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

templates_dir_path = path_now + 'templates/'
template = Jinja2Templates(directory=templates_dir_path).get_template("pdf.html")


def save_temp_pdf(pdf_bytes: bytes, user_info: str):
    file_path = pdf_dir + user_info + '.pdf'
    with open(file_path, "wb") as file:
        file.write(pdf_bytes)
    return file_path
