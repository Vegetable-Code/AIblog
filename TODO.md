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
