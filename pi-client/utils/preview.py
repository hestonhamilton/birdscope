# tilt_utils.py

import pantilthat
import time

class PanTiltHelper:
    """
    A helper class to manage the Pan-Tilt HAT for bird recording.
    Wraps pantilthat library functions for easier use in a project.
    LED functionalities are explicitly turned off during initialization.
    """

    def __init__(self, idle_timeout=2,
                 servo1_min=575, servo1_max=2325,
                 servo2_min=575, servo2_max=2325,
                 address=21, i2c_bus=None):
        """
        Initializes the PanTiltHAT. LEDs are disabled by setting enable_lights=False.

        Parameters:
            idle_timeout (int): Time in seconds after which servos automatically disable. 
            servo1_min (int): Minimum high pulse for servo 1 in microseconds. 
            servo1_max (int): Maximum high pulse for servo 1 in microseconds. 
            servo2_min (int): Minimum high pulse for servo 2 in microseconds. 
            servo2_max (int): Maximum high pulse for servo 2 in microseconds. 
            address (int): I2C address of the PanTiltHAT. 
            i2c_bus (int): I2C bus number. 
        """
        try:
            # Explicitly set enable_lights to False to ensure LEDs are off
            self.pt = pantilthat.PanTilt(
                enable_lights=False, # LEDs are OFF for bird-watching
                idle_timeout=idle_timeout,
                servo1_min=servo1_min,
                servo1_max=servo1_max,
                servo2_min=servo2_min,
                servo2_max=servo2_max,
                address=address,
                i2c_bus=i2c_bus
            )
            print("Pan-Tilt HAT initialized successfully with LEDs disabled.")
        except Exception as e:
            print(f"Error initializing Pan-Tilt HAT: {e}")
            self.pt = None # Indicate that initialization failed

    def is_initialized(self):
        """Checks if the Pan-Tilt HAT was successfully initialized."""
        return self.pt is not None

    def set_pan_angle(self, angle):
        """
        Sets the horizontal (pan) angle of the Pan-Tilt HAT in degrees. 

        Parameters:
            angle (int/float): Angle in degrees from -90 to 90. 
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot set pan angle.")
            return

        if not (-90 <= angle <= 90):
            print(f"Warning: Pan angle {angle} is out of typical range (-90 to 90 degrees).")
        try:
            self.pt.pan(angle) [cite: 22]
            # print(f"Pan set to {angle} degrees.")
        except Exception as e:
            print(f"Error setting pan angle: {e}")

    def set_tilt_angle(self, angle):
        """
        Sets the vertical (tilt) angle of the Pan-Tilt HAT in degrees. 

        Parameters:
            angle (int/float): Angle in degrees from -90 to 90. 
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot set tilt angle.")
            return

        if not (-90 <= angle <= 90):
            print(f"Warning: Tilt angle {angle} is out of typical range (-90 to 90 degrees).")
        try:
            self.pt.tilt(angle) [cite: 25]
            # print(f"Tilt set to {angle} degrees.")
        except Exception as e:
            print(f"Error setting tilt angle: {e}")

    def get_current_pan_angle(self):
        """
        Retrieves the current pan angle in degrees. 

        Returns:
            float: Current pan angle, or None if not initialized.
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot get pan angle.")
            return None
        try:
            return self.pt.get_pan() [cite: 23]
        except Exception as e:
            print(f"Error getting pan angle: {e}")
            return None

    def get_current_tilt_angle(self):
        """
        Retrieves the current tilt angle in degrees. 

        Returns:
            float: Current tilt angle, or None if not initialized.
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot get tilt angle.")
            return None
        try:
            return self.pt.get_tilt() [cite: 26]
        except Exception as e:
            print(f"Error getting tilt angle: {e}")
            return None

    def enable_servo(self, servo_index, state):
        """
        Enables or disables a specific servo.  Disabling a servo turns off the drive signal. 
        It's good practice to do this if you don't want the Pan/Tilt to point in a certain direction and instead want to save power. 

        Parameters:
            servo_index (int): Servo index: either 1 or 2. 
            state (bool): Servo state: True = on, False = off. 
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot enable/disable servo.")
            return

        if servo_index not in [1, 2]:
            print("Invalid servo index. Use 1 for pan or 2 for tilt.")
            return

        try:
            self.pt.servo_enable(servo_index, state) [cite: 28]
            # print(f"Servo {servo_index} {'enabled' if state else 'disabled'}.")
        except Exception as e:
            print(f"Error setting servo enable state: {e}")

    def set_servo_idle_timeout(self, seconds):
        """
        Configures the time, in seconds, after which the servos will be automatically disabled. 

        Parameters:
            seconds (int): Timeout in seconds. 
        """
        if not self.is_initialized():
            print("Pan-Tilt HAT not initialized. Cannot set idle timeout.")
            return

        try:
            self.pt.idle_timeout(seconds) [cite: 32]
            print(f"Servo idle timeout set to {seconds} seconds.")
        except Exception as e:
            print(f"Error setting idle timeout: {e}")

# Example Usage (for testing or integrating into your main bird-watching script):
if __name__ == "__main__":
    # Initialize PanTiltHelper with LEDs disabled by default (due to enable_lights=False in __init__)
    pt_helper = PanTiltHelper(idle_timeout=5)

    if pt_helper.is_initialized():
        # Example motion sequence:
        print("\nMoving pan-tilt...")
        pt_helper.set_pan_angle(45)
        pt_helper.set_tilt_angle(30)
        time.sleep(1)

        print(f"Current Pan: {pt_helper.get_current_pan_angle()} degrees")
        print(f"Current Tilt: {pt_helper.get_current_tilt_angle()} degrees")

        pt_helper.set_pan_angle(-45)
        pt_helper.set_tilt_angle(-30)
        time.sleep(1)

        print(f"Current Pan: {pt_helper.get_current_pan_angle()} degrees")
        print(f"Current Tilt: {pt_helper.get_current_tilt_angle()} degrees")

        # Disable servos to save power after movement
        pt_helper.enable_servo(1, False)
        pt_helper.enable_servo(2, False)
        print("Servos disabled.")

    else:
        print("Pan-Tilt HAT could not be initialized. Check connections and software.")