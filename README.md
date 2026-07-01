# AIBlog - 个人博客系统

基于 Vue 3 + FastAPI 的全栈个人博客，支持 Markdown 写作、PDF 导入、AI 搜索、多语言国际化。

## 技术栈

| 层次 | 技术 |
|------|------|
| 前台 | Vue 3 + Vite + Tailwind CSS |
| 后台管理 | Vue 3 + Vite + Element Plus |
| 后端 | FastAPI + SQLAlchemy + MySQL |
| 认证 | JWT Token |
| 存储 | 本地文件系统 / S3 兼容对象存储（Cloudflare R2） |
| 部署 | Docker + Railway |

## 功能特性

- **Markdown 写作** — 支持标准的 Markdown 语法编辑文章
- **PDF 导入** — 上传 PDF 自动解析为图文并茂的文章，支持原文下载
- **AI 智能搜索** — 基于语义的全文搜索
- **图形验证码** — 防止机器人刷接口
- **多语言国际化** — 根据 IP 自动切换中/英文
- **主题切换** — 管理后台支持暗色/亮色模式
- **标签管理** — 编辑文章时可直接创建新标签
- **响应式设计** — 适配桌面和移动端

## 项目结构

```
blog/
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── api/           # API 路由（文章、分类、标签、评论、认证等）
│   │   ├── models/        # 数据库模型
│   │   ├── schemas/       # Pydantic 数据模型
│   │   └── core/          # 配置、数据库、安全、依赖、存储层
│   ├── requirements.txt
│   ├── init_user.py       # 初始化管理员脚本
│   └── migrate_to_s3.py   # 迁移本地文件到 S3 脚本
├── frontend/              # Vue 3 前台
├── admin/                 # Vue 3 后台管理
├── docker-compose.yml     # 本地 MySQL
├── Dockerfile             # Railway 部署
├── railway.json
└── README.md
```

## 快速开始

### 1. 启动 MySQL

编辑 `backend/.env` 修改数据库连接信息：

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/blog_db
```

也可使用 Docker 启动：

```bash
docker-compose up mysql -d
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python init_user.py     # 初始化数据库和管理员账号
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

### 3. 启动前台

```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000

### 4. 启动后台管理

```bash
cd admin
npm install
npm run dev
```

访问：http://localhost:3001/admin/

## 登录信息

- 用户名: `admin`
- 密码: `admin123`

## API 路由

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/posts | 获取文章列表 |
| GET | /api/v1/posts/{slug} | 获取文章详情 |
| POST | /api/v1/posts/import-pdf | 导入 PDF 生成文章 |
| POST | /api/v1/auth/login | 登录 |
| GET | /api/v1/categories | 获取分类列表 |
| GET | /api/v1/tags | 获取标签列表 |
| POST | /api/v1/comments | 发表评论 |
| POST | /api/v1/captcha/image | 获取图形验证码 |
| POST | /api/v1/email-code/send | 发送邮箱验证码 |
| GET | /api/v1/ai-search | AI 语义搜索 |

## 部署

项目已配置 Railway 部署，详见 `Dockerfile` 和 `railway.json`。

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `DATABASE_URL` | MySQL 连接字符串 | 是 |
| `SECRET_KEY` | JWT 密钥 | 是 |
| `SMTP_HOST` | SMTP 服务器地址 | 邮箱验证码 |
| `SMTP_USER` | SMTP 账号 | 邮箱验证码 |
| `SMTP_PASSWORD` | SMTP 授权码 | 邮箱验证码 |
| `UPLOAD_ROOT` | 本地文件上传目录 | 本地存储 |
| `S3_ENDPOINT` | S3 兼容服务地址 | 对象存储 |
| `S3_ACCESS_KEY_ID` | S3 Access Key | 对象存储 |
| `S3_SECRET_ACCESS_KEY` | S3 Secret Key | 对象存储 |
| `S3_BUCKET_NAME` | S3 存储桶名称 | 对象存储 |
| `S3_PUBLIC_URL` | S3 公开访问 URL | 对象存储 |
