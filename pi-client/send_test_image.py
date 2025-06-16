#!/usr/bin/env python3

import time
from utils.camera import PiCameraCapture
from utils.image_utils import encode_image_to_jpeg
from utils.mqtt_sender import send_image

def main():
    print("[Test] Initializing camera...")
    camera = PiCameraCapture()
    frame = camera.capture_frame()

    if frame is None:
        print("[Test] Failed to capture frame.")
        return

    print("[Test] Encoding frame to JPEG...")
    jpeg_bytes = encode_image_to_jpeg(frame)

    if not jpeg_bytes:
        print("[Test] Failed to encode image.")
        return

    print("[Test] Sending image to GPU server...")
    send_image(jpeg_bytes)
    print("[Test] Done.")

    camera.stop()

if __name__ == "__main__":
    main()

