# 资源分享站

一个开箱即用的中文资源分享平台，支持资源发布、分类浏览、搜索、收藏、用户认证和管理后台。

**在线体验**: [https://erdelama.top](https://erdelama.top)

## 功能特性

- **资源管理** — 发布、浏览、搜索、收藏资源，支持分类筛选和热度排序
- **用户系统** — 注册/登录（JWT 双 Token）、图形验证码、密码修改
- **分享广场** — 推荐优质站点/工具，独立展示模块
- **管理后台** — 数据统计面板、资源审核、用户管理、分类管理、站点设置
- **文件上传** — 支持大文件上传（最大 200MB），Nginx 代理转发
- **轻量部署** — SQLite 数据库，无需额外依赖，一键部署脚本

## 技术栈

| 模块 | 技术 |
|------|------|
| **后端 API** | Python 3.10+ / FastAPI / SQLite (aiosqlite) / JWT |
| **用户前端** | Vue 3 / Vite / TypeScript / Pinia / Axios |
| **管理后台** | Vue 3 / Vite / TypeScript / Element Plus / ECharts |

## 项目结构

```
laoma/
├── resource-api/          # 后端 REST API（FastAPI）
│   ├── app/
│   │   ├── routers/       # 路由模块（auth, resources, admin, shares...）
│   │   ├── services/      # 业务逻辑层
│   │   ├── models/        # Pydantic 数据模型
│   │   ├── middleware/     # 错误处理中间件
│   │   ├── utils/         # 工具函数（JWT 依赖等）
│   │   └── database.py    # SQLite 初始化与连接管理
│   └── scripts/           # 数据库初始化、种子数据等脚本
├── resource-web/          # 用户前端（Vue 3 SPA）
├── resource-admin/        # 管理后台（Vue 3 SPA）
└── deploy/                # 部署脚本与 Nginx 配置
```

## 快速开始

### 环境要求

- Python >= 3.10
- Node.js >= 18.0
- npm >= 9.0

### 1. 启动后端

```bash
cd resource-api
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
python -m scripts.init_db
python -m scripts.seed_data
uvicorn app.main:app --reload --port 8000
```

### 2. 启动用户前端

```bash
cd resource-web
npm install
npm run dev
```

### 3. 启动管理后台

```bash
cd resource-admin
npm install
npm run dev
```

### 访问地址

| 项目 | 地址 |
|------|------|
| 用户前端 | http://localhost:5173 |
| 管理后台 | http://localhost:5174 |
| API 接口 | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |

默认管理员账号: `admin` / `admin123`

> Windows 用户也可以使用一键启动脚本: `.\deploy\start.ps1`

### 生产部署

```bash
sudo bash deploy/install.sh
```

一键完成：安装依赖、构建前端、配置 Nginx + Systemd。详见 [deploy/部署文档.md](deploy/部署文档.md)。

## API 概览

所有接口前缀 `/api/v1/`，响应格式:

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

| 模块 | 说明 |
|------|------|
| `/api/v1/auth` | 注册、登录、验证码、Token 刷新 |
| `/api/v1/resources` | 资源 CRUD、搜索、热门排行 |
| `/api/v1/categories` | 分类列表 |
| `/api/v1/favorites` | 收藏管理 |
| `/api/v1/shares` | 分享站点管理 |
| `/api/v1/admin` | 后台管理（需管理员权限） |

完整接口文档启动后访问 [http://localhost:8000/docs](http://localhost:8000/docs)。

## 交流群

欢迎扫码添加微信，拉你进项目交流群，一起讨论功能建议、Bug 反馈和使用心得。

> 请备注「资源分享站」

<div align="center">

![微信群二维码](docs/wechat-qrcode.png)

</div>

## 开源协议

MIT License
