import torchvision.models as models
import torch.nn as nn
import torch

def load_classifier(device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = models.resnet50(weights="DEFAULT")
    
    # Replace last layer with 200 classes for CUB-200 (if that's your dataset)
    num_classes = 200  # update this if needed
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model.to(device)
    model.eval()
    print("[Classifier] Model loaded.")
    return model

