"""
UI Components Module for Hangman Game
Contains all UI elements, buttons, and rendering functions.
"""

import pygame
import random
import math
import time
from constants import *

class FontManager:
    """Manages all fonts used in the game"""
    
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.word_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.button_font = pygame.font.SysFont("arial", 28)
        self.message_font = pygame.font.SysFont("arial", 36, bold=True)
        self.info_font = pygame.font.SysFont("arial", 22)


class HangmanRenderer:
    """Handles drawing the hangman figure"""
    
    @staticmethod
    def draw_hangman(surface, mistakes, width, height):
        center_x, center_y = width // 6, height // 3 - 20
        radius = 40

        # Draw gallows
        pygame.draw.line(surface, ACCENT, (center_x - 100, center_y + 200), 
                        (center_x + 100, center_y + 200), 8)
        pygame.draw.line(surface, ACCENT, (center_x, center_y + 200), 
                        (center_x, center_y - 150), 8)
        pygame.draw.line(surface, ACCENT, (center_x, center_y - 150), 
                        (center_x + 100, center_y - 150), 8)
        pygame.draw.line(surface, ACCENT, (center_x + 100, center_y - 150), 
                        (center_x + 100, center_y - 100), 8)

        if mistakes > 0:  # Head
            pygame.draw.circle(surface, TEXT_COLOR, (center_x + 100, center_y - 60), radius, 4)
            
        if mistakes > 1:  # Body
            pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y - 20), 
                           (center_x + 100, center_y + 60), 6)

        if mistakes > 2:  # Left Arm
            pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y), 
                           (center_x + 140, center_y - 30), 6)

        if mistakes > 3:  # Right Arm
            pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y), 
                           (center_x + 60, center_y - 30), 6)

        if mistakes > 4:  # Left Leg
            pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y + 60), 
                           (center_x + 60, center_y + 100), 6)

        if mistakes > 5:  # Right Leg
            pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y + 60), 
                           (center_x + 140, center_y + 100), 6)

        if mistakes > 6:  # Sad Face
            pygame.draw.arc(surface, TEXT_COLOR, (center_x + 80, center_y - 70, 40, 30), 
                           0, math.pi, 3)
            pygame.draw.circle(surface, TEXT_COLOR, (center_x + 85, center_y - 70), 3)
            pygame.draw.circle(surface, TEXT_COLOR, (center_x + 115, center_y - 70), 3)


class Button:
    """Represents a clickable button"""
    
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.visible = True
        self.clicked = False

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface, font):
        if not self.visible:
            return

        color = self.hover_color if self.is_hovered() and not self.clicked else self.color

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, ACCENT, self.rect, 3, border_radius=8)

        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered():
                self.clicked = True
                return True

        return False


class ButtonManager:
    """Manages all letter buttons"""
    
    def __init__(self, fonts, width, height):
        self.fonts = fonts
        self.width = width
        self.height = height
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        start_x = self.width // 2 + 50
        start_y = self.height // 2 - 80
        spacing = 45

        # Create A-Z buttons
        for i in range(26):
            letter = chr(65 + i)
            row = i // 9
            col = i % 9
            x = start_x + col * spacing
            y = start_y + row * spacing
            self.buttons.append(Button(x, y, 40, 40, letter))

    def reset_buttons(self):
        for button in self.buttons:
            button.visible = True
            button.clicked = False
            button.color = BUTTON_COLOR

    def update_button_states(self, guessed_letters, word):
        for button in self.buttons:
            letter = button.text
            if letter in guessed_letters:
                button.visible = False
                if letter not in word:
                    button.color = RED
                else:
                    button.color = GREEN

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface, self.fonts.button_font)

    def handle_events(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return button.text
        return None


class BackgroundRenderer:
    """Handles drawing the animated background"""
    
    @staticmethod
    def draw_decorations(surface, width, height):
        current_time = time.time()
        
        # Draw gently moving stars
        for i in range(100):
            
            # Use hash-based deterministic positioning
            base_x = hash(f"star_x_{i}") % width
            base_y = hash(f"star_y_{i}") % height
            
            x = base_x + int(10 * math.sin(current_time * 3.0 + i * 0.1))
            y = base_y + int(5 * math.cos(current_time * 2.5 + i * 0.05))
            
            # Use hash-based deterministic values for star properties
            size = 1 + (hash(f"star_size_{i}") % 3)  # Size between 1-3
            brightness = 150 + (hash(f"star_brightness_{i}") % 106)  # Brightness between 150-255
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)

        # Draw moon
        pygame.draw.circle(surface, (255, 255, 255), (width - 100, 100), 50)

        # Draw gently moving clouds
        
        cloud_positions = [(width - 300, 80), (width - 600, 120), (width - 900, 90)]
        for i, (base_x, base_y) in enumerate(cloud_positions):
            # Use deterministic positioning without affecting global random state
            x = base_x + int(20 * math.sin(current_time * 1.8 + i * 0.5))
            y = base_y + int(5 * math.sin(current_time * 1.5 + i * 0.3))
            
            # Use hash-based deterministic values for cloud properties
            size = 30 + (hash(f"cloud_{i}") % 31)  # Size between 30-60
            brightness = 150 + (hash(f"brightness_{i}") % 106)  # Brightness between 150-255
            pygame.draw.ellipse(surface, (brightness, brightness, brightness), (x, y, size, size * 0.8))

        # Draw border
        pygame.draw.rect(surface, ACCENT, (10, 10, width - 20, height - 20), 4, border_radius=10)


class GameRenderer:
    """Handles rendering all game elements"""
    
    def __init__(self, fonts):
        self.fonts = fonts

    def draw(self, surface, game_logic, button_manager, width, height):
        # Draw title
        title = self.fonts.title_font.render("Hangman Game", True, ACCENT)
        surface.blit(title, (width // 2 - title.get_width() // 2, 50))

        # Draw hangman
        HangmanRenderer.draw_hangman(surface, game_logic.mistakes, width, height)

        # Draw word display
        display_word = game_logic.get_display_word()
        word_surf = self.fonts.word_font.render(display_word, True, TEXT_COLOR)
        surface.blit(word_surf, (width // 2 - word_surf.get_width() // 2, height // 2 - 150))

        # Draw message
        if game_logic.message and game_logic.message_timer > 0:
            color = GREEN if 'Good' in game_logic.message or game_logic.game_state == "won" else RED
            msg_surf = self.fonts.message_font.render(game_logic.message, True, color)
            surface.blit(msg_surf, (width // 2 - msg_surf.get_width() // 2, height // 2 - 200))
            game_logic.message_timer -= 1

        # Draw game state message
        if game_logic.game_state == "won":
            msg = self.fonts.message_font.render('You Won! Press SPACE to play again', True, GREEN)
            surface.blit(msg, (width // 2 - msg.get_width() // 2, height - 100))
        elif game_logic.game_state == "lost":
            msg = self.fonts.message_font.render('You Lost! Press SPACE to play again', True, RED)
            surface.blit(msg, (width // 2 - msg.get_width() // 2, height - 100))
        else:
            msg = self.fonts.info_font.render(f"Mistakes: {game_logic.mistakes}/{MAX_MISTAKES}", True, TEXT_COLOR)
            surface.blit(msg, (width // 2 - msg.get_width() // 2, height - 100))

        # Draw buttons
        button_manager.update_button_states(game_logic.guessed_letters, game_logic.word)
        button_manager.draw(surface)

        # Draw instructions
        self.draw_instructions(surface, width, height)

    def draw_instructions(self, surface, width, height):
        instructions = [
            "How to Play:",
            "1. Guess the letter by clicking the buttons or typing",
            "2. You have 7 incorrect guesses allowed",
            "3. Try to guess the word before the man is hanged"
        ]

        for i, text in enumerate(instructions):
            y_pos = height - 150 - (len(instructions) - 1 - i) * 30
            color = LIGHT_BLUE if i > 0 else ACCENT
            instr = self.fonts.info_font.render(text, True, color)
            surface.blit(instr, (width // 2 - 200, y_pos)) 