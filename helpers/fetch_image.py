import json
import requests
from PIL import Image
from io import BytesIO
import time


def fetch_and_save_image(camera_id, timestamp):
    """Fetch an image from the NYC traffic camera API"""
    try:
        api_url = f'https://webcams.nyctmc.org/api/cameras/{camera_id}/image?t={timestamp}'
        print(f"[DEBUG] Fetching image from: {api_url}")
        
        response = requests.get(api_url)
        print(f"[DEBUG] Response status: {response.status_code}, Content length: {len(response.content) if response.status_code == 200 else 0}")
        
        if response.status_code == 200:
            try:
                img = Image.open(BytesIO(response.content))
                print(f"[DEBUG] Successfully opened image: {img.format}, Size: {img.size}")
                return img
            except Exception as e:
                print(f"[ERROR] Failed to process image for camera {camera_id}: {e}")
                return None
        else:
            print(f"[ERROR] Failed to fetch image for camera {camera_id}. Status Code: {response.status_code}")
            if response.status_code != 404:  # Don't print potentially large error responses
                print(f"[DEBUG] Error response: {response.text[:200]}...")
            return None

    except Exception as e:
        print(f"[ERROR] Request failed for camera {camera_id}: {e}")
        return None

def load_camera_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] camera_addresses_to_id.json file not found. Please run the scraping script first.")
        return None
    except json.JSONDecodeError:
        print("[ERROR] JSON file is malformed.")
        return None