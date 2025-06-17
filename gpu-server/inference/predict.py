import torch
import cv2
import numpy as np

from inference.detector import load_detector
from inference.classifier import load_classifier

# === Load models once at module level ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
detector = load_detector(device)
classifier = load_classifier(device)

def preprocess_image(image):
    """Convert a NumPy image (H x W x C) to PyTorch format"""
    image_tensor = torch.from_numpy(image / 255.0).float()  # normalize to [0,1]
    image_tensor = image_tensor.permute(2, 0, 1)  # HWC → CHW
    return image_tensor

def predict(image_path, conf_threshold=0.5):
    # === Load image ===
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        raise ValueError(f"Failed to load image: {image_path}")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    input_tensor = preprocess_image(image_rgb).unsqueeze(0).to(device)

    # === Run detection ===
    with torch.no_grad():
        outputs = detector(input_tensor)[0]

    boxes = outputs["boxes"]
    scores = outputs["scores"]
    labels = outputs["labels"]

    results = []
    for box, score, label in zip(boxes, scores, labels):
        if score.item() < conf_threshold:
            continue

        # Convert to integers for drawing/cropping
        x1, y1, x2, y2 = map(int, box.tolist())

        # === Placeholder: no classification yet ===
        results.append({
            "box": [x1, y1, x2, y2],
            "score": round(score.item(), 3),
            "label": f"object_{label.item()}",
            "species": "unknown",  # Placeholder for classifier result
            "confidence": None
        })

    return results

if __name__ == "__main__":
    test_img = "test.jpg"  # path to image
    preds = predict(test_img)

    for i, det in enumerate(preds):
        print(f"[{i}] Box: {det['box']}, Score: {det['score']}, Label: {det['label']}")

