import random, string, io, math
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

# In-memory store for captcha codes (in production, use Redis)
_captcha_store: dict[str, dict] = {}

router = APIRouter(prefix="/captcha", tags=["验证码"])


def _generate_captcha_text(length=4) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _generate_svg(text: str) -> str:
    """Generate a noisy SVG captcha image without external dependencies."""
    width = 130
    height = 48
    char_count = len(text)
    char_width = width // char_count
    
    # Colors
    bg_color = "#1e293b"
    text_colors = ["#06b6d4", "#8b5cf6", "#22d3ee", "#a78bfa", "#34d399", "#f472b6"]
    line_color = "#334155"
    
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0,0,{width},{height}">']
    lines.append(f'<rect width="{width}" height="{height}" fill="{bg_color}" rx="8"/>')
    
    # Random interference lines
    for _ in range(random.randint(3, 6)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line_color}" stroke-width="{random.randint(1, 2)}" opacity="0.5"/>')
    
    # Random dots
    for _ in range(random.randint(20, 40)):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        r = random.randint(1, 2)
        lines.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{line_color}" opacity="0.4"/>')
    
    # Characters with random rotation, position and color
    for i, ch in enumerate(text):
        x = i * char_width + char_width // 2 - 4 + random.randint(-3, 3)
        y = height // 2 + random.randint(-5, 5)
        angle = random.randint(-25, 25)
        color = random.choice(text_colors)
        font_size = random.randint(24, 30)
        lines.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-size="{font_size}" '
            f'font-weight="bold" font-family="Arial" text-anchor="middle" '
            f'transform="rotate({angle},{x},{y})" dominant-baseline="central">'
            f'{ch}</text>'
        )
    
    lines.append('</svg>')
    return '\n'.join(lines)


@router.get("/image")
def get_captcha():
    """Generate and return a CAPTCHA SVG."""
    text = _generate_captcha_text()
    captcha_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    _captcha_store[captcha_id] = {"text": text.lower(), "created_at": __import__("time").time()}
    
    svg = _generate_svg(text)
    return {"captcha_id": captcha_id, "svg": svg}


def verify_captcha(captcha_id: str, captcha_text: str) -> bool:
    """Verify captcha text (case-insensitive, one-time use)."""
    stored = _captcha_store.pop(captcha_id, None)
    if stored is None:
        return False
    return stored["text"] == captcha_text.lower()


def cleanup_expired():
    """Remove captchas older than 5 minutes."""
    now = __import__("time").time()
    expired = [k for k, v in _captcha_store.items() if now - v["created_at"] > 300]
    for k in expired:
        _captcha_store.pop(k, None)
