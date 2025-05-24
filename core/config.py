import curses
import configparser
import random
import os
from core import settings, logic, constants

config_parser = configparser.ConfigParser()


def load_config(filename='settings.ini'):
    config_parser.read(filename)
    default = config_parser.setdefault('default', {})
    default.setdefault('difficulty', '0')
    default.setdefault('colorsession', str(random.randint(0, 232)))
    default.setdefault('colorcorrect', '1')
    default.setdefault('colorincorrect', '1')
    return config_parser


def save_config(filename='settings.ini'):
    with open(filename, 'w') as configfile:
        config_parser.write(configfile)

def setgamedifficulty(difficulty):
    base_path = 'wordlists'
    file_names = constants.WORDLIST_FILES.get(difficulty, [])

    constants.WORDS = []
    for name in file_names:
        full_path = os.path.join(base_path, name)
        with open(full_path, 'r') as f:
            constants.WORDS.extend(f.read().splitlines())


def color_picker(window, config_key):
    max_y, max_x = window.getmaxyx()
    window.clear()
    y, x = max_y // 3, max_x // 5
    starty, startx = y, x
    maxx = int(max_x - (1 / 5 * max_x))
    screenrange = maxx - startx
    window.nodelay(1)
    window.timeout(100)
    curses.curs_set(1)

    for i in range(curses.COLORS):
        if x < maxx:
            window.addstr(y, x, '0', curses.color_pair(i + 1))
            x += 1
        else:
            x = max_x // 5
            y += 1

    maxy = y
    option = 1
    y, x = starty, startx
    window.move(y, x)

    while True:
        try:
            key = window.getkey()
        except:
            key = None

        if key == 'KEY_UP' and y != starty:
            y -= 1
            option -= screenrange + 1
        elif key == 'KEY_DOWN' and y != maxy:
            y += 1
            option += screenrange + 1
        elif key == 'KEY_LEFT' and x != startx:
            x -= 1
            option -= 1
        elif key == 'KEY_RIGHT' and x != maxx:
            x += 1
            option += 1
        elif key == '\n':
            config_parser['default'][config_key] = str(option)
            save_config()
            settings.settingscolormenu(window)
        elif key in ('KEY_HOME', 'KEY_BACKSPACE', 'KEY_DC'):
            settings.settingscolormenu(window)

        window.move(y, x)


def setincorrectcolor(window):
    color_picker(window, 'colorincorrect')


def setcorrectcolor(window):
    color_picker(window, 'colorcorrect')


def setmenucolor(window):
    color_picker(window, 'colorsession')
