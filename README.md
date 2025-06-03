# birdscope
This project uses visual data from a raspberry pi to inference the species of bird visible in that data.

**BirdScope** is a Raspberry Pi-based smart birdwatching device. It captures video using the official Pi Camera Module v2, allows motorized camera movement via a Pimoroni Pan-Tilt HAT, and streams or sends images to a separate device on the network for AI-powered bird species identification.

---

## Materials

| Component                     | Description                                          |
|-------------------------------|------------------------------------------------------|
| Raspberry Pi 3B+              | Main microcomputer controlling camera + motors       |
| Raspberry Pi Camera Module v2 | 8MP camera for capturing bird imagery                |
| Pimoroni Pan-Tilt HAT         | Dual-axis servo HAT to rotate and tilt the camera    |
| microSD Card (16GB)           | Storage for OS and project files                     |
| Raspberry Pi OEM Power Supply | 5V/2.5A power supply for stable operation            |
| Network access                | WiFi or LAN access to local/remote network           |
| Access to Secondary Device    | Any device capable of AI inferencing                 |

---

---

## OS Setup

To get started, you'll need to write the Raspberry Pi OS (Raspbian) onto your microSD card. Follow these steps:

### 1. Download Raspberry Pi Imager
- Download the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for your operating system (Windows, macOS, or Linux).
- Insert your **16GB microSD card** into your computer using a card reader.

### 2. Write the OS to the SD Card
- Launch Raspberry Pi Imager.
- Click **"Choose OS"** and select:
  - `Raspberry Pi OS (64-bit)` or
  - `Raspberry Pi OS Lite (64-bit)`
- Click **"Choose Storage"** and select your SD card.
- Before writing, click the gear ⚙️ icon (advanced options) and:
  - Set a hostname (e.g., `birdscope.local`)
  - Enable SSH (use password or public key)
  - Set default username and password
  - Configure Wi-Fi (SSID, password, country)
- Click **"Write"** and wait for the process to complete.

### 3. Boot the Pi
- Insert the microSD card into your Raspberry Pi 3B+.
- Connect power and wait 1–2 minutes for initial setup.
- You should now be able to SSH into the Pi:
  ```bash
  ssh pi@birdscope.local
  ```

---

## Update System Packages

After logging into your Pi for the first time, run the following to make sure your system is fully up to date:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

> This ensures that all packages, firmware, and the OS itself are current and reduces the chance of compatibility issues with Python libraries and peripherals.

---

Next: enabling the camera, installing servo + camera libraries, and writing the initial test script.