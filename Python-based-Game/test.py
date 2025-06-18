import pygame
import sys
import random
import math

pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption('Hangman Game')

# Colors
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


# Fonts
title_font = pygame.font.SysFont("arial", 48, bold = True)
word_font = pygame.font.SysFont("consolas", 42, bold = True)
button_font = pygame.font.SysFont("arial", 28)
message_font = pygame.font.SysFont("arial", 36, bold = True)
info_font = pygame.font.SysFont("arial", 22)


# Game Words
WORDS = ["PYTHON", "PROGRAMMING", "DEVELOPMENT", "FRAMEWORK", "ALGORITHM", "APPLICATION", "OPERATING", "SYSTEM", "DATABASE", "NETWORK", "SECURITY", "INFORMATION", "COMPUTER", "PROGRAM", "CODE", "DESIGN", "ENGINEERING", "SCIENCE", "TECHNOLOGY", "INNOVATION", "CREATIVITY", "SOLUTION", "PROCESS", "ANALYSIS",]


# Hangman drawing function

def draw_hangman(surface, mistakes):
    center_x, center_y = WIDTH // 6, HEIGHT // 3 - 20
    radius = 40

    # Draw gallows
    pygame.draw.line(surface, ACCENT, (center_x - 100, center_y + 200), (center_x + 100, center_y+ 200), 8)
    pygame.draw.line(surface, ACCENT, (center_x, center_y + 200), (center_x, center_y - 150), 8)
    pygame.draw.line(surface, ACCENT, (center_x, center_y - 150), (center_x + 100, center_y - 150), 8)
    pygame.draw.line(surface, ACCENT, (center_x + 100, center_y - 150), (center_x + 100, center_y - 100), 8)

    if mistakes > 0: # Head
        pygame.draw.circle(surface, TEXT_COLOR, (center_x + 100, center_y - 60), radius, 4)
        
    if mistakes > 1: # Body
        pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y - 20), (center_x + 100, center_y + 60), 6)

    if mistakes > 2: # Left Arm
        pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y), (center_x + 140, center_y - 30), 6)

    if mistakes > 3: # Right Arm
        pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y), (center_x + 60, center_y - 30), 6)

    if mistakes > 4: # Left Leg
        pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y + 60), (center_x + 60, center_y + 100), 6)

    if mistakes > 5: # Right Leg
        pygame.draw.line(surface, TEXT_COLOR, (center_x + 100, center_y + 60), (center_x + 140, center_y + 100), 6)

    if mistakes > 6: # Sad Face
        pygame.draw.arc(surface, TEXT_COLOR, (center_x + 80, center_y - 70, 40, 30), 0, math.pi, 3)

        pygame.draw.circle(surface, TEXT_COLOR, (center_x + 85, center_y - 70), 3)
        pygame.draw.circle(surface, TEXT_COLOR, (center_x + 115, center_y - 70), 3)


# Button Class for letter buttons
class Button:
    def __init__(self, x, y, width, height, text, color = BUTTON_COLOR, hover_color = BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.visible = True
        self.clicked = False

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        if not self.visible:
            return

        color = self.hover_color if self.is_hovered() and not self.clicked else self.color

        pygame.draw.rect(surface, color, self.rect, border_radius = 8)
        pygame.draw.rect(surface, ACCENT, self.rect, 3, border_radius = 8)

        text_surf = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center = self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered():
                self.clicked = True
                return True

        return False


# Game Class
class HangmanGame:
    def __init__(self) -> None:
        self.buttons = []
        self.create_buttons()
        self.reset_game()
        self.message = ""
        self.message_timer = 0

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.mistakes = 0
        self.game_state = "playing"
        self.message = ""
        self.message_timer = 0
        
        # Reset all buttons to initial state
        for button in self.buttons:
            button.visible = True
            button.clicked = False
            button.color = BUTTON_COLOR

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

            
                # Check if player has won
                if all(char in self.guessed_letters for char in self.word):
                    self.game_state = "won"
                    self.message = "Congratulations! You won!"

    def draw(self, surface):
        # Draw title
        title = title_font.render("Hangman Game", True, ACCENT)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw hangman
        draw_hangman(surface, self.mistakes)

        # Draw word display

        display_word = ""
        for char in self.word:
            if char in self.guessed_letters or self.game_state == "lost":
                display_word += char + " "
            else:
                display_word += "_ "

        word_surf = word_font.render(display_word, True, TEXT_COLOR)
        surface.blit(word_surf, (WIDTH // 2 - word_surf.get_width() // 2, HEIGHT // 2 - 150))

        # Draw message
        if self.message and self.message_timer > 0:
            color = GREEN if 'Good' in self.message or "won" in self.game_state else RED
            msg_surf = message_font.render(self.message, True, color)
            surface.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2 - 200))
            self.message_timer -= 1

        # Draw game state message
        if self.game_state == "won":
            msg = message_font.render('You Won! Press SPACE to play again', True, GREEN)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))

        elif self.game_state == "lost":
            msg = message_font.render('You Lost! Press SPACE to play again', True, RED)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))

        else:
            msg = info_font.render(f"Misktakes: {self.mistakes}/7", True, TEXT_COLOR)
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))

        # Draw buttons
        for button in self.buttons:
            letter = button.text
            if letter in self.guessed_letters:
                button.visible = False
                if letter not in self.word:
                    button.color = GREEN
                else:
                    button.color = RED

            button.draw(surface)

        instruction = [
            "How to Play:",
            "1. Guess the letter by clicking the buttons",
            "2. You have 7 incorrect guesses allowed",
            "3. Try to guess the word before the man is hanged"
        ]

        for i, text in enumerate(instruction):
            y_pos = HEIGHT - 100 - i * 30
            instr = info_font.render(text, True, LIGHT_BLUE if i > 0 else ACCENT)
            surface.blit(instr, (WIDTH // 2 - 200, y_pos))

# Main Game Loop
def main():
    game = HangmanGame()
    clock = pygame.time.Clock()

    # Draw Decorative elements
    def draw_decorations():
        # Draw stars on the background
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

        # Draw moon
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH - 100, 100), 50)

        # Draw clouds
        for _ in range(3):
            x = random.randint(0, WIDTH)
            y = random.randint(50, 150)
            size = random.randint(30, 60)
            brightness = random.randint(150, 255)
            pygame.draw.ellipse(screen, (brightness, brightness, brightness), (x, y, size, size * 0.8))

        # Draw border
        pygame.draw.rect(screen, ACCENT, (10, 10, WIDTH - 20, HEIGHT - 20), 4, border_radius = 10)

    running = True
    while running:
        screen.fill(BACKGROUND)
        draw_decorations()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.game_state in ["won", "lost"]:
                    game.reset_game()

                elif event.key == pygame.K_ESCAPE:
                    running = False

            # Handle button clicks
            for button in game.buttons:
                if button.handle_event(event):
                    game.guess_letter(button.text)

        
        # Draw game elements
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()