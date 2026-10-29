#!/bin/bash
# ============================================
# 后台管理系统 - Docker 一键部署（Linux 版）
# ============================================

# 设置脚本标题（Linux 下用 echo 代替 title）
echo "============================================"
echo "     后端 + 前端 + Nginx 一键部署启动中"
echo "============================================"

# 切换到脚本所在目录（Linux 方式）
cd "$(dirname "$0")" || exit 1

# 判断 docker-compose 命令（兼容 docker compose 插件）
if command -v docker-compose >/dev/null 2>&1; then
    DC="docker-compose"
elif docker compose version >/dev/null 2>&1; then
    DC="docker compose"
else
    echo "未检测到 docker-compose 或 docker compose，请先安装 Docker Compose！"
    exit 1
fi

echo "[1/4] 清理旧容器、镜像和缓存..."
$DC down --rmi local -v

echo "[2/4] 清理悬空镜像..."
docker image prune -f

# echo "[3/4] 开始构建镜像（无缓存）..."
# $DC build --no-cache

echo "[3/4] 开始构建镜像..."
$DC build

if [ $? -ne 0 ]; then
    echo "构建失败，请检查错误信息！"
    read -p "按回车键退出..."
    exit 1
fi

echo "[4/4] 启动服务..."
$DC up -d

echo ""
echo "============================================"
echo "部署完成！"
echo "前端访问地址：https://192.168.10.143/ (本地部分访问ip为你自己的，若是云部署则为你购买证书的域名)"
echo "============================================"
read -p "按回车键退出..."
