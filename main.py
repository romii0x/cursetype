#  ▄▄· ▄• ▄▌▄▄▄  .▄▄ · ▄▄▄ .▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▄▄▄ .
# ▐█ ▌▪█▪██▌▀▄ █·▐█ ▀. ▀▄.▀·•██  ▐█▪██▌▐█ ▄█▀▄.▀·
# ██ ▄▄█▌▐█▌▐▀▀▄ ▄▀▀▀█▄▐▀▀▪▄ ▐█.▪▐█▌▐█▪ ██▀·▐▀▀▪▄
# ▐███▌▐█▄█▌▐█•█▌▐█▄▪▐█▐█▄▄▌ ▐█▌· ▐█▀·.▐█▪·•▐█▄▄▌
# ·▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀▀  ▀▀▀  ▀▀▀   ▀ • .▀    ▀▀▀        
# author: https://github.com/ianshapiro1
# 
# Oxford 3/5000 from https://github.com/tgmgroup/Word-List-from-Oxford-Longman-5000
# 1000 most common US words from https://gist.github.com/deekayen/4148741
# ASCII text art from http://www.patorjk.com/software/taag 

import curses
import random
from core import ui, config, settings, constants

def init_colors():
    """Initialize terminal color pairs."""
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)

def check_terminal_size(window):
    """Ensure terminal is large enough for the UI."""
    height, width = window.getmaxyx()
    if width < 65 or height < 15:
        window.addstr(0, 0, f'Error: Terminal Size ({width}x{height}) too small.')
        window.addstr(2, 0, 'Press any key to quit.')
        window.getch()
        exit()

def setup_session_color():
    """Set or randomly pick a color for the session."""
    color = int(config.config_parser['default']['colorsession'])
    if color < 0:
        config.config_parser['default']['colorsession'] = str(random.randint(0, 232))

def main(window):
    # Load config and set game difficulty
    config.load_config()
    config.setgamedifficulty(int(config.config_parser['default']['difficulty']))

    # Initialize colors and session visuals
    init_colors()
    setup_session_color()

    # Validate terminal size
    check_terminal_size(window)

    # Show menu screen
    ui.menu(window)

if __name__ == "__main__":
    curses.wrapper(main)