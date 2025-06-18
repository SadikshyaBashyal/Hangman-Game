"""
Main Game Module for Hangman Game
Coordinates all components and runs the main game loop.
"""

import pygame
import sys
import os
from datetime import datetime
from constants import BACKGROUND
from ui_components import FontManager, ButtonManager, BackgroundRenderer, GameRenderer
from game_logic import GameLogic, InputHandler

class Game:
    """Main game class that coordinates all components"""
    
    def __init__(self):
        """Initialize the game with all components."""
        # Initialize Pygame
        pygame.init()
        
        # Create fullscreen window and get dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption('Hangman Game')
        
        # Initialize game components
        self.clock = pygame.time.Clock()
        self.fonts = FontManager()
        self.game_logic = GameLogic()
        self.button_manager = ButtonManager(self.fonts, self.width, self.height)
        self.game_renderer = GameRenderer(self.fonts)
        self.input_handler = InputHandler()

    def reset_game(self):
        """Reset the game to start a new round."""
        self.game_logic.reset_game()
        self.button_manager.reset_buttons()

    def capture_screenshot(self):
        """Capture a screenshot of the current game state."""
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hangman_game_{timestamp}.png"
        filepath = os.path.join("screenshots", filename)
        
        # Save the screenshot
        pygame.image.save(self.screen, filepath)
        print(f"Screenshot saved as: {filepath}")
        return filepath

    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Clear screen and draw background
            self.screen.fill(BACKGROUND)
            BackgroundRenderer.draw_decorations(self.screen, self.width, self.height)

            # Handle events
            for event in pygame.event.get():
                result = self.input_handler.handle_events(event, self.game_logic, self.button_manager)
                
                if result == "quit":
                    running = False
                elif result == "reset":
                    self.reset_game()
                
                # Handle screenshot capture
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F12:  # F12 key for screenshot
                        self.capture_screenshot()

            # Draw all game elements
            self.game_renderer.draw(self.screen, self.game_logic, self.button_manager, self.width, self.height)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)

        # Clean up
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main() 