# inference/image_utils.py

import os
import json
from datetime import datetime
import cv2
import torch
import numpy as np

# === Output directories ===
STATIC_DIR = "static"
LOG_DIR = "logs"
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def preprocess_image(image: np.ndarray) -> torch.Tensor:
    """
    Convert a NumPy image (H x W x C) to a normalized CHW PyTorch tensor.
    """
    image_tensor = torch.from_numpy(image / 255.0).float()
    image_tensor = image_tensor.permute(2, 0, 1)
    return image_tensor

def draw_boxes(image: np.ndarray, detections: list) -> np.ndarray:
    """
    Draw bounding boxes and species labels on the given image.
    """
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        label = f"{det['species']} ({det['confidence']:.2f})"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return image

def save_annotated_image(image_path: str, detections: list) -> str:
    """
    Draw boxes on the image and save to `static/` folder.
    Returns path to saved image.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"[!] Could not load image: {image_path}")
        return None
    annotated = draw_boxes(image, detections)
    base = os.path.splitext(os.path.basename(image_path))[0]
    save_path = os.path.join(STATIC_DIR, f"{base}_annotated.jpg")
    cv2.imwrite(save_path, annotated)
    print(f"Saved annotated image to {save_path}")
    return save_path

def log_predictions(image_path: str, detections: list, log_file: str = "logs/predictions.jsonl") -> None:
    """
    Append detection results to the prediction log.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "image_file": os.path.basename(image_path),
        "detections": detections
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"Logged predictions to {log_file}")

