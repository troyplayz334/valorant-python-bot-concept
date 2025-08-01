import pyautogui
import time
import keyboard
from PIL import ImageGrab

# Configuration
SCAN_RADIUS = 5            # Pixels around crosshair to check (1-10)
REACTION_TIME = 0.05       # Seconds between detection and key press (0.01-0.5)
SCAN_INTERVAL = 0.01       # Seconds between scans (0.001-0.1)
PRESS_DURATION = 0.1       # How long to press the 'k' key (0.01-0.3)

# Purple color detection settings
PURPLE_R_MIN = 120         # Minimum red value for purple
PURPLE_R_MAX = 255         # Maximum red value for purple
PURPLE_G_MIN = 0           # Minimum green value for purple
PURPLE_G_MAX = 100         # Maximum green value for purple
PURPLE_B_MIN = 120         # Minimum blue value for purple
PURPLE_B_MAX = 255         # Maximum blue value for purple

# Crosshair position (center of screen)
screen_width, screen_height = pyautogui.size()
crosshair_x = screen_width // 2
crosshair_y = screen_height // 2

def is_purple(pixel):
    """Check if a pixel is in the purple range"""
    r, g, b = pixel
    return (PURPLE_R_MIN <= r <= PURPLE_R_MAX and
            PURPLE_G_MIN <= g <= PURPLE_G_MAX and
            PURPLE_B_MIN <= b <= PURPLE_B_MAX)

def press_k():
    """Simulate pressing the 'k' key"""
    keyboard.press('k')
    time.sleep(PRESS_DURATION)
    keyboard.release('k')

def main():
    print("Purple Trigger bot started. Hold Left Shift to activate.")
    print("When purple is detected, the bot will press 'k'.")
    print("Press 'q' to quit.")
    
    running = True
    active = False
    
    while running:
        if keyboard.is_pressed('q'):
            running = False
            print("Exiting trigger bot...")
            break
            
        # Check shift key state
        if keyboard.is_pressed('shift'):
            if not active:
                active = True
                print("Trigger bot activated")
            
            # Capture screen around crosshair
            screenshot = ImageGrab.grab(bbox=(
                crosshair_x - SCAN_RADIUS,
                crosshair_y - SCAN_RADIUS,
                crosshair_x + SCAN_RADIUS,
                crosshair_y + SCAN_RADIUS
            ))
            
            # Check pixels for purple color
            for x in range(SCAN_RADIUS * 2):
                for y in range(SCAN_RADIUS * 2):
                    pixel = screenshot.getpixel((x, y))
                    if is_purple(pixel):
                        time.sleep(REACTION_TIME)  # Reaction delay
                        press_k()
                        time.sleep(0.1)  # Cooldown to prevent rapid repeats
                        break  # Exit after first detection
        else:
            if active:
                active = False
                print("Trigger bot deactivated")
        
        time.sleep(SCAN_INTERVAL)  # Reduce CPU usage

if __name__ == "__main__":
    main()