import os
import time
import yaml
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# === Load sensitive credentials from .env ===
load_dotenv()
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# === Load connection and topic config from config.yaml ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

BROKER = config.get('broker', 'localhost')
PORT = config.get('port', 1883)
IMAGE_TOPIC = config.get('image_topic', 'birdwatcher/image')
STATUS_TOPIC = config.get('status_topic', 'birdwatcher/status')

# === Initialize MQTT Client ===
client = mqtt.Client()
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.connect(BROKER, PORT)
client.loop_start()  # Run network loop in background

# === Send JPEG image to broker ===
def send_image(jpeg_bytes):
    if jpeg_bytes:
        client.publish(IMAGE_TOPIC, jpeg_bytes)
        print(f"[MQTT] Image published to topic '{IMAGE_TOPIC}' ({len(jpeg_bytes)} bytes)")

# === Send status messages as text ===
def send_status(message):
    payload = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}"
    client.publish(STATUS_TOPIC, payload)
    print(f"[MQTT] Status: {payload}")

