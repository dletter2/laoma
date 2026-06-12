#!/bin/sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== 资源分享站一键部署 ==="
echo "项目目录: $PROJECT_DIR"

# 1. Install system dependencies
echo "[1/5] 安装系统依赖..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv nodejs npm nginx

# Verify python3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "错误: python3 未安装或不在 PATH 中"
    echo "当前 PATH: $PATH"
    ls -la /usr/bin/python* 2>/dev/null || echo "/usr/bin/ 下无 python 文件"
    exit 1
fi
echo "Python 版本: $(python3 --version)"

# 2. Setup backend
echo "[2/5] 设置后端..."
cd "$PROJECT_DIR/resource-api"

# Remove broken venv if exists
if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    echo "检测到损坏的 venv 目录，正在删除..."
    rm -rf venv
fi

if [ ! -f "venv/bin/activate" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

set +e
. venv/bin/activate
set -e
pip install -r requirements.txt -q
python -m scripts.init_db
python -m scripts.seed_data
deactivate

# 3. Build frontends
echo "[3/5] 构建PC用户前端..."
cd "$PROJECT_DIR/resource-web"
npm install --silent
chmod +x node_modules/.bin/* 2>/dev/null || true
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build

echo "[4/5] 构建后台管理端..."
cd "$PROJECT_DIR/resource-admin"
npm install --silent
chmod +x node_modules/.bin/* 2>/dev/null || true
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build

# 4. Deploy to web directories
echo "[5/5] 部署文件..."
mkdir -p /var/www/resource-web
mkdir -p /var/www/resource-admin
mkdir -p /var/www/resource-api

cp -r "$PROJECT_DIR/resource-web/dist/"* /var/www/resource-web/
cp -r "$PROJECT_DIR/resource-admin/dist/"* /var/www/resource-admin/

# Copy API source (exclude venv, __pycache__, data, uploads)
mkdir -p /var/www/resource-api/uploads
# Preserve existing uploads
if [ -d /var/www/resource-api/uploads ] && [ "$(ls -A /var/www/resource-api/uploads 2>/dev/null)" ]; then
    cp -r /var/www/resource-api/uploads /tmp/_resource_api_uploads_backup
fi
cp -r "$PROJECT_DIR/resource-api/"* /var/www/resource-api/
rm -rf /var/www/resource-api/venv
rm -rf /var/www/resource-api/__pycache__
find /var/www/resource-api -name '*.pyc' -delete 2>/dev/null || true
# Restore uploads
if [ -d /tmp/_resource_api_uploads_backup ]; then
    cp -r /tmp/_resource_api_uploads_backup/* /var/www/resource-api/uploads/ 2>/dev/null || true
    rm -rf /tmp/_resource_api_uploads_backup
fi

# Create venv in deployed location (venv paths are not portable after copy)
echo "部署 Python 虚拟环境..."
python3 -m venv /var/www/resource-api/venv
set +e
. /var/www/resource-api/venv/bin/activate
set -e
pip install -r /var/www/resource-api/requirements.txt -q
deactivate

# Setup systemd
cp "$PROJECT_DIR/deploy/resource-api.service" /etc/systemd/system/

# Ensure directories exist and are writable by www-data
mkdir -p /data/laoma/db
mkdir -p /var/www/resource-api/uploads
chown -R www-data:www-data /data/laoma/db
chown -R www-data:www-data /var/www/resource-api/uploads

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
