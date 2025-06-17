# Birdscope GPU Server

This component of the Birdscope project receives images over MQTT from Raspberry Pi clients, performs bird detection and classification using PyTorch-based deep learning models, logs the results, and serves a gallery web interface for verified predictions.

---

## Features

- Receives images over MQTT with credentialed access
- Runs an AI inference pipeline using PyTorch and Hugging Face models:
  - Object detection with Faster R-CNN
  - Bird classification with Swin Transformer fine-tuned on CUB-200
- Applies configurable confidence thresholds
- Annotates and saves detection results to `static/` for display
- Logs all predictions to `logs/predictions.jsonl`
- Serves a Flask-based gallery dashboard to view predictions
- Supports configuration via `.env` and `config.yaml`
- Unified entrypoint via `main.py`

---

## Project Structure

```
gpu-server/
├── main.py                   # Unified launcher: MQTT + Flask
├── mqtt_receiver.py          # Subscribes to MQTT topic and runs inference
├── config.yaml               # MQTT topics and file paths
├── .env                      # MQTT credentials and broker settings
├── requirements.txt          # Python package requirements
├── received_images/          # Incoming unprocessed images
├── static/                   # Annotated images served by gallery
├── logs/
│   └── predictions.jsonl     # Structured log of inference results
├── inference/
│   ├── classifier.py         # Bird classifier using Swin Transformer
│   ├── detector.py           # Object detector wrapper
│   ├── predict.py            # Core inference and postprocessing logic
│   └── image_utils.py        # Utility functions for image processing
├── gallery_app/
│   ├── app.py                # Flask app that serves the image gallery
│   └── templates/
│       └── index.html        # HTML template for gallery UI
└── .gitignore
```

---

## Setup

### System Requirements

- Linux system with Python 3.8+
- GPU optional (uses CUDA if available)
- Mosquitto MQTT broker installed and configured

### Install Python Dependencies

```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients python3-pip
pip3 install -r requirements.txt
```

---

## MQTT Configuration

Edit `/etc/mosquitto/conf.d/default.conf`:

```ini
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
```

Set up the password file:

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd gpu_server
```

Set up an ACL file:

```ini
# /etc/mosquitto/acl
user gpu_server
topic readwrite birdscope/#
```

Restart the broker:

```bash
sudo systemctl restart mosquitto
```

---

## Configuration

### `.env`

```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=gpu_server
MQTT_PASSWORD=your_password_here
MQTT_TOPIC=birdscope/image
```

### `config.yaml`

```yaml
broker: localhost
port: 1883
image_topic: birdscope/image
save_dir: received_images
```

---

## Running the Server

Launch the gallery server and MQTT listener:

```bash
python3 main.py
```

On image receipt:
- Detection + classification runs automatically
- Annotated image is saved to `static/`
- Metadata is appended to `logs/predictions.jsonl`

---

## Accessing the Gallery

Visit the local web dashboard at:

```
http://localhost:5000
```

Each entry shows:
- Timestamped image
- Detected bird bounding boxes
- Predicted species and confidence scores

---

## MQTT Protocol

| Topic              | Payload       | Description                      |
|--------------------|---------------|----------------------------------|
| `birdscope/image`  | JPEG bytes    | Sent from Pi on motion trigger   |
| `birdscope/status` | Status string | Optional: system info, ping, etc |

---

## Possible Enhancements

- Pagination or filters in the gallery UI
- SQLite or Postgres storage of prediction logs
- Add systemd service to autostart `main.py` on boot
- Batch image upload and archival support

