#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== 资源分享站一键部署 ==="
echo "项目目录: $PROJECT_DIR"

# 1. Install system dependencies
echo "[1/5] 安装系统依赖..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm nginx > /dev/null

# 2. Setup backend
echo "[2/5] 设置后端..."
cd "$PROJECT_DIR/resource-api"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
python -m scripts.init_db
python -m scripts.seed_data
deactivate

# 3. Build frontends
echo "[3/5] 构建PC用户前端..."
cd "$PROJECT_DIR/resource-web"
npm install --silent
npm run build

echo "[4/5] 构建后台管理端..."
cd "$PROJECT_DIR/resource-admin"
npm install --silent
npm run build

# 4. Deploy to web directories
echo "[5/5] 部署文件..."
mkdir -p /var/www/resource-web
mkdir -p /var/www/resource-admin
mkdir -p /var/www/resource-api

cp -r "$PROJECT_DIR/resource-web/dist/"* /var/www/resource-web/
cp -r "$PROJECT_DIR/resource-admin/dist/"* /var/www/resource-admin/
cp -r "$PROJECT_DIR/resource-api/"* /var/www/resource-api/

# Setup systemd
cp "$PROJECT_DIR/deploy/resource-api.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable resource-api
systemctl restart resource-api

# Setup nginx
cp "$PROJECT_DIR/deploy/nginx.conf" /etc/nginx/sites-available/resource-share
ln -sf /etc/nginx/sites-available/resource-share /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo ""
echo "=== 部署完成 ==="
echo "前端访问: http://服务器IP/"
echo "管理后台: http://服务器IP/admin/"
echo "管理员账号: admin / admin123"
echo ""
echo "管理命令:"
echo "  查看API日志: journalctl -u resource-api -f"
echo "  重启API: systemctl restart resource-api"
echo "  重启Nginx: systemctl restart nginx"
