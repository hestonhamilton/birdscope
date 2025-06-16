#!/usr/bin/env python3
from flask import Flask, render_template, Response, request, jsonify
import time
import cv2
from picamera2 import Picamera2
from utils.tilt_controller import PanTiltHelper

app = Flask(__name__)

# --- PanTiltHelper Initialization ---
pan_tilt_helper = PanTiltHelper(
    idle_timeout=5,
    pan_min_angle=-45, pan_max_angle=45,
    tilt_min_angle=-30, tilt_max_angle=60
)

# --- Camera Initialization ---
camera = None
try:
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
    camera.start()
    print("Camera initialized successfully.")
except Exception as e:
    print(f"Error initializing camera: {e}")

servo_1_enabled = True
servo_2_enabled = True

def generate_frames():
    """
    Generator function to yield JPEG frames from the camera with both vertical and horizontal flip.
    """
    flip_both_axes = True # Keep this True for both flips

    if camera is None:
        print("Camera not available for streaming. Showing placeholder.")
        dummy_frame = 255 * (cv2.imread('no_camera.jpg') if cv2.haveImageReader('no_camera.jpg') else None)
        if dummy_frame is None or dummy_frame.shape[0] == 0:
            dummy_frame = cv2.cvtColor(dummy_frame if dummy_frame is not None else (0,0,0), cv2.COLOR_BGR2RGB) # Ensure correct color for text
            dummy_frame = cv2.circle(dummy_frame, (320, 240), 100, (0, 0, 255), -1)
            dummy_frame = cv2.putText(dummy_frame, "NO CAMERA FEED", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        _, buffer = cv2.imencode('.jpg', dummy_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        return

    while True:
        try:
            frame = camera.capture_array()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if flip_both_axes:
                flipped_frame = cv2.flip(frame_rgb, -1)
                ret, buffer = cv2.imencode('.jpg', flipped_frame)
            else:
                ret, buffer = cv2.imencode('.jpg', frame_rgb)

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.03)
        except Exception as e:
            print(f"Error in camera streaming: {e}")
            break


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status_json')
def status_json():
    current_pan = pan_tilt_helper.get_current_pan_angle()
    current_tilt = pan_tilt_helper.get_current_tilt_angle()
    servos_active = pan_tilt_helper.is_initialized() and (servo_1_enabled or servo_2_enabled)

    return jsonify({
        "current_pan": current_pan if current_pan is not None else 0.0,
        "current_tilt": current_tilt if current_tilt is not None else 0.0,
        "servo_enabled": servos_active,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/move_pan', methods=['POST'])
def move_pan():
    data = request.get_json()
    angle_offset = data.get('angle_offset', 0)

    if not pan_tilt_helper.is_initialized():
        return jsonify({"status": "error", "message": "Pan-Tilt HAT not initialized."}), 500

    current_pan = pan_tilt_helper.get_current_pan_angle()
    if current_pan is None:
        return jsonify({"status": "error", "message": "Could not get current pan angle."}), 500

    new_pan = current_pan + angle_offset
    pan_tilt_helper.set_pan_angle(new_pan) # set_pan_angle handles clamping

    return jsonify({"status": "success", "new_pan_angle": new_pan})

@app.route('/move_tilt', methods=['POST'])
def move_tilt():
    data = request.get_json()
    angle_offset = data.get('angle_offset', 0)

    if not pan_tilt_helper.is_initialized():
        return jsonify({"status": "error", "message": "Pan-Tilt HAT not initialized."}), 500

    current_tilt = pan_tilt_helper.get_current_tilt_angle()
    if current_tilt is None:
        return jsonify({"status": "error", "message": "Could not get current tilt angle."}), 500

    new_tilt = current_tilt + angle_offset
    pan_tilt_helper.set_tilt_angle(new_tilt) # set_tilt_angle handles clamping

    return jsonify({"status": "success", "new_tilt_angle": new_tilt})

# --- NEW ROUTES for absolute positioning ---
@app.route('/set_pan_absolute', methods=['POST'])
def set_pan_absolute():
    data = request.get_json()
    target_angle = data.get('target_angle')

    if target_angle is None:
        return jsonify({"status": "error", "message": "Missing 'target_angle' in request."}), 400

    if not pan_tilt_helper.is_initialized():
        return jsonify({"status": "error", "message": "Pan-Tilt HAT not initialized."}), 500

    pan_tilt_helper.set_pan_angle(target_angle)
    return jsonify({"status": "success", "target_angle": target_angle})

@app.route('/set_tilt_absolute', methods=['POST'])
def set_tilt_absolute():
    data = request.get_json()
    target_angle = data.get('target_angle')

    if target_angle is None:
        return jsonify({"status": "error", "message": "Missing 'target_angle' in request."}), 400

    if not pan_tilt_helper.is_initialized():
        return jsonify({"status": "error", "message": "Pan-Tilt HAT not initialized."}), 500

    pan_tilt_helper.set_tilt_angle(target_angle)
    return jsonify({"status": "success", "target_angle": target_angle})

@app.route('/enable_servos', methods=['POST'])
def enable_servos():
    global servo_1_enabled, servo_2_enabled
    data = request.get_json()
    state = data.get('state', True)

    if not pan_tilt_helper.is_initialized():
        return jsonify({"status": "error", "message": "Pan-Tilt HAT not initialized."}), 500

    pan_tilt_helper.enable_servo(1, state)
    pan_tilt_helper.enable_servo(2, state)

    servo_1_enabled = state
    servo_2_enabled = state

    return jsonify({"status": "success", "servos_enabled": state})


if __name__ == '__main__':
    print("Visit http://<pi-ip>:5050/ to control Pan/Tilt HAT and view live camera feed.")
    try:
        app.run(host='0.0.0.0', port=5050, debug=False)
    finally:
        if camera:
            print("Stopping camera.")
            camera.stop()
            camera.close()