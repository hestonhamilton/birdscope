# BirdScope

**BirdScope** is a real-time bird species identification system using AI-powered computer vision. It combines a Raspberry Pi camera module with cloud-based GPU inference to detect and classify birds using deep learning models.

This project showcases how embedded hardware, edge computing, and modern machine learning tools can work together in a full-stack, production-style pipeline.

---

## Why It Matters

BirdScope demonstrates:

- Real-world application of computer vision and deep learning
- Edge-to-cloud communication via MQTT
- Structured logging and thresholding for reliable AI inference
- Full-stack Python development including a Flask dashboard
- Hugging Face model integration in a custom PyTorch pipeline

Whether you're interested in wildlife monitoring, IoT, or end-to-end ML system design, BirdScope offers a complete example project for applied AI.

---

## Architecture Overview

```
┌────────────┐              MQTT               ┌──────────────┐
│ Raspberry  │ ─────────────▶────────────────▶ │ GPU Server   │
│ Pi Client  │                                 │ Inference    │
│ (camera +  │                                 │ + Gallery UI │
│ motion)    │ ◀────────────▶───────────────── │              │
└────────────┘        Status (optional)        └──────────────┘
```

1. The Pi detects motion and publishes camera frames via MQTT.
2. The GPU server runs object detection and classification models.
3. Annotated results and metadata are saved for later viewing.
4. A Flask app displays identified birds in a live gallery.

---

## Repository Structure

```
birdscope/
├── pi-client/         Raspberry Pi: camera, motion, MQTT publisher
├── gpu-server/        GPU server: detection, classification, MQTT, gallery
├── README.md          You're here
```

---

## Setup Instructions

Each part of BirdScope has its own README:

- [Pi Client Setup](./pi-client/README.md) – Set up camera, motion sensor, and MQTT publishing.
- [GPU Server Setup](./gpu-server/README.md) – Run inference pipeline, Flask gallery, and receive MQTT images.

---

## Technologies Used

- Computer Vision: PyTorch, torchvision, Faster R-CNN, Swin Transformer
- Model Inference: Hugging Face model hub, TorchScript-ready modules
- Image Handling: OpenCV, PIL, classification thresholding, JPEG pipelines
- Messaging: MQTT via Mosquitto and paho-mqtt
- Web UI: Flask for real-time image gallery
- Logging: JSONL structured prediction logs

---

## Future Enhancements

- Add audio detection with BirdNET integration
- Train custom bird classifier with regional data
- Add SQLite or PostgreSQL metadata indexing
- Deploy as containerized services
- Support multi-camera/multi-zone deployments

---

## License

This project is licensed under the MIT License.

