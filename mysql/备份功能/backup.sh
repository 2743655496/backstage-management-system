#!/bin/bash

# ============================
# 企业级 MySQL 自动备份脚本
# ============================

# ============================
# 企业级 MySQL 自动备份脚本 - 配置区域
# ============================

# 本地备份目录（必须是宿主机路径）
# 用于存放 .sql.gz 备份文件和日志
# 建议放在独立磁盘或大容量目录
BACKUP_DIR="/data/mysql_backup"

# MySQL 容器名称（docker ps 查看）
# 必须与 docker-compose.yml 中的 container_name 一致
MYSQL_CONTAINER="mysql"

# MySQL 登录信息（生产环境建议创建专用备份用户）
# MYSQL_USER：备份用户（root 或 backup_user）
# MYSQL_PASSWORD：对应密码
# MYSQL_DATABASE：要备份的数据库名称
MYSQL_USER="root"
MYSQL_PASSWORD="111111"
MYSQL_DATABASE="backstage"

# 备份服务器（可选，但强烈推荐）
# 如果你有第二台服务器用于异地备份，请填写以下信息
# REMOTE_USER：备份服务器的 SSH 用户
# REMOTE_HOST：备份服务器 IP
# REMOTE_DIR：备份服务器存放目录
# 如果不需要上传，请留空 REMOTE_HOST=""
REMOTE_USER="backup"
REMOTE_HOST="192.168.10.200"
REMOTE_DIR="/data/mysql_backup"

# 本地备份保留天数（建议 7～30 天）
# 超过天数的备份会自动删除
RETENTION_DAYS=7

# 自动生成备份文件名（无需修改）
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="${MYSQL_DATABASE}_${DATE}.sql.gz"

# 日志文件路径（记录备份、上传、清理等信息）
LOGFILE="$BACKUP_DIR/backup.log"

mkdir -p $BACKUP_DIR

echo "[$(date)] === 开始备份数据库 $MYSQL_DATABASE ===" >> $LOGFILE

# === 1. 执行备份（容器内 mysqldump） ===
docker exec $MYSQL_CONTAINER mysqldump \
  -u$MYSQL_USER -p$MYSQL_PASSWORD \
  --single-transaction --quick --routines --events $MYSQL_DATABASE \
  | gzip > $BACKUP_DIR/$FILENAME

if [ $? -ne 0 ]; then
    echo "[$(date)] ❌ 备份失败" >> $LOGFILE
    exit 1
fi

echo "[$(date)] ✔ 备份成功: $FILENAME" >> $LOGFILE


# === 2. 校验备份文件是否有效 ===
gzip -t $BACKUP_DIR/$FILENAME
if [ $? -ne 0 ]; then
    echo "[$(date)] ❌ 备份文件损坏: $FILENAME" >> $LOGFILE
    exit 1
fi

echo "[$(date)] ✔ 备份文件校验成功" >> $LOGFILE


# === 3. 上传到备份服务器（可选） ===
if [ -n "$REMOTE_HOST" ]; then
    scp $BACKUP_DIR/$FILENAME $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/
    if [ $? -eq 0 ]; then
        echo "[$(date)] ✔ 上传到备份服务器成功" >> $LOGFILE
    else
        echo "[$(date)] ❌ 上传到备份服务器失败" >> $LOGFILE
    fi
fi


# === 4. 自动清理过期备份 ===
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete
echo "[$(date)] ✔ 清理超过 $RETENTION_DAYS 天的备份文件" >> $LOGFILE

echo "[$(date)] === 备份流程结束 ===" >> $LOGFILE
