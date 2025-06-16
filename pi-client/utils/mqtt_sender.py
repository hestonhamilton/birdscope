import yaml
import paho.mqtt.client as mqtt
import time
import os

# === Load config ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

BROKER = config.get('broker', 'localhost')
PORT = config.get('port', 1883)
IMAGE_TOPIC = config.get('image_topic', 'birdwatcher/image')
STATUS_TOPIC = config.get('status_topic', 'birdwatcher/status')

# === Initialize MQTT Client ===
client = mqtt.Client()
client.connect(BROKER, PORT)
client.loop_start()  # Run network loop in background

# === Send Image ===
def send_image(jpeg_bytes):
    if jpeg_bytes:
        client.publish(IMAGE_TOPIC, jpeg_bytes)
        print(f"[MQTT] Image published to topic '{IMAGE_TOPIC}' ({len(jpeg_bytes)} bytes)")

# === Optional: Send Status ===
def send_status(message):
    payload = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}"
    client.publish(STATUS_TOPIC, payload)
    print(f"[MQTT] Status: {payload}")

