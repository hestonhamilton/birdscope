import torchvision
import torch

def load_detector(device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load pretrained Faster R-CNN model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")

    model.to(device)
    model.eval()  # Set to inference mode (no training updates)
    print("[Detector] Model loaded and ready.")
    return model

