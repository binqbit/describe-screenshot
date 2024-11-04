import base64
from PIL import PngImagePlugin, ImageGrab
import io
import time

last_screenshot = None

def get_screenshot():
    image = ImageGrab.grabclipboard()
    if type(image) == PngImagePlugin.PngImageFile:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()
        global last_screenshot
        if last_screenshot is None or last_screenshot != image_bytes:
            last_screenshot = image_bytes
            return image_bytes
        return None
    return None

def to_base64_url(image_bytes):
    data = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{data}"

def listen_screenshot():
    print("Waiting for screenshot...")
    global last_screenshot
    if last_screenshot is None:
        last_screenshot = get_screenshot()
        if last_screenshot is None:
            last_screenshot = b""

    while True:
        image_bytes = get_screenshot()
        if image_bytes:
            image_url = to_base64_url(image_bytes)
            return image_url
        time.sleep(0.1)
