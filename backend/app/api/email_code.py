import random, string, smtplib, time
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..core.config import settings

# In-memory store for email codes
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
    """Send verification code via SMTP."""
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_pass = settings.SMTP_PASSWORD
    from_email = settings.SMTP_FROM_EMAIL or smtp_user
    
    if not smtp_host or not smtp_user or not smtp_pass:
        # Dev mode: just print the code
        print(f"[DEV] Email verification code for {to_email}: {code}")
        return True
    
    subject = "博客注册验证码"
    body = f"""
    <div style="max-width:480px;margin:0 auto;padding:32px 24px;background:#0f172a;border-radius:16px;font-family:Arial,sans-serif;">
        <div style="text-align:center;margin-bottom:24px;">
            <div style="width:48px;height:48px;margin:0 auto;background:linear-gradient(135deg,#06b6d4,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:20px;">AI</div>
        </div>
        <h2 style="color:#e2e8f0;text-align:center;font-size:18px;margin-bottom:8px;">邮箱验证</h2>
        <p style="color:#94a3b8;text-align:center;font-size:14px;margin-bottom:24px;">您的注册验证码如下，5分钟内有效：</p>
        <div style="background:#1e293b;border-radius:12px;padding:20px;text-align:center;margin-bottom:24px;border:1px solid #334155;">
            <span style="font-size:36px;font-weight:bold;letter-spacing:8px;color:#06b6d4;font-family:monospace;">{code}</span>
        </div>
        <p style="color:#64748b;text-align:center;font-size:12px;">如果这不是您的操作，请忽略此邮件。</p>
    </div>
    """
    
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def _cleanup_expired():
    """Remove codes older than 5 minutes."""
    now = time.time()
    expired = [k for k, v in _email_code_store.items() if now - v["created_at"] > 300]
    for k in expired:
        _email_code_store.pop(k, None)


@router.post("/send")
def send_verification_code(req: SendCodeRequest):
    """Send email verification code."""
    from .captcha import verify_captcha
    
    # Verify captcha first
    if not verify_captcha(req.captcha_id, req.captcha_text):
        raise HTTPException(status_code=400, detail="图形验证码错误")
    
    _cleanup_expired()
    
    # Rate limit: 1 per minute per email
    existing = _email_code_store.get(req.email)
    if existing and time.time() - existing["created_at"] < 60:
        raise HTTPException(status_code=429, detail="请60秒后再获取验证码")
    
    code = _generate_code()
    _email_code_store[req.email] = {"code": code, "created_at": time.time()}
    
    sent = _send_email(req.email, code)
    if not sent:
        raise HTTPException(status_code=500, detail="验证码发送失败")
    
    return {"message": "验证码已发送"}


def verify_email_code(email: str, code: str) -> bool:
    """Verify email code (one-time use)."""
    stored = _email_code_store.pop(email, None)
    if stored is None:
        return False
    if time.time() - stored["created_at"] > 300:
        return False
    return stored["code"] == code
