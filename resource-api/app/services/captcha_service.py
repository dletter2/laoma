import io
import uuid
import time
import random
import string
from PIL import Image, ImageDraw, ImageFont

_captcha_store: dict[str, tuple[str, float]] = {}
CAPTCHA_EXPIRE_SECONDS = 300
MAX_CAPTCHA_STORE = 1000


def generate_captcha_text(length: int = 4) -> str:
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "").replace("L", "")
    return "".join(random.choice(chars) for _ in range(length))


def generate_captcha_image(text: str) -> bytes:
    width, height = 120, 40
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()

    x_start = 10
    for ch in text:
        y = random.randint(2, 8)
        draw.text((x_start, y), ch, fill=(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)), font=font)
        x_start += 24

    for _ in range(5):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=1)

    for _ in range(30):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def create_captcha() -> dict:
    _cleanup_expired()
    if len(_captcha_store) >= MAX_CAPTCHA_STORE:
        oldest_key = next(iter(_captcha_store))
        del _captcha_store[oldest_key]
    text = generate_captcha_text()
    key = uuid.uuid4().hex
    _captcha_store[key] = (text.upper(), time.time())
    image_bytes = generate_captcha_image(text)
    import base64
    image_b64 = base64.b64encode(image_bytes).decode()
    return {"captcha_key": key, "captcha_image": f"data:image/png;base64,{image_b64}"}


def verify_captcha(key: str, answer: str) -> bool:
    _cleanup_expired()
    entry = _captcha_store.pop(key, None)
    if entry is None:
        return False
    text, ts = entry
    if time.time() - ts > CAPTCHA_EXPIRE_SECONDS:
        return False
    return text == answer.strip().upper()


def _cleanup_expired():
    now = time.time()
    expired = [k for k, (_, ts) in _captcha_store.items() if now - ts > CAPTCHA_EXPIRE_SECONDS]
    for k in expired:
        del _captcha_store[k]
