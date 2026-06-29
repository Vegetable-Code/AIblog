# Blog - Vue + FastAPI 博客系统

一个完整的个人博客系统，包含前台展示和后台管理。

## 技术栈

| 层次 | 技术 |
|------|------|
| 前台 | Vue 3 + Vite + Tailwind CSS |
| 后台 | Vue 3 + Vite + Element Plus |
| 后端 | FastAPI + SQLAlchemy + MySQL |
| 认证 | JWT Token |

## 项目结构

├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据库模型
│   │   ├── schemas/  # Pydantic 模型
│   │   └── core/     # 配置、数据库、安全、依赖
│   ├── requirements.txt
│   └── init_user.py  # 初始化管理员脚本
├── frontend/         # Vue 3 前台
├── admin/            # Vue 3 后台管理
├── docker-compose.yml
└── README.md

## 快速开始

### 1. 启动 MySQL

编辑 backend/.env 文件，修改数据库连接信息：

DATABASE_URL=mysql+pymysql://root:password@localhost:3306/blog_db

也可使用 Docker 启动 MySQL：

docker-compose up mysql -d

### 2. 启动后端

cd backend
pip install -r requirements.txt
python init_user.py     # 初始化数据库和管理员账号
uvicorn app.main:app --reload --port 8000

API 文档: http://localhost:8000/docs

### 3. 启动前台

cd frontend
npm install
npm run dev

访问: http://localhost:3000

### 4. 启动后台

cd admin
npm install
npm run dev

访问: http://localhost:3001

## 登录信息

- 用户名: admin
- 密码: admin123

## API 路由

| 路径 | 描述 |
|------|------|
| GET  /api/v1/posts | 获取文章列表 |
| GET  /api/v1/posts/{slug} | 获取文章详情 |
| POST /api/v1/auth/login | 登录 |
| GET  /api/v1/categories | 获取分类列表 |
| GET  /api/v1/tags | 获取标签列表 |
| POST /api/v1/comments | 发表评论 |
