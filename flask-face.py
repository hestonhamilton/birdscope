#!/usr/bin/env python3
from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import Transform
import pantilthat
import cv2
import time

app = Flask(__name__)

# === CAMERA INIT ===
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (640, 480)},
    transform=Transform(hflip=True, vflip=True)
))
picam2.start()

# === CASCADE INIT ===
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# === INITIAL SERVO SNAP TO POSITION ===
DEFAULT_PAN = 0.0
DEFAULT_TILT = -30.0  # angled downward by default
current_pan = pantilthat.get_pan() or 0.0
current_tilt = pantilthat.get_tilt() or 0.0

print(f"Moving to default position (Pan: {DEFAULT_PAN}, Tilt: {DEFAULT_TILT})")

def smooth_move(start, end, steps=20, delay=0.03):
    delta = (end - start) / steps
    for i in range(steps):
        yield start + delta * (i + 1)
        time.sleep(delay)

for p in smooth_move(current_pan, DEFAULT_PAN):
    pantilthat.pan(p)
    current_pan = p

for t in smooth_move(current_tilt, DEFAULT_TILT):
    pantilthat.tilt(t)
    current_tilt = t


# === TRACKING PARAMS ===
FRAME_CENTER_X = 320
FRAME_CENTER_Y = 240
PAN_STEP = 5.0
TILT_STEP = 5.0
SMOOTHING = 0.2
TOLERANCE = 40

# === SCAN STATE ===
scanning = True
scan_direction = 1
scan_tilt_direction = -1
scan_pause_frames = 0
MAX_PAN = 90
MIN_PAN = -90
MAX_TILT = 80
MIN_TILT = -80

def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)

def generate_frames():
    global current_pan, current_tilt, scanning, scan_direction, scan_tilt_direction, scan_pause_frames

    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            cx = x + w // 2
            cy = y + h // 2
            dx = cx - FRAME_CENTER_X
            dy = cy - FRAME_CENTER_Y

            scanning = False
            scan_pause_frames = 15  # brief lock before scanning resumes

            if abs(dx) > TOLERANCE:
                target_pan = current_pan - PAN_STEP if dx > 0 else current_pan + PAN_STEP
                current_pan = (1 - SMOOTHING) * current_pan + SMOOTHING * target_pan

            if abs(dy) > TOLERANCE:
                target_tilt = current_tilt + TILT_STEP if dy > 0 else current_tilt - TILT_STEP
                current_tilt = (1 - SMOOTHING) * current_tilt + SMOOTHING * target_tilt

            current_pan = clamp(current_pan, MIN_PAN, MAX_PAN)
            current_tilt = clamp(current_tilt, MIN_TILT, MAX_TILT)
            pantilthat.pan(current_pan)
            pantilthat.tilt(current_tilt)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        else:
            if scan_pause_frames > 0:
                scan_pause_frames -= 1
            else:
                scanning = True

        # === SCANNING MODE ===
        if scanning:
            current_pan += scan_direction * 4.0  # Scan 4° per frame (faster)
            if current_pan >= MAX_PAN or current_pan <= MIN_PAN:
                scan_direction *= -1
                current_pan = clamp(current_pan, MIN_PAN, MAX_PAN)

                current_tilt += scan_tilt_direction * 5
                if current_tilt >= MAX_TILT or current_tilt <= MIN_TILT:
                    scan_tilt_direction *= -1
                current_tilt = clamp(current_tilt, MIN_TILT, MAX_TILT)
                pantilthat.tilt(current_tilt)

            pantilthat.pan(current_pan)

        # === HUD ===
        cv2.drawMarker(frame, (FRAME_CENTER_X, FRAME_CENTER_Y), (0, 0, 255),
                       markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.putText(frame, f"Pan: {int(current_pan)} Tilt: {int(current_tilt)}",
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return '<h1>Birdscope Face Tracking</h1><img src="/video_feed">'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Serving video at http://<pi-ip>:5000/")
    app.run(host='0.0.0.0', port=5000)

