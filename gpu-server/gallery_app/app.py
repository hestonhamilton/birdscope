from flask import Flask, render_template, request, url_for
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, '..', 'logs', 'predictions.jsonl')
STATIC_PATH = os.path.join(BASE_DIR, '..', 'received_images')

app = Flask(__name__, static_folder=STATIC_PATH, template_folder='templates')


def load_predictions(min_conf: float):
    """Load predictions from log file filtered by min confidence."""
    entries = []
    if not os.path.exists(LOG_FILE):
        return entries

    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            detections = [d for d in data.get('detections', []) if d.get('confidence', 0) >= min_conf]
            if not detections:
                continue

            entries.append({
                'timestamp': data.get('timestamp'),
                'image_file': data.get('image_file'),
                'detections': detections
            })

    entries.sort(key=lambda x: x['timestamp'], reverse=True)
    return entries


@app.route('/')
def index():
    min_conf = request.args.get('min_conf', default=0.6, type=float)
    entries = load_predictions(min_conf)
    return render_template('index.html', entries=entries, min_conf=min_conf)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
