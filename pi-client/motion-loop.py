#!/usr/bin/env python3

import time
from utils.camera import PiCameraCapture
from utils.motion_detector import MotionDetector
from utils.image_utils import encode_image_to_jpeg
from utils.mqtt_sender import send_image, send_status

COOLDOWN_SECONDS = 30

def main():
    print("[MotionLoop] Initializing camera and motion detector...")
    camera = PiCameraCapture()
    detector = MotionDetector(camera.camera)

    last_sent_time = 0

    print("[MotionLoop] Starting motion detection loop...")
    while True:
        try:
            motion = detector.detect_motion()
            now = time.time()

            if motion:
                print(f"[MotionLoop] Motion detected at {time.strftime('%H:%M:%S')}")

                if now - last_sent_time >= COOLDOWN_SECONDS:
                    frame = camera.capture_frame()
                    jpeg = encode_image_to_jpeg(frame)

                    if jpeg:
                        send_image(jpeg)
                        send_status("Motion image sent")
                        last_sent_time = now
                    else:
                        print("[MotionLoop] Failed to encode image.")
                else:
                    remaining = COOLDOWN_SECONDS - (now - last_sent_time)
                    print(f"[MotionLoop] Cooldown active ({remaining:.1f}s remaining)")
        except KeyboardInterrupt:
            print("\n[MotionLoop] Interrupted. Exiting.")
            break
        except Exception as e:
            print(f"[MotionLoop] Error: {e}")
            time.sleep(2)

    camera.stop()
    print("[MotionLoop] Camera stopped.")

if __name__ == "__main__":
    main()

