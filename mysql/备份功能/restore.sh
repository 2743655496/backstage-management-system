#!/bin/bash

# ============================
# 企业级 MySQL 自动恢复脚本
# ============================

# === 配置区域 ===

# MySQL 容器名称（必须与 docker-compose.yml 一致）
MYSQL_CONTAINER="mysql"

# MySQL 登录信息（建议与 backup.sh 保持一致）
MYSQL_USER="root"
MYSQL_PASSWORD="111111"
MYSQL_DATABASE="backstage"

# 备份文件路径（你要恢复哪个备份就填哪个）
# 示例：/data/mysql_backup/backstage_2026-02-05_03-00-00.sql.gz
BACKUP_FILE="$1"

# 日志文件
LOGFILE="/data/mysql_backup/restore.log"

# ============================
# 1. 参数检查
# ============================
if [ -z "$BACKUP_FILE" ]; then
    echo "用法: ./restore.sh <备份文件路径>"
    echo "示例: ./restore.sh /data/mysql_backup/backstage_2026-02-05_03-00-00.sql.gz"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 找不到备份文件: $BACKUP_FILE"
    exit 1
fi

echo "[$(date)] === 开始恢复数据库 $MYSQL_DATABASE ===" >> $LOGFILE
echo "使用备份文件: $BACKUP_FILE" >> $LOGFILE


# ============================
# 2. 校验备份文件是否损坏
# ============================
gzip -t "$BACKUP_FILE"
if [ $? -ne 0 ]; then
    echo "[$(date)] ❌ 备份文件损坏，无法恢复" >> $LOGFILE
    exit 1
fi
echo "[$(date)] ✔ 备份文件校验成功" >> $LOGFILE


# ============================
# 3. 清空数据库（防止数据冲突）
# ============================
echo "[$(date)] ✔ 清空数据库 $MYSQL_DATABASE" >> $LOGFILE

docker exec -i $MYSQL_CONTAINER mysql \
  -u$MYSQL_USER -p$MYSQL_PASSWORD \
  -e "DROP DATABASE IF EXISTS $MYSQL_DATABASE; CREATE DATABASE $MYSQL_DATABASE;"


# ============================
# 4. 执行恢复
# ============================
echo "[$(date)] ✔ 开始导入 SQL..." >> $LOGFILE

gunzip < "$BACKUP_FILE" | docker exec -i $MYSQL_CONTAINER mysql \
  -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE

if [ $? -ne 0 ]; then
    echo "[$(date)] ❌ 数据恢复失败" >> $LOGFILE
    exit 1
fi

echo "[$(date)] ✔ 数据恢复成功" >> $LOGFILE
echo "[$(date)] === 恢复流程结束 ===" >> $LOGFILE

echo "🎉 数据库恢复成功！"
