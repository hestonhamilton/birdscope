# motion_detector.py
import pantilthat
import time

def detect_motion(threshold=0.2):
    """
    Reads tilt from Pimoroni Tilt HAT.
    Returns True if tilt exceeds threshold.
    """
    x = pantilthat.accel().x
    y = pantilthat.accel().y
    z = pantilthat.accel().z

    magnitude = (x**2 + y**2 + z**2)**0.5
    delta = abs(magnitude - 1.0)  # 1g is the baseline
    return delta > threshold
