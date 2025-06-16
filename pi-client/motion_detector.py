#!/usr/bin/env python3
import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import Transform
import time

class MotionDetector:
    def __init__(self, threshold=5000, sleep_time=0.2):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": (640, 480)},
            transform=Transform(hflip=True, vflip=True)
        ))
        self.picam2.start()
        time.sleep(1)

        self.prev_gray = None
        self.threshold = threshold
        self.sleep_time = sleep_time

    def detect_motion(self):
        frame = self.picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        motion = False
        if self.prev_gray is not None:
            delta = cv2.absdiff(self.prev_gray, gray)
            thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
            motion_score = cv2.countNonZero(thresh)

            if motion_score > self.threshold:
                print(f"[Motion] Triggered! Score: {motion_score}")
                motion = True

        self.prev_gray = gray
        time.sleep(self.sleep_time)
        return motion
