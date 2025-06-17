# utils/classifier.py

from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch

class BirdClassifier:
    def __init__(self, model_name="Emiel/cub-200-bird-classifier-swin", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load model and image processor
        self.processor = AutoImageProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)
        self.model.eval()

        # Map class index → bird species name
        self.id2label = self.model.config.id2label

    def predict(self, pil_image):
        inputs = self.processor(images=pil_image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            conf, pred = torch.max(probs, dim=1)

        species = self.id2label.get(pred.item(), f"class_{pred.item()}")
        return species, conf.item()

