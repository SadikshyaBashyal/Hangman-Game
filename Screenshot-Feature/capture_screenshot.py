"""
Automatic screenshot capture for the Hangman Game.
This script runs the game briefly and captures a screenshot.
"""

import pygame
import sys
import os
import time
from datetime import datetime
from constants import BACKGROUND
from ui_components import FontManager, ButtonManager, BackgroundRenderer, GameRenderer
from game_logic import GameLogic, InputHandler

def capture_game_screenshot():
    """Run the game briefly and capture a screenshot."""
    # Initialize Pygame
    pygame.init()
    
    # Create fullscreen window
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption('Hangman Game - Screenshot Capture')
    
    # Initialize components
    fonts = FontManager()
    game_logic = GameLogic()
    button_manager = ButtonManager(fonts, width, height)
    game_renderer = GameRenderer(fonts)
    input_handler = InputHandler()
    
    # Create screenshots directory
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    # Run game for a few frames to show it in action
    clock = pygame.time.Clock()
    frame_count = 0
    max_frames = 180  # 3 seconds at 60 FPS
    
    print("Capturing game screenshot...")
    print("Game will run for 3 seconds to show animations...")
    
    while frame_count < max_frames:
        # Clear screen and draw background
        screen.fill(BACKGROUND)
        BackgroundRenderer.draw_decorations(screen, width, height)
        
        # Handle events (minimal)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        # Draw all game elements
        game_renderer.draw(screen, game_logic, button_manager, width, height)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        
        # Capture screenshot at 2 seconds (120 frames)
        if frame_count == 120:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hangman_game_screenshot_{timestamp}.png"
            filepath = os.path.join("screenshots", filename)
            pygame.image.save(screen, filepath)
            print(f"Screenshot captured: {filepath}")
    
    # Clean up
    pygame.quit()
    print("Screenshot capture completed!")
    return os.path.join("screenshots", filename)

if __name__ == "__main__":
    try:
        screenshot_path = capture_game_screenshot()
        print(f"Successfully captured screenshot: {screenshot_path}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        sys.exit(1) 