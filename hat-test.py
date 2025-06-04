#!/usr/bin/env python3

import pantilthat
import time

def move_and_pause(pan_angle, tilt_angle, pause=1.0):
    print(f"Moving to pan: {pan_angle}°, tilt: {tilt_angle}°")
    pantilthat.servo_one(pan_angle)   # Pan (left/right)
    pantilthat.servo_two(tilt_angle)  # Tilt (up/down)
    time.sleep(pause)

def main():
    print("Starting Pan-Tilt test...")

    # Optional: calibrate pulse range if needed
    pantilthat.servo_pulse_min(1, 500)
    pantilthat.servo_pulse_max(1, 2500)
    pantilthat.servo_pulse_min(2, 500)
    pantilthat.servo_pulse_max(2, 2500)

    # Move to a few angles
    move_and_pause(-45, -30)
    move_and_pause(0, 0)
    move_and_pause(45, 30)

    # Return to center
    move_and_pause(0, 0, pause=0.5)

    # Disable servos
    pantilthat.servo_enable(1, False)
    pantilthat.servo_enable(2, False)
    print("Servos disabled. Test complete.")

if __name__ == "__main__":
    main()

