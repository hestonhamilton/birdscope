#!/usr/bin/env python3
from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import Transform
import cv2

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (1920, 1080)},
    transform=Transform(hflip=True, vflip=True)  # 180° flip
))
picam2.set_controls({"AwbMode": 0})  # Auto white balance
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Serving video at http://<pi-ip>:5000/video_feed")
    app.run(host='0.0.0.0', port=5000)
