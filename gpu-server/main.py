import threading
import time

from gallery_app.app import app
import mqtt_receiver


def start_flask():
    print("[MAIN] Starting Flask gallery app...")
    app.run(host='0.0.0.0', port=8080, use_reloader=False)


def start_mqtt(stop_event):
    mqtt_receiver.run(stop_event)


def main():
    stop_event = threading.Event()

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    mqtt_thread = threading.Thread(target=start_mqtt, args=(stop_event,), daemon=True)

    flask_thread.start()
    mqtt_thread.start()

    print("[MAIN] Both services started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[MAIN] Shutdown signal received. Cleaning up...")
        stop_event.set()
        mqtt_thread.join()
        print("[MAIN] Shutdown complete.")


if __name__ == '__main__':
    main()
