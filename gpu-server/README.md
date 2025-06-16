# 🧠 Birdscope GPU Server

This server acts as both the **MQTT broker** and **image processor** for the Birdscope project. It receives images from the Raspberry Pi over MQTT, saves them, and prepares them for future inference and dashboard display.

---

## 📦 Features

- Runs Mosquitto MQTT broker
- Authenticated image ingestion via MQTT
- Saves incoming images from Pi in `received_images/`
- Uses `.env` for secure credentials
- Hybrid config via `.env` + `config.yaml`

---

## 📁 Project Structure

```
gpu-server/
├── mqtt_receiver.py        # Subscribes to MQTT topic and saves JPEGs
├── config.yaml             # Topic names, save path
├── .env                    # MQTT credentials
├── requirements.txt        # Python dependencies
├── received_images/        # Saved incoming images
└── .gitignore              # Hides .env from version control
```

---

## ⚙️ Setup

### 🐍 Python Dependencies

```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients python3-pip
pip3 install paho-mqtt opencv-python PyYAML python-dotenv
```

---

### 🔐 Mosquitto Configuration

Edit `/etc/mosquitto/conf.d/default.conf`:

```ini
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
```

Create password file:

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd gpu_server
```

Example ACL file at `/etc/mosquitto/acl`:

```ini
user gpu_server
topic readwrite birdscope/#
```

Restart Mosquitto:

```bash
sudo systemctl restart mosquitto
```

---

### 🔐 `.env`

```env
MQTT_USERNAME=gpu_server
MQTT_PASSWORD=your_password_here
```

---

### 📄 `config.yaml`

```yaml
broker: localhost
port: 1883
image_topic: birdscope/image
save_dir: received_images
```

---

## 🚀 Running the Image Receiver

```bash
python3 mqtt_receiver.py
```

Expected output:

```
[MQTT] Connected with result code 0
[MQTT] Message received on birdscope/image (xxxxx bytes)
[MQTT] Saved: received_images/YYYYMMDD-HHMMSS.jpg
```

---

## 📡 MQTT Protocol

| Topic            | Payload       | Description               |
|------------------|---------------|---------------------------|
| `birdscope/image` | JPEG bytes    | Image sent from Pi on motion |
| `birdscope/status` | (Optional) status text | Pi status messages |

---

## ✅ To Do (Optional Enhancements)

- Run inference pipeline on received images
- Acknowledge image receipt to Pi
- Add dashboard UI or database indexing
- Add systemd service for `mqtt_receiver.py`
