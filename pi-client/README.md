# 🐦 Birdscope Pi Client

This Raspberry Pi client captures video, detects motion, and sends frames to a GPU server over MQTT for bird detection and classification.

---

## 📦 Features

- Motion detection using frame differencing
- JPEG image encoding and MQTT publishing
- Configurable pan/tilt control via Pimoroni PanTilt HAT
- Flask interface for live video and manual control
- `.env` + `config.yaml` driven configuration
- Cooldown logic to prevent rapid resends

---

## 📁 Project Structure

```
pi-client/
├── main.py                  # Old Flask entry point (now uses app.py)
├── app.py                   # Flask routes for video + control
├── motion_mqtt_loop.py      # Main runtime script (motion → image → MQTT)
├── send_test_image.py       # Manual test image sender
├── tilt_preview.py          # Manual pan/tilt test
├── config.yaml              # Broker IP, topics, tilt limits
├── .env                     # MQTT credentials
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html           # Web control UI
├── utils/
│   ├── camera.py            # PiCamera2 wrapper
│   ├── image_utils.py       # JPEG encode/decode
│   ├── mqtt_sender.py       # MQTT send logic
│   ├── tilt_controller.py   # PanTilt HAT servo helper
│   └── motion_detector.py   # Frame diff motion logic
```

---

## ⚙️ Setup

### 🐍 Python Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-picamera2 python3-opencv python3-paho-mqtt python3-yaml
pip3 install python-dotenv
```

> If using legacy Pi OS: install `libcamera` support and ensure your system supports Picamera2.

---

### 📄 `config.yaml`

```yaml
broker: BROKER_IP                 # IP of the GPU server
port: 1883
image_topic: birdscope/image
status_topic: birdscope/status
```

---

### 🔐 `.env`

```env
MQTT_USERNAME=birdpi
MQTT_PASSWORD=your_password_here
```

---

## 🚀 Running

### ✅ Run Motion Detection + MQTT Sending

```bash
python3 motion_mqtt_loop.py
```

On motion detection:
- Frame is captured
- JPEG is sent to `image_topic` via MQTT
- Cooldown prevents further sends for 30 seconds

---

### 🧪 Run Manual Test

```bash
python3 send_test_image.py
```

Captures a single image and sends it immediately.

---

### 🌐 Run Flask UI (optional)

```bash
python3 main.py
```

Visit:

```
http://<pi-ip>:5050/
```

- See live video
- Move pan/tilt
- Test motion via `/test_motion`

---

## 🔁 Autostart (Optional)

To run `motion_mqtt_loop.py` on boot:

```bash
sudo nano /etc/systemd/system/birdscope-motion.service
```

```ini
[Unit]
Description=Birdscope Motion Detection Client
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/birdscope/pi-client/motion_mqtt_loop.py
WorkingDirectory=/home/pi/birdscope/pi-client
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Then enable:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable birdscope-motion
sudo systemctl start birdscope-motion
```

---

## 📡 MQTT Protocol

| Topic             | Payload           | Description                    |
|------------------|-------------------|--------------------------------|
| `birdscope/image` | JPEG bytes        | Motion-triggered frame         |
| `birdscope/status` | Text message     | Optional status/heartbeat logs |

---

## ✅ To Do (Optional Enhancements)

- Add MQTT reconnection and retry logic
- Send bounding box metadata from GPU server back to Pi
- Rotate or sweep pan/tilt on motion
