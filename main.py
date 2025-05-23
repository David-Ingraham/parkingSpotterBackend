"""
caching the phtos from the camera api in a folde ron ther server so that ther server can 

give a uri frot he frontd end to access. 

current working backend implementation 

"""



import os
import time
import base64
from io import BytesIO
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from fetch_image import fetch_and_save_image
from get_nearby_cameras import find_nearby_cameras
from dotenv import load_dotenv
import psutil

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

def log_memory(label=""):
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / 1024 / 1024  # in MB
    print(f"[{label}] Memory usage: {mem:.2f} MB")

@app.post("/photo")
def photo():
    

    log_memory("start /photo")
    print("hello")
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
                os.fsync(f.fileno())  # <- force write to disk


            output.append({
                "address": addr,
                "url": f"https://parkingspotterbackend.onrender.com/static/imgs/{filename}"
            })
        except Exception as e:
            print(f"❌ Failed for {addr}: {e}")

    log_memory("before return")
    print(f"Request took {time.time() - start:.2f} seconds")


    return jsonify(images=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
