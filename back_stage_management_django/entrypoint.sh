#!/bin/bash
set -e

INIT_FLAG="/app/.initialized"

echo "Backend container starting..."

if [ ! -f "$INIT_FLAG" ]; then
    echo "Running initial setup..."

    echo "Waiting for MySQL..."
    python - <<EOF
import pymysql, os, time, sys

host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

max_wait = 300
interval = 2
elapsed = 0

while elapsed < max_wait:
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connect_timeout=2
        )
        conn.close()
        print("MySQL ready")
        sys.exit(0)
    except Exception:
        time.sleep(interval)
        elapsed += interval

print("MySQL not ready in time")
sys.exit(1)
EOF

    echo "Applying migrations..."
    python manage.py migrate

    echo "Importing SQL data..."
    python run_sql.py || true

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    touch "$INIT_FLAG"
else
    echo "Initialization already done. Skipping migrate & SQL import."
fi

echo "Starting Gunicorn..."
exec gunicorn back_stage_management_django.wsgi:application \
    -b 0.0.0.0:8000 \
    -w 4 \
    --timeout 120
