"""
Screenshot utility for capturing game screenshots.
Run this after starting the game to capture a screenshot.
"""

import pygame
import os
from datetime import datetime

def capture_screenshot(surface, filename=None):
    """
    Capture a screenshot of the current game screen.
    
    Args:
        surface: Pygame surface to capture
        filename: Optional filename, defaults to timestamp
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hangman_game_{timestamp}.png"
    
    # Create screenshots directory if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    # Save the screenshot
    filepath = os.path.join("screenshots", filename)
    pygame.image.save(surface, filepath)
    print(f"Screenshot saved as: {filepath}")
    return filepath

def capture_game_screenshot():
    """Capture a screenshot of the running game."""
    # Initialize Pygame if not already done
    if not pygame.get_init():
        pygame.init()
    
    # Get the current display surface
    surface = pygame.display.get_surface()
    if surface:
        return capture_screenshot(surface)
    else:
        print("No active display surface found. Make sure the game is running.")
        return None

if __name__ == "__main__":
    print("Screenshot utility for Hangman Game")
    print("Run this while the game is running to capture a screenshot.")
    print("Press any key to capture screenshot...")
    
    # Wait for key press
    input()
    
    # Capture screenshot
    result = capture_game_screenshot()
    if result:
        print(f"Screenshot captured successfully: {result}")
    else:
        print("Failed to capture screenshot.") 