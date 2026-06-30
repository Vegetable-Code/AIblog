import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_via_brevo(to_email: str, code: str) -> bool:
    api_key = settings.BREVO_API_KEY
    from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER or "noreply@example.com"

    if not api_key:
        logger.error("[BREVO] BREVO_API_KEY not set")
        return False

    html_body = "<p>\u60a8\u7684\u9a8c\u8bc1\u7801\u662f: <b>" + code + "</b></p><p>5\u5206\u949f\u5185\u6709\u6548</p>"

    payload = {
        "sender": {"email": from_email, "name": "\u535a\u5ba2\u7cfb\u7edf"},
        "to": [{"email": to_email}],
        "subject": "\u535a\u5ba2\u6ce8\u518c\u9a8c\u8bc1\u7801",
        "htmlContent": html_body,
    }

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(BREVO_API_URL, json=payload, headers=headers)
            if resp.status_code in (200, 201, 202):
                logger.info(f"[BREVO] Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"[BREVO] Failed: status={resp.status_code}, body={resp.text}")
                return False
    except Exception as e:
        logger.error(f"[BREVO] Exception: {e}")
        return False
