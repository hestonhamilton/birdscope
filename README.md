# BirdScope

**BirdScope** is a Raspberry Pi-based smart birdwatching device. It captures video using the official Pi Camera Module v2, allows motorized camera movement via a Pimoroni Pan-Tilt HAT, and streams or sends images to a separate device on the network for AI-powered bird species identification.

---

## 🧰 Materials

| Component                     | Description                                          |
|------------------------------|------------------------------------------------------|
| Raspberry Pi 3B+             | Main microcomputer controlling camera + motors      |
| Raspberry Pi Camera Module v2| 8MP camera for capturing bird imagery               |
| Pimoroni Pan-Tilt HAT        | Dual-axis servo HAT to rotate and tilt the camera   |
| microSD Card (16GB)          | Storage for OS and project files                    |
| Raspberry Pi OEM Power Supply| 5V/2.5A power supply for stable operation           |
| Network Access               | Wi-Fi or LAN access to local/remote network         |
| Secondary Device             | Any device capable of running AI inference models   |

---

## ⚙️ OS Setup

To get started, you'll need to write the Raspberry Pi OS (Raspbian) onto your microSD card. Follow these steps:

### 1. Download Raspberry Pi Imager

- Download the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for your OS (Windows, macOS, or Linux).
- Insert your **16GB microSD card** into your computer using a card reader.

### 2. Write the OS to the SD Card

- Launch Raspberry Pi Imager.
- Click **"Choose OS"** and select:
  - `Raspberry Pi OS (64-bit)` or
  - `Raspberry Pi OS Lite (64-bit)`
- Click **"Choose Storage"** and select your SD card.
- Click the gear ⚙️ icon (advanced options) and configure:
  - Hostname (e.g., `birdscope.local`)
  - Enable SSH (with password or public key)
  - Set default username/password
  - Wi-Fi SSID, password, and country

Then click **Write** and wait for the process to complete.

### 3. Boot the Pi

- Insert the microSD card into your Raspberry Pi 3B+.
- Connect power and wait 1–2 minutes for first boot.
- You should now be able to SSH into the Pi:
  ```bash
  ssh pi@birdscope.local
  ```

---

## 🛠 System Preparation

### 1. Update System Packages

Run these commands to ensure your Pi is fully updated:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

---

## 📸 Camera Setup

### 1. Verify Camera is Detected

Raspberry Pi OS Bullseye and newer use the `libcamera` stack, so no `raspi-config` setting is required.

Check for connected camera:

```bash
libcamera-hello --list-cameras
```

Expected output:
```
Available cameras
-----------------
0 : imx219 [3280x2464 10-bit RGGB] (...)
```

Test a capture:

```bash
libcamera-still -o test.jpg
```

> If your camera isn’t detected, check the ribbon cable connection and reboot.

---

## 🔌 Pan-Tilt HAT Setup

### 1. Install Pan-Tilt HAT Drivers (Recommended)

Install using Pimoroni’s official script:

```bash
curl https://get.pimoroni.com/pantilt | bash
```

This will:
- Install required Python libraries (`gpiozero`, `pigpio`, `pantilthat`, etc.)
- Enable I2C and SPI interfaces
- Set up the `pigpiod` daemon
- Provide example scripts and documentation

> ⚠️ On Raspberry Pi OS Bookworm, this may fail due to Python environment protections (PEP 668). If so, follow the system-wide install steps below.

---

### 2. Enable I²C (Required for Pan-Tilt Communication)

If you didn’t use the Pimoroni script, you must enable I²C manually:

```bash
sudo raspi-config
```

- Select **Interface Options**
- Enable **I2C**
- Exit and reboot if prompted

---

## 🔧 Install Dependencies (System-Wide)

To simplify compatibility with `picamera2`, install all Python packages via `apt` instead of a virtual environment.

```bash
sudo apt install -y python3-picamera2 python3-opencv python3-flask libcamera-apps
```

This installs:
- `picamera2`: modern Raspberry Pi camera library (uses libcamera)
- `opencv`: for face/bird recognition
- `flask`: for video streaming to the browser
- `libcamera-apps`: command-line tools like `libcamera-hello`, `libcamera-still`, etc.

---

### 3. Enable `pigpio` Daemon (If Not Already Enabled)

This is required for servo control via `pantilthat`:

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

---

✅ You're now ready to write Python scripts that:
- Control the pan/tilt movement
- Stream video to a browser
- Detect birds or faces in the video stream

Next: build your first test script using `picamera2` and `opencv`.
