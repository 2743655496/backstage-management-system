#!/bin/bash

echo "=============================="
echo "🚀 开始部署 Docker（生产环境 HTTPS）"
echo "=============================="

echo "📌 停止旧容器..."
docker-compose down

echo "📌 开始构建镜像（无缓存）..."
docker-compose build --no-cache

echo "📌 启动服务..."
docker-compose up -d

echo "=============================="
echo "🎉 部署完成！"
echo "🌐 前端访问地址：https://yourdomain.com"
echo "=============================="
