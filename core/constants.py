LETTERS = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
COMMANDS = ['quit', 'q', 'sentence', 's', 'paragraph', 'p', 'help', 'settings', 'c']
OPENING_MESSAGE = 'Welcome to CurseType! Type "sentence" or "help" and press enter.'
CONSOLE_BANNER = 'CurseType'
SPECIAL_CHARS = [chr(39), chr(32), chr(45), 'KEY_BACKSPACE']
SETTINGS = ['color', 'vocabulary']
SETTINGS_COLOR = ['correct letter', 'incorrect letter', 'menu color']
SETTINGS_DIFFICULTY = ['common words', 'oxford 3000', 'oxford 5000']
COLOR_INDICATORS = [10, 10, 197, 203, 215, 227, 191, 155, 119, 122, 124, 82, 76, 70, 64, 100, 142, 184, 226, 254]

MIN_TERMINAL_WIDTH = 65
MIN_TERMINAL_HEIGHT = 15

WORDLIST_FILES = {
    0: ['1-1000.txt'],
    1: ['1-1000.txt', 'o3000.txt'],
    2: ['o5000.txt', '1-1000.txt', 'o3000.txt']
}

WORDS = []