#!/bin/bash
set -e

API_DIR="/var/www/resource-api"
DB_DIR="/data/laoma/db"

echo "=== 一键启动 resource-api ==="

# 1. Ensure db directory
mkdir -p "$DB_DIR"
chown -R www-data:www-data "$DB_DIR"

# 2. Ensure venv
if [ ! -f "$API_DIR/venv/bin/activate" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv "$API_DIR/venv"
fi

. "$API_DIR/venv/bin/activate"
pip install -r "$API_DIR/requirements.txt" -q

# 3. Init db if not exists
if [ ! -f "$DB_DIR/app.db" ]; then
    echo "初始化数据库..."
    cd "$API_DIR"
    python -m scripts.init_db
    python -m scripts.seed_data
fi

deactivate

# 4. Ensure uploads dir
mkdir -p "$API_DIR/uploads"
chown -R www-data:www-data "$API_DIR/uploads"

# 5. Start service
cp "$(dirname "$0")/resource-api.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable resource-api
systemctl restart resource-api

sleep 2

# 6. Status check
echo ""
echo "服务状态:"
systemctl status resource-api --no-pager -l | head -15

echo ""
echo "端口监听:"
ss -tlnp | grep 8000 || echo "  端口 8000 未监听，请检查日志"

echo ""
echo "=== 启动完成 ==="
echo "  查看日志: journalctl -u resource-api -f"
echo "  重启服务: systemctl restart resource-api"
echo "  停止服务: systemctl stop resource-api"
