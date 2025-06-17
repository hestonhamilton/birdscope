# mqtt_receiver.py

import os
import base64
import uuid
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from dotenv import load_dotenv

from inference.predict import predict
from inference.image_utils import save_annotated_image, log_predictions

# === Load environment and configuration ===
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "birdscope/image")

IMAGE_DIR = "received_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# === MQTT Handlers ===
def save_incoming_image(payload_bytes) -> str:
    """
    Save raw JPEG bytes from MQTT to a unique file in IMAGE_DIR.
    Returns full path to saved image.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
    path = os.path.join(IMAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(payload_bytes)
    print(f"[✔] Image saved: {path}")
    return path

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected successfully to {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"[MQTT] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"[MQTT] Received message on topic: {msg.topic}")
    try:
        image_path = save_incoming_image(msg.payload)
        predict(image_path)  # now handles saving + logging
    except Exception as e:
        print(f"[!] Error during inference: {e}")

# === MQTT Client Setup ===
def run(stop_event=None):
    """Start the MQTT receiver loop."""
    client = mqtt.Client()
    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)

    client.loop_start()
    print("[MQTT] Receiver started")
    try:
        if stop_event:
            stop_event.wait()
        else:
            while True:
                time.sleep(1)
    finally:
        client.loop_stop()
        client.disconnect()
        print("[MQTT] Receiver stopped")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("[MQTT] Interrupted, shutting down")

