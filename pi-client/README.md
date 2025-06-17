# Birdscope Pi Client

This Raspberry Pi client captures video, detects motion, and sends frames to a GPU server over MQTT for bird detection and classification.

---

## Features

- Motion detection using frame differencing
- JPEG image encoding and MQTT publishing
- Configurable pan/tilt control via Pimoroni PanTilt HAT
- Flask interface for live video and manual control
- `.env` + `config.yaml` driven configuration
- Cooldown logic to prevent rapid resends

---

## Materials

| Component                     | Description                                  |
|-------------------------------|----------------------------------------------|
| Raspberry Pi 3B+ or newer     | Hosts camera, HAT, and motion logic          |
| Camera Module v2              | 8MP image sensor with ribbon connector       |
| Pimoroni Pan-Tilt HAT         | Dual servo control for positioning camera    |
| microSD Card (16GB or more)   | OS and code storage                          |
| Power Supply (5V/2.5A+)       | Reliable power for camera and motors         |

---

## OS Installation & Camera Setup

### 1. Flash Raspberry Pi OS

- Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- Choose `Raspberry Pi OS Lite (64-bit)`
- Use the gear icon to:
  - Set hostname (e.g. `birdscope.local`)
  - Enable SSH
  - Set user/password
  - Configure Wi-Fi (SSID, pass)

### 2. Boot & Update System

SSH into your Pi after first boot:

```bash
ssh pi@birdscope.local
```

Update packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### 3. Verify Camera Detection

Modern Pi OS uses libcamera:

```bash
libcamera-hello --list-cameras
```

Expect output like:

```
0 : imx219 [3280x2464 10-bit RGGB] (/base/soc/i2c0mux/i2c@1/imx219@10)
```

Test capture:

```bash
libcamera-still -o test.jpg
```

---

## Install Dependencies

### System Packages

```bash
sudo apt-get install -y python3-picamera2 python3-opencv \
    python3-paho-mqtt python3-yaml python3-flask \
    python3-gpiozero python3-pigpio python3-dotenv
```

### Pan-Tilt HAT Support

Install Pimoroni libraries:

```bash
curl https://get.pimoroni.com/pantilt | bash
```

Ensure `pigpiod` is running:

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

---

## Configuration

### `.env`

Create a `.env` file:

```env
MQTT_USERNAME=birdpi
MQTT_PASSWORD=your_password_here
```

### `config.yaml`

Example:

```yaml
broker: 192.168.1.100       # GPU server IP
port: 1883
image_topic: birdscope/image
status_topic: birdscope/status
cooldown: 30
min_motion_area: 500
tilt:
  min_pan: -90
  max_pan: 90
  min_tilt: -45
  max_tilt: 45
```

---

## Project Structure

```
pi-client/
├── main.py                  # Optional Flask control panel
├── app.py                   # Flask UI routes and video stream
├── motion_mqtt_loop.py      # Main runtime loop (motion → MQTT)
├── send_test_image.py       # One-off JPEG sender
├── tilt_preview.py          # Servo test script
├── config.yaml              # Broker IP, topics, motion params
├── .env                     # MQTT credentials
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html           # Flask UI
└── utils/
    ├── camera.py            # Picamera2 wrapper
    ├── image_utils.py       # Encode/resize logic
    ├── mqtt_sender.py       # MQTT send logic
    ├── tilt_controller.py   # Servo helper
    └── motion_detector.py   # Frame diff logic
```

---

## Running

### Motion + MQTT Runtime

```bash
python3 motion_mqtt_loop.py
```

On motion:
- Captures frame
- Encodes as JPEG
- Publishes to MQTT topic

### Manual Test Image

```bash
python3 send_test_image.py
```

Sends one image to GPU server for test classification.

### Flask UI

```bash
python3 main.py
```

Visit `http://<pi-ip>:5050` in your browser to view the control interface.

---

## Autostart (Optional)

To run `motion_mqtt_loop.py` on boot:

```bash
sudo nano /etc/systemd/system/birdscope-motion.service
```

Paste:

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

Enable it:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable birdscope-motion
sudo systemctl start birdscope-motion
```

---

## MQTT Protocol

| Topic              | Payload           | Description                    |
|-------------------|-------------------|--------------------------------|
| `birdscope/image`  | JPEG bytes        | Motion-triggered frame         |
| `birdscope/status` | Text message      | Optional status/heartbeat logs |

