# inference/predict.py

import torch
import cv2
import json
import os
import numpy as np
import shutil
from datetime import datetime
from PIL import Image
from inference.detector import load_detector
from inference.classifier import BirdClassifier
from inference.image_utils import (
    preprocess_image,
    save_annotated_image,
    log_predictions,
)

# === Load models once ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
detector = load_detector(device)
classifier = BirdClassifier(device=device)

STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

def predict(image_path, conf_threshold=0.5):
    # === Load image ===
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        raise ValueError(f"Failed to load image: {image_path}")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    input_tensor = preprocess_image(image_rgb).unsqueeze(0).to(device)

    # === Run object detection ===
    with torch.no_grad():
        outputs = detector(input_tensor)[0]

    boxes = outputs["boxes"]
    scores = outputs["scores"]
    labels = outputs["labels"]

    results = []
    for box, score, label in zip(boxes, scores, labels):
        if score.item() < conf_threshold:
            continue

        x1, y1, x2, y2 = map(int, box.tolist())
        crop = image_rgb[y1:y2, x1:x2]

        if crop.shape[0] < 10 or crop.shape[1] < 10:
            print(f"Skipping tiny crop: {crop.shape}")
            continue

        crop_pil = Image.fromarray(crop)
        species, confidence = classifier.predict(crop_pil)
        print(f"Predicted: {species} ({confidence:.2f})")

        results.append({
            "box": [x1, y1, x2, y2],
            "score": round(score.item(), 3),
            "label": f"object_{label.item()}",
            "species": species,
            "confidence": round(confidence, 3)
        })

    # === Postprocessing ===
    if results:
        annotated_path = save_annotated_image(image_path, results)
        log_predictions(image_path, results)

        # Copy to static/ for gallery
        static_path = os.path.join(STATIC_DIR, os.path.basename(annotated_path))
        if annotated_path != static_path:
            shutil.copy(annotated_path, static_path)
            print(f"[✔] Copied to gallery: {static_path}")

    return results

if __name__ == "__main__":
    test_img = "test.jpg"
    preds = predict(test_img)

    for i, det in enumerate(preds):
        print(f"[{i}] Box: {det['box']}, Score: {det['score']}, Label: {det['label']}, Species: {det['species']}")

