import random, string, smtplib, time
from email.mime.text import MIMEText
from email.utils import make_msgid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..core.config import settings

_email_code_store: dict[str, dict] = {}

router = APIRouter(prefix="/email-code", tags=["邮箱验证码"])


class SendCodeRequest(BaseModel):
    email: EmailStr
    captcha_id: str
    captcha_text: str


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str


def _generate_code(length=6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def _send_email(to_email: str, code: str) -> bool:
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_pass = settings.SMTP_PASSWORD
    from_email = settings.SMTP_FROM_EMAIL or smtp_user
    use_ssl = settings.SMTP_USE_SSL

    import os
    has_pass = 'SET' if smtp_pass else 'NOT SET'
    print(f"[DEBUG] SMTP_HOST={smtp_host} SMTP_PORT={smtp_port} SMTP_USER={smtp_user} SMTP_PASS={has_pass} USE_SSL={use_ssl}")

    if not smtp_host or not smtp_user or not smtp_pass:
        print(f"[DEV] Email verification code for {to_email}: {code}")
        return True

    subject = "博客注册验证码"
    body_template = '''<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:Arial,'Microsoft YaHei',sans-serif;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:20px 0;">
<tr><td align="center">
<table role="presentation" width="480" cellpadding="0" cellspacing="0" style="max-width:480px;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
<tr><td style="padding:36px 32px 24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding-bottom:20px;">
<table role="presentation" cellpadding="0" cellspacing="0">
<tr><td align="center" width="40" height="40" style="width:40px;height:40px;background:#18181b;border-radius:8px;font-size:18px;font-weight:bold;color:#ffffff;">AI</td></tr>
</table>
</td></tr>
<tr><td align="center" style="padding-bottom:4px;"><h1 style="margin:0;font-size:22px;font-weight:600;color:#18181b;">邮箱验证</h1></td></tr>
<tr><td align="center" style="padding-bottom:24px;"><p style="margin:0;font-size:14px;color:#71717a;">您的注册验证码如下，5分钟内有效：</p></td></tr>
<tr><td align="center">
<table role="presentation" cellpadding="0" cellspacing="0" style="background:#fafafa;border-radius:8px;border:1px solid #e4e4e7;padding:16px 36px;">
<tr><td align="center" style="font-size:32px;font-weight:bold;letter-spacing:10px;color:#18181b;font-family:'Courier New',monospace;">''' + '{code}' + '''</td></tr>
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
</html>'''

    msg = MIMEText(body_template.format(code=code), "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    domain = smtp_user.split("@")[-1] if "@" in smtp_user else "localhost"
    msg["Message-ID"] = make_msgid(domain=domain)
    msg["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

    try:
        print(f"[DEBUG] Connecting to {smtp_host}:{smtp_port} (SSL={use_ssl})...")
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                print(f"[DEBUG] SMTP SSL login successful, sending to {to_email}...")
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.set_debuglevel(1)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                print(f"[DEBUG] SMTP STARTTLS login successful, sending to {to_email}...")
                server.send_message(msg)
        print(f"[DEBUG] Email sent successfully to {to_email}!")
        return True
    except smtplib.SMTPRecipientsRefused as e:
        print(f"[ERROR] Recipient refused by SMTP server: {e}")
        return False
    except smtplib.SMTPSenderRefused as e:
        print(f"[ERROR] Sender refused by SMTP server: {e}")
        return False
    except smtplib.SMTPAuthenticationError:
        print(f"[ERROR] SMTP authentication failed. Check SMTP_USER and SMTP_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP error: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        import traceback
        traceback.print_exc()
        return False



def _cleanup_expired():
    now = time.time()
    expired = [k for k, v in _email_code_store.items() if now - v["created_at"] > 300]
    for k in expired:
        _email_code_store.pop(k, None)



@router.post("/send")
def send_verification_code(req: SendCodeRequest):
    from .captcha import verify_captcha

    if not verify_captcha(req.captcha_id, req.captcha_text):
        raise HTTPException(status_code=400, detail="\u56fe\u5f62\u9a8c\u8bc1\u7801\u9519\u8bef")

    _cleanup_expired()

    existing = _email_code_store.get(req.email)
    if existing and time.time() - existing["created_at"] < 60:
        raise HTTPException(status_code=429, detail="\u8bf760\u79d2\u540e\u518d\u83b7\u53d6\u9a8c\u8bc1\u7801")

    code = _generate_code()
    _email_code_store[req.email] = {"code": code, "created_at": time.time()}

    sent = _send_email(req.email, code)
    if not sent:
        raise HTTPException(status_code=500, detail="\u9a8c\u8bc1\u7801\u53d1\u9001\u5931\u8d25")

    return {"message": "\u9a8c\u8bc1\u7801\u5df2\u53d1\u9001"}


def verify_email_code(email: str, code: str) -> bool:
    stored = _email_code_store.pop(email, None)
    if stored is None:
        return False
    if time.time() - stored["created_at"] > 300:
        return False
    return stored["code"] == code

