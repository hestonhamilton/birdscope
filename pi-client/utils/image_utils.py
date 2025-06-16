# pi-client/utils/image_utils.py

import cv2
import numpy as np

def encode_image_to_jpeg(image_array, quality=90):
    """
    Encodes a NumPy image array (RGB or BGR) into JPEG bytes.

    Parameters:
        image_array (numpy.ndarray): The input image as a NumPy array (e.g., from PiCamera2).
                                     Expected format is typically RGB (from Picamera2 capture_array)
                                     or BGR (if processed by OpenCV before this).
        quality (int): JPEG compression quality from 0 (worst) to 100 (best).

    Returns:
        bytes: The JPEG encoded image bytes, or None if encoding fails.
    """
    if image_array is None:
        print("Warning: Attempted to encode a None image array.")
        return None

    # OpenCV imencode expects BGR format for standard JPEG encoding.
    # Picamera2's capture_array() with format="RGB888" yields RGB.
    # So, we should convert from RGB to BGR before encoding.
    if len(image_array.shape) == 3 and image_array.shape[2] == 3: # Check if it's a 3-channel image
        # Assume input is RGB from Picamera2, convert to BGR for OpenCV
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    else:
        # If it's already grayscale or some other format, or already BGR, use directly
        image_bgr = image_array

    try:
        # Encode the image to JPEG bytes
        # The quality parameter is passed as part of a list for imencode
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        success, buffer = cv2.imencode('.jpg', image_bgr, encode_param)

        if success:
            return buffer.tobytes()
        else:
            print("Error: Could not encode image to JPEG.")
            return None
    except Exception as e:
        print(f"Error during JPEG encoding: {e}")
        return None

def decode_jpeg_to_image(jpeg_bytes):
    """
    Decodes JPEG bytes back into a NumPy image array (BGR format).

    Parameters:
        jpeg_bytes (bytes): The JPEG encoded image bytes.

    Returns:
        numpy.ndarray: The decoded image as a NumPy array (BGR format), or None if decoding fails.
    """
    if jpeg_bytes is None:
        print("Warning: Attempted to decode None JPEG bytes.")
        return None
    try:
        # Convert bytes to a numpy array for cv2.imdecode
        np_arr = np.frombuffer(jpeg_bytes, np.uint8)
        image_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # IMREAD_COLOR for 3-channel BGR

        if image_array is None:
            print("Error: Could not decode JPEG bytes.")
            return None
        return image_array
    except Exception as e:
        print(f"Error during JPEG decoding: {e}")
        return None

# Example Usage (for testing this file independently)
if __name__ == "__main__":
    # Create a dummy image (e.g., a simple colored square) for testing
    dummy_image_rgb = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(dummy_image_rgb, (100, 100), (300, 300), (255, 0, 0), -1) # Blue square
    cv2.putText(dummy_image_rgb, "Test Image", (350, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Green text

    print("Encoding dummy image...")
    jpeg_bytes = encode_image_to_jpeg(dummy_image_rgb, quality=85)

    if jpeg_bytes:
        print(f"Encoded JPEG bytes length: {len(jpeg_bytes)} bytes")
        # Save to file to verify
        with open("dummy_encoded.jpg", "wb") as f:
            f.write(jpeg_bytes)
        print("Dummy encoded image saved as dummy_encoded.jpg")

        print("Decoding dummy image...")
        decoded_image_bgr = decode_jpeg_to_image(jpeg_bytes)

        if decoded_image_bgr is not None:
            print(f"Decoded image shape: {decoded_image_bgr.shape}, dtype: {decoded_image_bgr.dtype}")
            cv2.imwrite("dummy_decoded.jpg", decoded_image_bgr)
            print("Dummy decoded image saved as dummy_decoded.jpg")
        else:
            print("Failed to decode image.")
    else:
        print("Failed to encode image.")


