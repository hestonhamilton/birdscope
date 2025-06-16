#!/usr/bin/env python3
import time
from flask import Flask
from picamera2 import Picamera2
from libcamera import Transform
from utils.tilt_controller import PanTiltHelper
from utils.motion_detector import MotionDetector
from app import create_app

# --- Camera ---
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(hflip=True, vflip=True)))
camera.start()
time.sleep(1)

# --- PanTilt ---
pan_tilt_helper = PanTiltHelper(
    idle_timeout=5,
    pan_min_angle=-45, pan_max_angle=45,
    tilt_min_angle=-30, tilt_max_angle=60
)

# --- MotionDetector ---
motion_detector = MotionDetector(camera)

# --- Create Flask App ---
app = create_app(camera, pan_tilt_helper, motion_detector)

if __name__ == '__main__':
    print("Visit http://<pi-ip>:5050/ to control Pan/Tilt HAT and view live camera feed.")
    try:
        app.run(host='0.0.0.0', port=5050)
    finally:
        print("Shutting down camera.")
        camera.stop()
        camera.close()

