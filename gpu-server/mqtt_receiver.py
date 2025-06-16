import os
import time
import yaml
import cv2
import numpy as np
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# === Load .env for sensitive credentials ===
load_dotenv()
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# === Load config.yaml ===
with open("config.yaml") as f:
    config = yaml.safe_load(f)

BROKER = config["broker"]
PORT = config["port"]
TOPIC = config["image_topic"]
SAVE_DIR = config["save_dir"]
os.makedirs(SAVE_DIR, exist_ok=True)

# === MQTT Handlers ===
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    if rc == 0:
        print(f"[MQTT] Subscribing to topic: {TOPIC}")
        client.subscribe(TOPIC)
    else:
        print("[MQTT] Connection failed — check credentials or broker config.")

def on_message(client, userdata, msg):
    print(f"[MQTT] Message received on {msg.topic} ({len(msg.payload)} bytes)")
    np_arr = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        print("[MQTT] Failed to decode image.")
        return
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(SAVE_DIR, f"{timestamp}.jpg")
    cv2.imwrite(filename, image)
    print(f"[MQTT] Saved: {filename}")

# === Setup MQTT client ===
client = mqtt.Client()
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_forever()

