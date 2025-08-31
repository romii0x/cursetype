"""
Configuration management module for CurseType

This module handles all configuration-related functionality including:
- Loading and saving settings from/to INI files
- Word list management based on difficulty settings
- Color picker interface for customizing UI colors
- Configuration file initialization and defaults
"""

import curses
import configparser
import random
import os
from core import settings, logic, constants

# Global configuration parser instance
config_parser = configparser.ConfigParser()


def load_config(filename='settings.ini'):
    """
    Load configuration from INI file with default values.
    
    Creates default configuration if file doesn't exist or is missing values.
    
    Args:
        filename: Path to the configuration file
        
    Returns:
        configparser.ConfigParser: Loaded configuration object
    """
    config_parser.read(filename)
    default = config_parser.setdefault('default', {})
    
    # Set default values for configuration options
    default.setdefault('difficulty', '0')
    default.setdefault('colorsession', '252') # light gray
    default.setdefault('colorcorrect', '3') # bright green
    default.setdefault('colorincorrect', '2') # bright red
    
    return config_parser


def save_config(filename='settings.ini'):
    """
    Save current configuration to INI file.
    
    Args:
        filename: Path to the configuration file
    """
    with open(filename, 'w') as configfile:
        config_parser.write(configfile)

def setgamedifficulty(difficulty):
    """
    Load word lists based on the selected difficulty level.
    
    Different difficulty levels use different word lists:
    - 0: MonkeyType default (200 most common words)
    - 1: English 1000 (most common words)
    - 2: English 1000 + Oxford 3000 words
    - 3: All word lists (Oxford 5000 + English 1000 + Oxford 3000)
    
    Args:
        difficulty: Difficulty level (0, 1, 2, or 3)
    """
    base_path = 'wordlists'
    file_names = constants.WORDLIST_FILES.get(difficulty, [])

    # Clear existing word list and load new words
    constants.WORDS = []
    for name in file_names:
        full_path = os.path.join(base_path, name)
        try:
            with open(full_path, 'r') as f:
                constants.WORDS.extend(f.read().splitlines())
        except FileNotFoundError:
            # Skip missing word list files
            continue


def color_picker(window, config_key):
    """
    Interactive color picker interface for customizing UI colors.
    
    Displays all available terminal colors in a grid format and allows
    users to navigate and select colors using arrow keys.
    
    Args:
        window: Curses window for the color picker interface
        config_key: Configuration key to save the selected color to
    """
    max_y, max_x = window.getmaxyx()
    window.clear()
    
    # Calculate grid layout
    y, x = max_y // 3, max_x // 5
    starty, startx = y, x
    maxx = int(max_x - (1 / 5 * max_x))
    cols_per_row = maxx - startx
    
    # Configure window for color picker interaction
    window.nodelay(1)
    window.timeout(100)
    curses.curs_set(1)  # Show cursor for color selection

    # Draw all available colors in a grid
    color_count = 0
    for i in range(curses.COLORS):
        if x < maxx:
            window.addstr(y, x, '0', curses.color_pair(i + 1))
            x += 1
            color_count += 1
        else:
            # Move to next row when current row is full
            x = startx
            y += 1
            window.addstr(y, x, '0', curses.color_pair(i + 1))
            x += 1
            color_count += 1

    maxy = y
    
    # Get current color setting and position cursor accordingly
    current_option = int(config_parser['default'][config_key])
    
    # Calculate cursor position based on current color
    option = current_option
    color_index = current_option - 1  # Convert to 0-based index
    
    # Calculate x, y position from color index
    x = startx + (color_index % cols_per_row)
    y = starty + (color_index // cols_per_row)
    
    # Ensure position is within bounds
    if y > maxy:
        y = maxy
        x = startx + (color_index % cols_per_row)
    
    # Draw footer message
    footer_msg = 'Back(home/del) | Select(enter)'
    footer_x = (max_x // 2) - (len(footer_msg) // 2)
    window.addstr(maxy + 1, footer_x, footer_msg,
                  curses.color_pair(int(config_parser['default']['colorsession'])))
    
    # Position cursor on current color
    window.move(y, x)

    # Color picker interaction loop
    while True:
        try:
            key = window.getkey()
        except curses.error:
            key = None

        # Handle navigation with boundary checking
        if key == 'KEY_UP' and y != starty:
            y -= 1
            option -= cols_per_row
        elif key == 'KEY_DOWN' and y != maxy:
            y += 1
            option += cols_per_row
        elif key == 'KEY_LEFT' and x != startx:
            x -= 1
            option -= 1
        elif key == 'KEY_RIGHT' and x != maxx - 1:
            x += 1
            option += 1
        elif key == '\n':
            # Save selected color if it's within valid range
            if 1 <= option <= curses.COLORS:
                config_parser['default'][config_key] = str(option)
                save_config()
                settings.settingscolormenu(window)
        elif key in ('KEY_HOME', 'KEY_BACKSPACE', 'KEY_DC'):
            # Reset terminal to normal mode before going back
            window.nodelay(False)
            window.timeout(-1)  # Reset to blocking mode
            curses.curs_set(0)  # Hide cursor
            curses.echo()  # Re-enable echo
            settings.settingscolormenu(window)

        window.move(y, x)


def setincorrectcolor(window):
    """
    Launch color picker for incorrect letter color setting.
    
    Args:
        window: Curses window for the color picker
    """
    color_picker(window, 'colorincorrect')


def setcorrectcolor(window):
    """
    Launch color picker for correct letter color setting.
    
    Args:
        window: Curses window for the color picker
    """
    color_picker(window, 'colorcorrect')


def setmenucolor(window):
    """
    Launch color picker for menu color setting.
    
    Args:
        window: Curses window for the color picker
    """
    color_picker(window, 'colorsession')
