# motion_detector.py
import pantilthat

def detect_motion(threshold=0.2):
    """Read accelerometer values from the Pimoroni Pan-Tilt HAT.

    Returns ``True`` when the magnitude of acceleration deviates from 1g
    by more than ``threshold``.
    """
    x, y, z = pantilthat.get_accel()

    magnitude = (x**2 + y**2 + z**2)**0.5
    delta = abs(magnitude - 1.0)  # 1g is the baseline
    return delta > threshold
