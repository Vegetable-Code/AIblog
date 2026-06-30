import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


def send_via_resend(to_email: str, code: str) -> bool:
    api_key = settings.RESEND_API_KEY
    from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER or "noreply@example.com"

    if not api_key:
        logger.error("[RESEND] RESEND_API_KEY not set")
        return False

    payload = {
        "from": f"博客系统 <{from_email}>",
        "to": [to_email],
        "subject": "博客注册验证码",
        "html": "<p>您的验证码是: <b>" + code + "</b></p><p>5分钟内有效</p>",
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(RESEND_API_URL, json=payload, headers=headers)
            if resp.status_code in (200, 201):
                logger.info(f"[RESEND] Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"[RESEND] Failed: status={resp.status_code}, body={resp.text}")
                return False
    except Exception as e:
        logger.error(f"[RESEND] Exception: {e}")
        return False
