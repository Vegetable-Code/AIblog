# Railway 部署待处理事项

## 🔧 Cloudflare R2 对象存储配置（解决图片随重部署丢失的问题）

代码已支持 S3 兼容的对象存储，需在 Railway 面板设置以下环境变量：

| 变量名 | 说明 |
|--------|------|
| `S3_ENDPOINT` | `https://<account-id>.r2.cloudflarestorage.com` |
| `S3_ACCESS_KEY_ID` | R2 API 令牌 Access Key |
| `S3_SECRET_ACCESS_KEY` | R2 API 令牌 Secret Key |
| `S3_BUCKET_NAME` | 存储桶名称，如 `aiblog-images` |
| `S3_PUBLIC_URL` | Bucket 公共访问 URL，如 `https://pub-xxxxx.r2.dev` |

### 配置步骤

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/) → R2 → 创建存储桶
2. 存储桶设置 → 开启公共访问，复制公共 URL
3. 我的个人资料 → API 令牌 → 创建令牌（R2 读+写权限）
4. Railway 项目 → Variables → 添加上表环境变量
5. 重新部署

## ✅ 已完成

- [x] PDF 导入功能（图片渲染 + 原文下载）
- [x] 管理后台主题切换（暗色/亮色）
- [x] 编辑文章时可直接创建标签
- [x] 国际化（IP 自动切换语言）
- [x] 图形验证码
- [ ] Cloudflare R2 对象存储配置

## 📦 AI 工具插件系统（待规划）

目标：训练好的模型可通过后台注册上线，前台自动适配，无需改代码。

**架构核心：**
- 后台新增“模型管理”模块：CRUD + 上传模型文件 + 配置输入输出 Schema
- 后端新增模型注册表数据库表 + 推理引擎（内置推理 / API 转发）
- 前台新增 /ai-tools 页面，根据 Schema 动态渲染表单和结果
- 支持模型上下线控制

**模型预处理（文本向量化）方案（供实现时确认）：**

方案一（推荐）：模型文件自包含。训练时把向量化器和模型打包成同一个 Pipeline（如 sklearn Pipeline 或 ONNX），上传单个文件，引擎直接 pipeline.predict()，内置完成向量化。

方案二：模型 + 向量化器分离。Schema 中指定预处理方式和向量化器文件路径，适用于同一向量化器配多个模型、或灵活替换的场景。

方案三：内置通用向量化器。引擎内置 sentence-transformers / jieba 等，Schema 中指定即可，通用性强但推理开销较大。

**举例说明：**
- 场景：人名 → 国家预测模型
- 输入 Schema：人名（text）+ 返回候选项数（number）
- 输出 Schema：国家/地区（list）+ 置信度（percentage）
- 后台配好 Schema + 上传模型文件后，前台自动渲染表单和结果页，无需改代码

**状态：** 待规划，确认方案后执行

