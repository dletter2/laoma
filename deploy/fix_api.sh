#!/bin/bash
set -e
echo "=== 修复 API 服务 ==="

# 1. 安装缺失依赖
echo "安装缺失依赖..."
cd /var/www/resource-api
source venv/bin/activate
pip install httpx Pillow -q
deactivate

# 2. 重启 API 服务
echo "重启 API 服务..."
systemctl restart resource-api
sleep 3

# 3. 检查状态
echo "API 服务状态:"
systemctl status resource-api --no-pager

echo ""
echo "端口监听:"
ss -tlnp | grep 8000

echo ""
echo "测试本地访问:"
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost/api/v1/auth/me || echo "API 访问失败"

echo ""
echo "=== 修复完成 ==="
