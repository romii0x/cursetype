"""
Constants module for CurseType

This module contains all the constant values used throughout the application,
including character sets, UI text, color schemes, and configuration options.
"""

# Character sets for input validation
LETTERS = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]  # a-z + A-Z
COMMANDS = ['quit', 'q', 'sentence', 's', 'paragraph', 'p', 'help', 'settings', 'c']

# UI text constants
OPENING_MESSAGE = 'Welcome to CurseType! Type "sentence" or "help" and press enter.'
CONSOLE_BANNER = 'CurseType'

# Special characters that are valid input (apostrophe, space, hyphen, backspace)
SPECIAL_CHARS = [chr(39), chr(32), chr(45), 'KEY_BACKSPACE']

# Settings menu options
SETTINGS = ['color', 'vocabulary']
SETTINGS_COLOR = ['correct letter', 'incorrect letter', 'menu color']
SETTINGS_DIFFICULTY = ['common words', 'oxford 3000', 'oxford 5000']

# Color indicators for WPM/accuracy display
# Colors change based on performance: blue (great) -> green (good) -> yellow (average)-> red (poor)
COLOR_INDICATORS = [10, 10, 197, 203, 215, 227, 191, 155, 119, 122, 124, 82, 76, 70, 64, 100, 142, 184, 226, 254]

# Minimum terminal dimensions required for proper display
MIN_TERMINAL_WIDTH = 65
MIN_TERMINAL_HEIGHT = 15

# Word list file mappings by difficulty level
# Each difficulty level loads different word files for varied vocabulary
WORDLIST_FILES = {
    0: ['1-1000.txt'],                    # Common words
    1: ['1-1000.txt', 'o3000.txt'],       # Common + Oxford 3000
    2: ['o5000.txt', '1-1000.txt', 'o3000.txt']  # All word lists
}

# Global word list - populated at runtime based on difficulty setting
WORDS = []