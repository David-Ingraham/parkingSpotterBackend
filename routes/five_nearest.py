import os
import time
from flask import Blueprint, request, jsonify
from PIL import Image
from helpers.fetch_image import fetch_and_save_image
from helpers.get_nearby_cameras import find_nearby_cameras
import psutil
import os
import inspect 

bp = Blueprint('five_nearest', __name__)
BASE_URL = os.getenv("BACKEND_URL")

def log_memory(label=""):
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / 1024 / 1024  # in MB
    print(f"[{label}] Memory usage: {mem:.2f} MB")

@bp.before_app_request
def log_headers():
    print("BASE_URL is:", BASE_URL)
    print(f"\n[{request.method}] {request.path}")
    for h, v in request.headers.items():
        print(f"{h}: {v}")

@bp.post("/fiveNearest")
def fiveNearest():
    print(f"Above is for the {inspect.stack()[1][3]} endpoint")
    

    log_memory("start /fiveNearest")
    start = time.time()
    data = request.get_json()
    lat, lng = data["lat"], data["lng"]
    
    # Delete old images
    img_dir = os.path.join("static", "imgs")
    os.makedirs(img_dir, exist_ok=True)
    for f in os.listdir(img_dir):
        os.remove(os.path.join(img_dir, f))

    cameras = find_nearby_cameras(lat, lng, "camera_id_lat_lng_wiped.json")
    if not cameras:
        return jsonify(error="no cameras nearby"), 404

    log_memory("after image fetch")

    stamp = int(time.time())
    output = []

    for addr, info in list(cameras.items())[:5]:
        try:
            img = fetch_and_save_image(info["camera_id"], stamp)
            if img.width > 640:
                h = img.height * 640 // img.width
                img = img.resize((640, h), Image.LANCZOS)

            filename = f"{stamp}_{addr.replace(' ', '_')}.jpg"
            path = os.path.join(img_dir, filename)
            with open(path, 'wb') as f:
                img.save(f, format="JPEG", quality=70, optimize=True)
                f.flush()
                os.fsync(f.fileno())

            output.append({
                "address": addr,
                "url": f"{BASE_URL}/static/imgs/{filename}"
            })
        except Exception as e:
            print(f"❌ Failed for {addr}: {e}")

    log_memory("before return")
    print(f"Request took {time.time() - start:.2f} seconds")

    return jsonify(images=output)
