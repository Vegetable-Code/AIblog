import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


def send_via_resend(to_email: str, code: str) -> bool:
    api_key = settings.RESEND_API_KEY
    from_email = "onboarding@resend.dev"

    if not api_key:
        logger.error("[RESEND] RESEND_API_KEY not set")
        return False

    payload = {
        "from": f"\u535a\u5ba2\u7cfb\u7edf <{from_email}>",
        "to": [to_email],
        "subject": "\u535a\u5ba2\u6ce8\u518c\u9a8c\u8bc1\u7801",
        "html": "<p>\u60a8\u7684\u9a8c\u8bc1\u7801\u662f: <b>" + code + "</b></p><p>5\u5206\u949f\u5185\u6709\u6548</p>",
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
