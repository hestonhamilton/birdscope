#!/usr/bin/env python3
from flask import Flask, jsonify
import time
from motion_detector import detect_motion

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Birdscope Motion Detector</h1><p>Visit /status for real-time motion state.</p>'

@app.route('/status')
def status():
    triggered = detect_motion()
    return jsonify({
        "motion": triggered,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    print("Visit http://<pi-ip>:5050/status to test motion")
    app.run(host='0.0.0.0', port=5050)

