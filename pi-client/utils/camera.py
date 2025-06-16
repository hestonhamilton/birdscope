# pi-client/camera.py

from picamera2 import Picamera2, Preview
import cv2
import time

class PiCameraCapture:
    """
    Manages image capture from the Raspberry Pi Camera Module v2 using Picamera2.
    """

    def __init__(self, resolution=(640, 480), flip_horizontal=True, flip_vertical=True):
        """
        Initializes the camera with a specified resolution and optional flipping.

        Parameters:
            resolution (tuple): Desired resolution (width, height) for image capture.
            flip_horizontal (bool): Whether to flip the captured image horizontally.
            flip_vertical (bool): Whether to flip the captured image vertically.
        """
        self.camera = None
        self.resolution = resolution
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical

        try:
            self.camera = Picamera2()
            # Create a still configuration for capturing high-resolution images
            # or a preview configuration for faster, lower-res grabs
            # Using preview_configuration for general purpose captures as discussed for streaming
            camera_config = self.camera.create_preview_configuration(
                main={"size": resolution, "format": "RGB888"} # Capture in RGB format
            )
            self.camera.configure(camera_config)
            self.camera.start()
            # Allow camera to warm up
            time.sleep(1)
            print(f"PiCamera2 initialized at {resolution[0]}x{resolution[1]}.")
            if flip_horizontal or flip_vertical:
                print(f"Camera feed configured with flip: Horizontal={flip_horizontal}, Vertical={flip_vertical}")

        except Exception as e:
            print(f"Error initializing PiCamera2: {e}")
            self.camera = None # Indicate camera failure

    def capture_frame(self):
        """
        Captures a single frame from the camera as a NumPy array.
        Applies configured flipping.

        Returns:
            numpy.ndarray: The captured image frame (RGB format), or None if camera is not initialized or capture fails.
        """
        if self.camera is None:
            print("Camera is not initialized. Cannot capture frame.")
            return None
        try:
            # Capture as a NumPy array
            frame = self.camera.capture_array() # This returns an array in RGB888 as configured
            
            # Apply flipping if configured
            flip_code = 0 # Default no flip
            if self.flip_horizontal and self.flip_vertical:
                flip_code = -1 # Both axes
            elif self.flip_horizontal:
                flip_code = 1  # Horizontal only
            elif self.flip_vertical:
                flip_code = 0  # Vertical only (this is already set by default above if no flip)

            if flip_code != 0: # Only flip if a flip is actually required
                frame = cv2.flip(frame, flip_code)

            return frame
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None

    def stop(self):
        """
        Stops the camera preview and releases resources.
        """
        if self.camera:
            try:
                self.camera.stop()
                self.camera.close()
                print("PiCamera2 stopped and resources released.")
            except Exception as e:
                print(f"Error stopping PiCamera2: {e}")

# Example Usage (for testing this file independently)
if __name__ == "__main__":
    camera_capture = PiCameraCapture(resolution=(1280, 720), flip_horizontal=True, flip_vertical=True) # Higher resolution for still capture if desired

    if camera_capture.is_initialized():
        print("Capturing a test image in 2 seconds...")
        time.sleep(2)
        frame = camera_capture.capture_frame()

        if frame is not None:
            print(f"Captured frame with shape: {frame.shape}, dtype: {frame.dtype}")
            # Save the captured frame to a file for verification
            # Convert RGB to BGR for OpenCV saving
            cv2.imwrite("test_capture_flipped.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print("Test image saved as test_capture_flipped.jpg")
        else:
            print("Failed to capture image.")

    camera_capture.stop()
    print("Camera test complete.")

