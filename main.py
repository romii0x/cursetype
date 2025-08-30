#  ▄▄· ▄• ▄▌▄▄▄  .▄▄ · ▄▄▄ .▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▄▄▄ .
# ▐█ ▌▪█▪██▌▀▄ █·▐█ ▀. ▀▄.▀·•██  ▐█▪██▌▐█ ▄█▀▄.▀·
# ██ ▄▄█▌▐█▌▐▀▀▄ ▄▀▀▀█▄▐▀▀▪▄ ▐█.▪▐█▌▐█▪ ██▀·▐▀▀▪▄
# ▐███▌▐█▄█▌▐█•█▌▐█▄▪▐█▐█▄▄▌ ▐█▌· ▐█▀·.▐█▪·•▐█▄▄▌
# ·▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀▀  ▀▀▀  ▀▀▀   ▀ • .▀    ▀▀▀        
# author: https://github.com/romii0x
# 
# Oxford 3/5000 from https://github.com/tgmgroup/Word-List-from-Oxford-Longman-5000
# 1000 most common US words from https://gist.github.com/deekayen/4148741
# ASCII text art from http://www.patorjk.com/software/taag 

"""
This module serves as the main entry point for the CurseType application.
It handles initialization of the curses environment, terminal setup,
and launches the main menu interface.
"""

import curses
import random
from core import ui, config, settings, constants

def init_colors():
    """
    Initialize terminal color pairs for the application.
    
    Sets up color pairs 1 through curses.COLORS for use throughout the app.
    Each color pair maps a foreground color to the default background.
    """
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)

def check_terminal_size(window):
    """
    Validate that the terminal is large enough to display the UI properly.
    
    Args:
        window: The curses window object
        
    Exits the program if terminal is too small to display the interface.
    """
    height, width = window.getmaxyx()
    if width < constants.MIN_TERMINAL_WIDTH or height < constants.MIN_TERMINAL_HEIGHT:
        window.addstr(0, 0, f'Error: Terminal Size ({width}x{height}) too small.')
        window.addstr(2, 0, 'Press any key to quit.')
        window.getch()
        exit()

def setup_session_color():
    """
    Set or randomly pick a color for the current session.
    
    If the session color is set to -1 (random), generates a random color
    between 0 and 232 and saves it to the configuration.
    """
    color = int(config.config_parser['default']['colorsession'])
    if color < 0:
        config.config_parser['default']['colorsession'] = str(random.randint(0, 232))

def main(window):
    """
    Main application entry point.
    
    Initializes the application, loads configuration, sets up the terminal
    environment, and launches the main menu.
    
    Args:
        window: The curses window object provided by curses.wrapper()
    """
    # Load configuration and set game difficulty
    config.load_config()
    config.setgamedifficulty(int(config.config_parser['default']['difficulty']))

    # Initialize colors and session visuals
    init_colors()
    setup_session_color()

    # Validate terminal size
    check_terminal_size(window)

    # Show the main menu screen
    ui.menu(window)

if __name__ == "__main__":
    # Use curses.wrapper to handle terminal setup/cleanup
    curses.wrapper(main)