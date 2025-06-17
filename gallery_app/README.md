# BirdScope Gallery App

This simple Flask application displays a gallery of annotated bird images that have been processed by the GPU inference server. Images are shown only if at least one detection meets a specified confidence threshold.

## Running

From the project root:

```bash
cd gallery_app
FLASK_APP=app.py flask run --host=0.0.0.0 --port=8080
```

Then visit `http://<gpu-server-ip>:8080/` in your browser.

You can filter results by minimum confidence using the `min_conf` query parameter, for example: `/?min_conf=0.7`.
