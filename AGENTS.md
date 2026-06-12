# AGENTS.md

## Project Overview

Chinese resource-sharing site (资源分享站) — three independent packages, no monorepo tooling:

| Package | Stack | Purpose |
|---------|-------|---------|
| `resource-api/` | Python 3.10+ / FastAPI / SQLite (aiosqlite) | Backend REST API |
| `resource-web/` | Vue 3 / Vite / TypeScript / Pinia / Axios | Public-facing SPA |
| `resource-admin/` | Vue 3 / Vite / TypeScript / Pinia / Axios / Element Plus / ECharts | Admin panel SPA |

## Commands

### Backend (from `resource-api/`)

```bash
# First-time setup
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Initialize database + seed admin user
python -m scripts.init_db
python -m scripts.seed_data

# Run dev server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Python scripts must be run as modules** (`python -m scripts.X`), not directly. The `sys.path` manipulation in each script depends on this.

### Frontends (from `resource-web/` or `resource-admin/`)

```bash
npm install
npm run dev      # Vite dev server with API proxy to localhost:8000
npm run build    # vue-tsc && vite build → dist/
```

There is **no test suite, linter, formatter, or typecheck command** configured in either frontend. `npm run build` includes `vue-tsc` as the only type verification.

### Deploy (Ubuntu server)

```bash
sudo bash deploy/install.sh
```

One-shot script: installs deps, builds frontends, copies to `/var/www/`, configures systemd + nginx. See `deploy/部署文档.md` for manual steps.

## Architecture

### API

- All routes prefixed `/api/v1/` (routers in `resource-api/app/routers/`)
- Response envelope: `{ code: 0, message: "...", data: ... }` — code 0 = success
- Paginated responses use `PaginatedResponse` wrapper with `items`, `total`, `page`, `page_size`
- JWT auth: `Authorization: Bearer <token>`. Two token storage keys: `access_token` (web), `admin_token` (admin)
- Custom exceptions: `AppException` hierarchy in `middleware/error_handler.py` — throw these, not raw HTTPError

### Database

- SQLite at `resource-api/data/app.db`, created automatically on first run
- WAL mode + foreign keys enabled
- Schema defined in `database.py` `init_db()` — not in SQL migration files
- Default categories seeded in `seed_default_categories()` (different set from `scripts/seed_data.py` — the latter's categories take precedence if DB is empty)

### Frontend Routing

- `resource-web/` serves from `/` — standard `createWebHistory()`
- `resource-admin/` serves from `/admin/` — `createWebHistory('/admin/')`. Admin routes like `/resources` are relative to this base.
- Both frontends proxy `/api` → `localhost:8000` in dev mode via Vite config

### File Uploads

- Uploaded files stored in `resource-api/uploads/`
- Nginx proxies `/uploads/` to the FastAPI backend
- Max upload size: 200MB (nginx `client_max_body_size`)

## Gotchas

- **No root `package.json`** — each frontend is an independent npm project. `npm install` must be run in each directory separately.
- **Database schema changes** go in `database.py` `init_db()`. There are no migrations. Column additions are done via `ALTER TABLE` with existence checks (see the `nickname` column addition).
- **`.gitignore`** ignores `.*/**`, `docs/**`, `openspec/**` — hidden directories are excluded from git.
- **Default admin credentials**: `admin` / `admin123`. Change `SECRET_KEY` env var in production.
- **Two different category seed lists**: `database.py:seed_default_categories()` (6 items) vs `scripts/seed_data.py` (6 items, different names). The runtime seeder in `database.py` runs on app start; the script seeder is for manual setup.
