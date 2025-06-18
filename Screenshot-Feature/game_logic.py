"""
Game Logic Module for Hangman Game
Contains the core game mechanics and state management.
"""

import pygame
import random
from constants import WORDS, MAX_MISTAKES, MESSAGE_DISPLAY_TIME

class GameLogic:
    """Handles the core game logic including word selection, letter guessing,
    win/lose conditions, and game state management."""
    
    def __init__(self):
        """Initialize game logic and start a new game."""
        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state with a new word."""
        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.mistakes = 0
        self.game_state = "playing"  # "playing", "won", or "lost"
        self.message = ""
        self.message_timer = 0

    def guess_letter(self, letter):
        """Process a letter guess and update game state accordingly.
        
        Args:
            letter: The letter being guessed (uppercase)
        """
        # Ignore if letter already guessed or game is over
        if letter in self.guessed_letters or self.game_state != "playing":
            return

        self.guessed_letters.add(letter)

        if letter not in self.word:
            # Wrong guess
            self.mistakes += 1
            self.message = f"'{letter}' is not in the word"
            self.message_timer = MESSAGE_DISPLAY_TIME

            # Check if game is lost
            if self.mistakes >= MAX_MISTAKES:
                self.game_state = "lost"
                self.message = "You lost! The word was: " + self.word
        else:
            # Correct guess
            self.message = f"Good! '{letter}' is in the word!"
            self.message_timer = MESSAGE_DISPLAY_TIME
            
        # Check if player has won (after every guess)
        if all(char in self.guessed_letters for char in self.word):
            self.game_state = "won"
            self.message = "Congratulations! You won!"

    def get_display_word(self):
        """Get the word display string with underscores for unguessed letters.
        
        Returns:
            String representation of the word with underscores and spaces
        """
        display_word = ""
        for char in self.word:
            if char in self.guessed_letters or self.game_state == "lost":
                display_word += char + " "  # Show letter if guessed or game over
            else:
                display_word += "_ "        # Show underscore if not guessed
        return display_word

    def is_game_over(self):
        """Check if the game is in a terminal state.
        
        Returns:
            True if game is won or lost, False otherwise
        """
        return self.game_state in ["won", "lost"]


class InputHandler:
    """Handles all input events including keyboard and mouse input.
    Processes user interactions and returns appropriate actions."""
    
    @staticmethod
    def handle_events(event, game_logic, button_manager):
        """Process a single event and return the appropriate action.
        
        Args:
            event: Pygame event to process
            game_logic: GameLogic instance
            button_manager: ButtonManager instance
            
        Returns:
            String indicating the action: "quit", "reset", or "continue"
        """
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.KEYDOWN:
            # Handle keyboard input
            if event.key == pygame.K_SPACE and game_logic.is_game_over():
                return "reset"  # Restart game if won/lost
            elif event.key == pygame.K_ESCAPE:
                return "quit"   # Exit game
            elif event.unicode.isalpha() and game_logic.game_state == "playing":
                # Handle letter input
                letter = event.unicode.upper()
                if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    game_logic.guess_letter(letter)
        
        # Handle button clicks
        button_letter = button_manager.handle_events(event)
        if button_letter:
            game_logic.guess_letter(button_letter)
        
        return "continue" 