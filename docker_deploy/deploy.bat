@echo off
title 后台管理系统 - Docker 一键部署
echo ============================================
echo      后端 + 前端 + Nginx 一键部署启动中
echo ============================================

REM 切换到脚本所在目录
cd /d %~dp0

echo [1/4] 清理旧容器、镜像和缓存...
docker-compose down --rmi local -v

echo [2/4] 清理悬空镜像...
docker image prune -f

echo [3/4] 开始构建镜像（无缓存）...
docker-compose build --no-cache

if %errorlevel% neq 0 (
    echo 构建失败，请检查错误信息！
    pause
    exit /b 1
)

echo [4/4] 启动服务...
docker-compose up -d

echo.
echo ============================================
echo 部署完成！
echo 前端访问地址：http://localhost
echo 如果配置了 HTTPS，请访问：https://yourdomain.com
echo ============================================
pause
