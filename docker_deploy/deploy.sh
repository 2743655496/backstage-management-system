#!/bin/bash

# ================================
#   后端 + 前端 + Nginx 一键部署
# ================================

# 彩色输出
GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

echo -e "${GREEN}============================================${RESET}"
echo -e "${GREEN}   后端 + 前端 + Nginx 一键部署启动中${RESET}"
echo -e "${GREEN}============================================${RESET}"

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查 docker-compose 是否存在
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误：未检测到 docker-compose，请先安装！${RESET}"
    exit 1
fi

echo -e "${YELLOW}[1/4] 清理旧容器、镜像和缓存...${RESET}"
docker-compose down --rmi local -v

echo -e "${YELLOW}[2/4] 清理悬空镜像...${RESET}"
docker image prune -f

echo -e "${YELLOW}[3/4] 开始构建镜像（无缓存）...${RESET}"
docker-compose build --no-cache
if [ $? -ne 0 ]; then
    echo -e "${RED}构建失败，请检查错误信息！${RESET}"
    exit 1
fi

echo -e "${YELLOW}[4/4] 启动服务...${RESET}"
docker-compose up -d

echo
echo -e "${GREEN}============================================${RESET}"
echo -e "${GREEN}部署完成！${RESET}"
echo -e "${GREEN}前端访问地址：http://localhost${RESET}"
echo -e "${GREEN}如果配置了 HTTPS，请访问：https://yourdomain.com${RESET}"
echo -e "${GREEN}============================================${RESET}"
