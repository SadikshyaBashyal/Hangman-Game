import pygame
import sys
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 0, 0  # Will be set dynamically
BACKGROUND = (25, 35, 55)
ACCENT = (255, 215, 0)
TEXT_COLOR = (240, 240, 250)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
BUTTON_ACTIVE = (50, 120, 170)
RED = (220, 60, 60)
GREEN = (70, 180, 70)
LIGHT_BLUE = (100, 180, 255)
DARK_BLUE = (40, 60, 100)

# Game Words
WORDS = ["PYTHON", "PROGRAMMING", "DEVELOPMENT", "FRAMEWORK", "ALGORITHM", "APPLICATION", 
         "OPERATING", "SYSTEM", "DATABASE", "NETWORK", "SECURITY", "INFORMATION", 
         "COMPUTER", "PROGRAM", "CODE", "DESIGN", "ENGINEERING", "SCIENCE", 
         "TECHNOLOGY", "INNOVATION", "CREATIVITY", "SOLUTION", "PROCESS", "ANALYSIS"]


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
    def draw_hangman(surface, mistakes):
        center_x, center_y = WIDTH // 6, HEIGHT // 3 - 20
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
    
    def __init__(self, fonts):
        self.fonts = fonts
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        start_x = WIDTH // 2 + 50
        start_y = HEIGHT // 2 - 80
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
    def draw_decorations(surface):
        current_time = time.time()
        
        # Draw gently moving stars
        for i in range(100):
            random.seed(i)
            base_x = random.randint(0, WIDTH)
            base_y = random.randint(0, HEIGHT)
            
            x = base_x + int(10 * math.sin(current_time * 3.0 + i * 0.1))
            y = base_y + int(5 * math.cos(current_time * 2.5 + i * 0.05))
            
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)

        # Draw moon
        pygame.draw.circle(surface, (255, 255, 255), (WIDTH - 100, 100), 50)

        # Draw gently moving clouds
        cloud_positions = [(WIDTH - 300, 80), (WIDTH - 600, 120), (WIDTH - 900, 90)]
        for i, (base_x, base_y) in enumerate(cloud_positions):
            x = base_x + int(20 * math.sin(current_time * 1.8 + i * 0.5))
            y = base_y + int(5 * math.sin(current_time * 1.5 + i * 0.3))
            
            size = random.randint(30, 60)
            brightness = random.randint(150, 255)
            pygame.draw.ellipse(surface, (brightness, brightness, brightness), (x, y, size, size * 0.8))

        # Draw border
        pygame.draw.rect(surface, ACCENT, (10, 10, WIDTH - 20, HEIGHT - 20), 4, border_radius=10)


class GameLogic:
    """Handles the core game logic"""
    
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.mistakes = 0
        self.game_state = "playing"
        self.message = ""
        self.message_timer = 0

    def guess_letter(self, letter):
        if letter in self.guessed_letters or self.game_state != "playing":
            return

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.mistakes += 1
            self.message = f"'{letter}' is not in the word"
            self.message_timer = 60

            if self.mistakes >= 7:
                self.game_state = "lost"
                self.message = "You lost! The word was: " + self.word
        else:
            self.message = f"Good! '{letter}' is in the word!"
            self.message_timer = 60
            
        # Check if player has won (after every guess)
        if all(char in self.guessed_letters for char in self.word):
            self.game_state = "won"
            self.message = "Congratulations! You won!"

    def get_display_word(self):
        display_word = ""
        for char in self.word:
            if char in self.guessed_letters or self.game_state == "lost":
                display_word += char + " "
            else:
                display_word += "_ "
        return display_word

    def is_game_over(self):
        return self.game_state in ["won", "lost"]


class GameRenderer:
    """Handles rendering all game elements"""
    
    def __init__(self, fonts):
        self.fonts = fonts

    def draw(self, surface, game_logic, button_manager):
        # Draw title
        title = self.fonts.title_font.render("Hangman Game", True, ACCENT)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw hangman
        HangmanRenderer.draw_hangman(surface, game_logic.mistakes)

        # Draw word display
        display_word = game_logic.get_display_word()
        word_surf = self.fonts.word_font.render(display_word, True, TEXT_COLOR)
        surface.blit(word_surf, (WIDTH // 2 - word_surf.get_width() // 2, HEIGHT // 2 - 150))

        # Draw message
        if game_logic.message and game_logic.message_timer > 0:
            color = GREEN if 'Good' in game_logic.message or game_logic.game_state == "won" else RED
            msg_surf = self.fonts.message_font.render(game_logic.message, True, color)
            surface.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2 - 200))
            game_logic.message_timer -= 1

        # Draw game state message
        if game_logic.game_state == "won":
            msg = self.fonts.message_font.render('You Won! Press SPACE to play again', True, GREEN)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))
        elif game_logic.game_state == "lost":
            msg = self.fonts.message_font.render('You Lost! Press SPACE to play again', True, RED)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))
        else:
            msg = self.fonts.info_font.render(f"Mistakes: {game_logic.mistakes}/7", True, TEXT_COLOR)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))

        # Draw buttons
        button_manager.update_button_states(game_logic.guessed_letters, game_logic.word)
        button_manager.draw(surface)

        # Draw instructions
        self.draw_instructions(surface)

    def draw_instructions(self, surface):
        instructions = [
            "How to Play:",
            "1. Guess the letter by clicking the buttons or typing",
            "2. You have 7 incorrect guesses allowed",
            "3. Try to guess the word before the man is hanged"
        ]

        for i, text in enumerate(instructions):
            y_pos = HEIGHT - 150 - i * 30
            color = LIGHT_BLUE if i > 0 else ACCENT
            instr = self.fonts.info_font.render(text, True, color)
            surface.blit(instr, (WIDTH // 2 - 200, y_pos))


class InputHandler:
    """Handles all input events"""
    
    @staticmethod
    def handle_events(event, game_logic, button_manager):
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_logic.is_game_over():
                return "reset"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.unicode.isalpha() and game_logic.game_state == "playing":
                letter = event.unicode.upper()
                if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    game_logic.guess_letter(letter)
        
        # Handle button clicks
        button_letter = button_manager.handle_events(event)
        if button_letter:
            game_logic.guess_letter(button_letter)
        
        return "continue"


class Game:
    """Main game class that coordinates all components"""
    
    def __init__(self):
        global WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WIDTH, HEIGHT = self.screen.get_size()
        pygame.display.set_caption('Hangman Game')
        
        self.clock = pygame.time.Clock()
        self.fonts = FontManager()
        self.game_logic = GameLogic()
        self.button_manager = ButtonManager(self.fonts)
        self.game_renderer = GameRenderer(self.fonts)
        self.input_handler = InputHandler()

    def reset_game(self):
        self.game_logic.reset_game()
        self.button_manager.reset_buttons()

    def run(self):
        running = True
        while running:
            self.screen.fill(BACKGROUND)
            BackgroundRenderer.draw_decorations(self.screen)

            for event in pygame.event.get():
                result = self.input_handler.handle_events(event, self.game_logic, self.button_manager)
                
                if result == "quit":
                    running = False
                elif result == "reset":
                    self.reset_game()

            # Draw game elements
            self.game_renderer.draw(self.screen, self.game_logic, self.button_manager)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()