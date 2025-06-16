from flask import Flask, render_template, Response, request, jsonify
import time
import cv2

def create_app(camera, pan_tilt_helper, motion_detector):
    app = Flask(__name__)

    servo_1_enabled = True
    servo_2_enabled = True

    def generate_frames():
        if camera is None:
            print("Camera not available for streaming. Showing placeholder.")
            dummy_frame = 255 * (cv2.imread('no_camera.jpg') if cv2.haveImageReader('no_camera.jpg') else None)
            if dummy_frame is None or dummy_frame.shape[0] == 0:
                dummy_frame = cv2.cvtColor(dummy_frame if dummy_frame is not None else (0, 0, 0), cv2.COLOR_BGR2RGB)
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
                ret, buffer = cv2.imencode('.jpg', frame_rgb)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
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
        return jsonify({
            "current_pan": pan_tilt_helper.get_current_pan_angle() or 0.0,
            "current_tilt": pan_tilt_helper.get_current_tilt_angle() or 0.0,
            "servo_enabled": pan_tilt_helper.is_initialized() and (servo_1_enabled or servo_2_enabled),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    # --- Servo control endpoints (move, set absolute, enable) ---
    @app.route('/move_pan', methods=['POST'])
    def move_pan():
        angle_offset = request.get_json().get('angle_offset', 0)
        pan_tilt_helper.set_pan_angle((pan_tilt_helper.get_current_pan_angle() or 0) + angle_offset)
        return jsonify({"status": "success"})

    @app.route('/move_tilt', methods=['POST'])
    def move_tilt():
        angle_offset = request.get_json().get('angle_offset', 0)
        pan_tilt_helper.set_tilt_angle((pan_tilt_helper.get_current_tilt_angle() or 0) + angle_offset)
        return jsonify({"status": "success"})

    @app.route('/set_pan_absolute', methods=['POST'])
    def set_pan_absolute():
        angle = request.get_json().get('target_angle')
        pan_tilt_helper.set_pan_angle(angle)
        return jsonify({"status": "success", "target_angle": angle})

    @app.route('/set_tilt_absolute', methods=['POST'])
    def set_tilt_absolute():
        angle = request.get_json().get('target_angle')
        pan_tilt_helper.set_tilt_angle(angle)
        return jsonify({"status": "success", "target_angle": angle})

    @app.route('/enable_servos', methods=['POST'])
    def enable_servos():
        nonlocal servo_1_enabled, servo_2_enabled
        state = request.get_json().get('state', True)
        pan_tilt_helper.enable_servo(1, state)
        pan_tilt_helper.enable_servo(2, state)
        servo_1_enabled = servo_2_enabled = state
        return jsonify({"status": "success", "servos_enabled": state})

    @app.route('/test_motion')
    def test_motion():
        try:
            for _ in range(3):
                motion_detector.detect_motion()
                time.sleep(0.1)
            detected = motion_detector.detect_motion()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

        return jsonify({"status": "success", "motion_detected": detected})

    return app

