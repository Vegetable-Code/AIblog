# -*- coding: utf-8 -*-
import httpx
from fastapi import APIRouter, Request

router = APIRouter(prefix="/i18n", tags=["国际化"])

COUNTRY_TO_LOCALE = {
    "CN": "zh-CN", "TW": "zh-TW", "HK": "zh-TW",
    "JP": "ja-JP", "KR": "ko-KR",
    "US": "en-US", "GB": "en-US", "AU": "en-US",
    "CA": "en-US", "SG": "en-US",
    "DE": "de-DE", "FR": "fr-FR", "RU": "ru-RU",
    "BR": "pt-BR", "IN": "en-US",
}

_ip_cache = {}


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
        if ip and ip != "unknown":
            return ip
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    client = request.client
    if client:
        return client.host
    return "127.0.0.1"


async def _geoip_lookup(ip: str):
    if ip in ("127.0.0.1", "::1", "localhost") or ip.startswith(("10.", "172.16.", "192.168.", "100.")):
        return "zh-CN"
    if ip in _ip_cache:
        return _ip_cache[ip]
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"http://ip-api.com/json/{ip}?fields=status,countryCode")
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    locale = COUNTRY_TO_LOCALE.get(data.get("countryCode", ""), "en-US")
                    _ip_cache[ip] = locale
                    return locale
    except Exception:
        pass
    return None


@router.get("/locale")
async def get_locale(request: Request):
    ip = _get_client_ip(request)
    locale = await _geoip_lookup(ip)
    if not locale:
        al = request.headers.get("Accept-Language", "")
        if al.startswith("zh"):
            locale = "zh-CN"
        elif al.startswith("ja"):
            locale = "ja-JP"
        elif al.startswith("ko"):
            locale = "ko-KR"
        else:
            locale = "en-US"
    return {"locale": locale}
