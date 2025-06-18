// Word list from your Python version
const words = [
    "PYTHON", "JAVASCRIPT", "PROGRAMMING", "COMPUTER", "ALGORITHM",
    "DATABASE", "NETWORK", "DEVELOPER", "SOFTWARE", "CODING"
];

class HangmanGame {
    constructor() {
        this.canvas = document.getElementById('hangman');
        this.ctx = this.canvas.getContext('2d');
        this.wordDisplay = document.querySelector('.word-display');
        this.keyboard = document.querySelector('.keyboard');
        this.messageDisplay = document.querySelector('.game-message');
        this.newGameBtn = document.getElementById('new-game-btn');
        
        this.maxMistakes = 6;
        this.mistakes = 0;
        this.word = '';
        this.guessedLetters = new Set();
        
        this.initializeGame();
        this.setupEventListeners();
    }
    
    initializeGame() {
        this.word = words[Math.floor(Math.random() * words.length)];
        this.mistakes = 0;
        this.guessedLetters.clear();
        this.messageDisplay.textContent = '';
        this.messageDisplay.className = 'game-message';
        
        this.createWordDisplay();
        this.createKeyboard();
        this.drawHangman();
    }
    
    createWordDisplay() {
        this.wordDisplay.innerHTML = '';
        [...this.word].forEach(letter => {
            const letterElement = document.createElement('div');
            letterElement.className = 'letter';
            letterElement.textContent = this.guessedLetters.has(letter) ? letter : '';
            this.wordDisplay.appendChild(letterElement);
        });
    }
    
    createKeyboard() {
        this.keyboard.innerHTML = '';
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(letter => {
            const button = document.createElement('button');
            button.className = 'key';
            button.textContent = letter;
            button.disabled = this.guessedLetters.has(letter);
            button.addEventListener('click', () => this.handleGuess(letter));
            this.keyboard.appendChild(button);
        });
    }
    
    handleGuess(letter) {
        if (this.guessedLetters.has(letter)) return;
        
        this.guessedLetters.add(letter);
        const button = [...this.keyboard.children].find(btn => btn.textContent === letter);
        button.disabled = true;
        button.classList.add('used');
        
        if (!this.word.includes(letter)) {
            this.mistakes++;
            this.drawHangman();
        }
        
        this.createWordDisplay();
        this.checkGameEnd();
    }
    
    checkGameEnd() {
        const won = [...this.word].every(letter => this.guessedLetters.has(letter));
        const lost = this.mistakes >= this.maxMistakes;
        
        if (won) {
            this.messageDisplay.textContent = 'Congratulations! You won!';
            this.messageDisplay.className = 'game-message win';
            this.disableKeyboard();
        } else if (lost) {
            this.messageDisplay.textContent = `Game Over! The word was: ${this.word}`;
            this.messageDisplay.className = 'game-message lose';
            this.disableKeyboard();
        }
    }
    
    disableKeyboard() {
        [...this.keyboard.children].forEach(button => {
            button.disabled = true;
        });
    }
    
    drawHangman() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = '#2C3E50';
        this.ctx.lineWidth = 3;
        
        // Base
        this.ctx.beginPath();
        this.ctx.moveTo(50, 250);
        this.ctx.lineTo(250, 250);
        this.ctx.stroke();
        
        if (this.mistakes >= 1) {
            // Pole
            this.ctx.beginPath();
            this.ctx.moveTo(100, 250);
            this.ctx.lineTo(100, 50);
            this.ctx.lineTo(200, 50);
            this.ctx.lineTo(200, 80);
            this.ctx.stroke();
        }
        
        if (this.mistakes >= 2) {
            // Head
            this.ctx.beginPath();
            this.ctx.arc(200, 100, 20, 0, Math.PI * 2);
            this.ctx.stroke();
        }
        
        if (this.mistakes >= 3) {
            // Body
            this.ctx.beginPath();
            this.ctx.moveTo(200, 120);
            this.ctx.lineTo(200, 180);
            this.ctx.stroke();
        }
        
        if (this.mistakes >= 4) {
            // Left arm
            this.ctx.beginPath();
            this.ctx.moveTo(200, 140);
            this.ctx.lineTo(170, 160);
            this.ctx.stroke();
        }
        
        if (this.mistakes >= 5) {
            // Right arm
            this.ctx.beginPath();
            this.ctx.moveTo(200, 140);
            this.ctx.lineTo(230, 160);
            this.ctx.stroke();
        }
        
        if (this.mistakes >= 6) {
            // Left leg
            this.ctx.beginPath();
            this.ctx.moveTo(200, 180);
            this.ctx.lineTo(170, 220);
            this.ctx.stroke();
            
            // Right leg
            this.ctx.beginPath();
            this.ctx.moveTo(200, 180);
            this.ctx.lineTo(230, 220);
            this.ctx.stroke();
        }
    }
    
    setupEventListeners() {
        this.newGameBtn.addEventListener('click', () => this.initializeGame());
        
        document.addEventListener('keydown', (event) => {
            const letter = event.key.toUpperCase();
            if (/^[A-Z]$/.test(letter) && !this.guessedLetters.has(letter)) {
                this.handleGuess(letter);
            }
        });
    }
}

// Start the game when the page loads
window.addEventListener('load', () => {
    new HangmanGame();
}); 