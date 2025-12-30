# TMS 控制台（Vue 3 + FastAPI）

本地运输/运单管理示例，前端 Vue 3 + TypeScript + Vite + Element Plus，后端 FastAPI + SQLite + SQLModel。

## 功能概览
- 运单 CRUD（创建/查询/更新/删除）
- 分页 + 每页条数切换，空数据展示
- 模态表单：运单号、状态、费用、起讫点、承运商、日期等字段
- 前端样式：Element Plus 组件，中文 UI，本地代理 `/api`
- 数据存储：SQLite，启动自动创建

## 前置条件
- Node.js 18+
- Python 3.11+

## 快速启动
1) 后端
```bash
cd backend
python -m venv .venv313 && .\.venv313\Scripts\Activate.ps1   # 可选
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2) 前端
```bash
cd frontend
npm install
npm run dev
```

> Vite 将 `/api` 代理到 `http://127.0.0.1:8000`，如改端口请同步更新 `vite.config.ts`。

## 批量造数（可选）
```bash
cd backend
.\.venv313\Scripts\Activate.ps1
python seed.py --count 100
```

## API 速览
- `GET /shipments` 列表（支持 `limit`/`offset`）
- `POST /shipments` 创建
- `GET /shipments/{id}` 查询
- `PUT /shipments/{id}` 更新
- `DELETE /shipments/{id}` 删除
- `GET /health` 健康检查

## 调试提示
- CORS 已全开放，便于本地联调。
- SQLite 位于 `backend/data.db`；若需重置，可删除文件后重启后端。
