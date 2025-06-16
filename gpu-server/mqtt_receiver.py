#!/usr/bin/env python3
import os
import time
import yaml
import cv2
import numpy as np
import paho.mqtt.client as mqtt

with open("config.yaml") as f:
    config = yaml.safe_load(f)

BROKER = config["broker"]
PORT = config["port"]
TOPIC = config["image_topic"]
SAVE_DIR = config.get("save_dir", "received_images")
os.makedirs(SAVE_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    np_arr = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        print("[MQTT] Failed to decode image.")
        return
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(SAVE_DIR, f"{timestamp}.jpg")
    cv2.imwrite(filename, image)
    print(f"[MQTT] Saved image: {filename}")

client = mqtt.Client()
client.username_pw_set("birdpi", "<your-password>")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_forever()

