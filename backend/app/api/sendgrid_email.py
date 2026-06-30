import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"


def send_via_sendgrid(to_email: str, code: str) -> bool:
    """Send verification code via SendGrid Web API (HTTPS, works on Railway)."""
    api_key = settings.SENDGRID_API_KEY
    from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER or "noreply@example.com"

    if not api_key:
        logger.error("[SENDGRID] SENDGRID_API_KEY not set")
        return False

    subject = "博客注册验证码"
    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:Arial,'Microsoft YaHei',sans-serif;">
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:20px 0;">
<tr><td align="center">
<table role="presentation" width="480" cellpadding="0" cellspacing="0" style="max-width:480px;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
<tr><td style="padding:36px 32px 24px;">
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding-bottom:20px;">
<table role="presentation" cellpadding="0" cellspacing="0">
<tr><td align="center" width="40" height="40" style="width:40px;height:40px;background:#18181b;border-radius:8px;font-size:18px;font-weight:bold;color:#ffffff;">AI</td></tr>
</table>
</td></tr>
<tr><td align="center" style="padding-bottom:4px;"><h1 style="margin:0;font-size:22px;font-weight:600;color:#18181b;">邮箱验证</h1></td></tr>
<tr><td align="center" style="padding-bottom:24px;"><p style="margin:0;font-size:14px;color:#71717a;">您的注册验证码如下，5分钟内有效：</p></td></tr>
<tr><td align="center">
<table role="presentation" cellpadding="0" cellspacing="0" style="background:#fafafa;border-radius:8px;border:1px solid #e4e4e7;padding:16px 36px;">
<tr><td align="center" style="font-size:32px;font-weight:bold;letter-spacing:10px;color:#18181b;font-family:'Courier New',monospace;">{code}</td></tr>
</table>
</td></tr>
</table>
</td></tr>
<tr><td style="padding:0 32px 28px;"><p style="margin:0;font-size:12px;color:#a1a1aa;text-align:center;">如果这不是您的操作，请忽略此邮件。</p></td></tr>
</table>
</td></tr>
<tr><td align="center" style="padding-top:10px;"><p style="margin:0;font-size:11px;color:#a1a1aa;">来自博客系统</p></td></tr>
</table>
</body>
</html>"""

    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_content}],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(SENDGRID_API_URL, json=payload, headers=headers)
            if resp.status_code in (200, 201, 202):
                logger.info(f"[SENDGRID] Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"[SENDGRID] Failed: status={resp.status_code}, body={resp.text}")
                return False
    except Exception as e:
        logger.error(f"[SENDGRID] Exception: {e}")
        return False
