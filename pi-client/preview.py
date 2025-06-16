#!/usr/bin/env python3
from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import Transform
import cv2
import time

app = Flask(__name__)

# === Initialize camera ===
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (640, 480)},
    transform=Transform(hflip=True, vflip=True)
))
picam2.start()
time.sleep(1)

# ✅ Let camera handle white balance automatically
picam2.set_controls({
    "AwbMode": 1  # AUTO (no manual gains)
})

def generate_frames():
    while True:
        frame = picam2.capture_array()
        cv2.putText(frame, "AWB: auto", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2, cv2.LINE_AA)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return '<h1>Birdscope Stream (Auto White Balance)</h1><img src="/video_feed">'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Serving video at http://<pi-ip>:5000/")
    app.run(host='0.0.0.0', port=5000)
