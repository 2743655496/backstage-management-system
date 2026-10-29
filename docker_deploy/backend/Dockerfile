FROM python:3.12-slim

WORKDIR /app

# 安装基础依赖 + MySQL 客户端
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖，如果无法下载请更换源地址
COPY requirements.txt .
#RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt #阿里云
RUN pip install gunicorn

# 复制 Django 项目
COPY . .

# 赋予脚本执行权限 
RUN chmod +x ./entrypoint.sh 

ENTRYPOINT ["./entrypoint.sh"]
