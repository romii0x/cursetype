import curses
from core import constants, settings, logic, config

def updatewpm(counter, wpm, acc):
    counter.clear()
    wpm_index = max(min(int(wpm) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    acc_index = max(min(int(acc) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    
    if wpm < 200:
        counter.addstr(0, 0, f'{wpm:.2f} wpm ', curses.color_pair(constants.COLOR_INDICATORS[wpm_index]))
        counter.addstr(0, 11, f'| {acc:.2f} %', curses.color_pair(constants.COLOR_INDICATORS[acc_index]))
    else:
        counter.addstr(0, 0, f'{wpm:.2f} wpm ')
        counter.addstr(0, 11, f'| {acc:.2f} %', curses.color_pair(constants.COLOR_INDICATORS[acc_index]))
    counter.refresh()

def displayinfo(window, wpm, acc, seconds, realcch, realich, cch, ich, mode):
    y, x = window.getmaxyx()
    x //= 2
    y //= 2
    x -= 10
    
    window.clear()
    window.move(y, x)
    
    color_session = curses.color_pair(int(config.config_parser['default']['colorsession']))
    wpm_index = max(min(int(wpm) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    acc_index = max(min(int(acc) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)

    window.addstr(y+1, x, 'Menu(home/del) New(enter)', color_session)
    window.addstr(y-3, x, f'{wpm:.2f} wpm', curses.color_pair(constants.COLOR_INDICATORS[wpm_index]))
    window.addstr(y-2, x, f'{acc:.2f} % ', curses.color_pair(constants.COLOR_INDICATORS[acc_index]))
    window.addstr(y-1, x, f'{seconds:.2f} (s) ')
    window.addstr(y, x, f'C: {realcch} I: {realich} M: {ich} F: {ich - realich}')

    while True:
        key = window.getkey()
        if key in ['KEY_HOME', 'KEY_DC']:
            menu(window)
        elif key == '\n':
            if mode == 1:
                logic.sentence_mode(window)
            elif mode == 2:
                logic.paragraph_mode(window)

def guide(window):
    y, x = window.getmaxyx()
    curses.curs_set(0)
    window.clear()
    x = x // 2 - len(constants.GUIDE_FILE[1]) // 2
    color_session = curses.color_pair(int(config.config_parser['default']['colorsession']))

    for i, line in enumerate(constants.GUIDE_FILE):
        window.addstr(1 + i, x, str(line), color_session)

    window.nodelay(1)
    window.timeout(100)
    window.refresh()

    while True:
        try:
            key = window.getkey()
        except:
            key = None

        if key in ['KEY_HOME', 'KEY_DC']:
            menu(window)
            return

def menu(window):
    curses.curs_set(0)
    window.clear()
    height, width = window.getmaxyx()

    options = [
        ("Sentence Mode", lambda: logic.sentence_mode(window)),
        ("Paragraph Mode", lambda: logic.paragraph_mode(window)),
        ("Guide", lambda: guide(window)),
        ("Settings", lambda: settings.settingsmainmenu(window)),
        ("Exit", lambda: exit())
    ]
    selected = 0

    color_session = curses.color_pair(int(config.config_parser['default']['colorsession']))
    color_highlight = curses.A_REVERSE

    while True:
        window.clear()
        banner_y = height // 2 - len(options) // 2 - 2
        banner_x = width // 2 - len(constants.CONSOLE_BANNER) // 2
        window.addstr(banner_y, banner_x, constants.CONSOLE_BANNER, color_session)

        for i, (text, _) in enumerate(options):
            x = width // 2 - len(text) // 2
            y = height // 2 - len(options) // 2 + i
            if i == selected:
                window.addstr(y, x, text, color_highlight | color_session)
            else:
                window.addstr(y, x, text, color_session)

        key = window.getch()

        if key in [curses.KEY_UP, ord('k')]:
            selected = (selected - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord('j')]:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, ord('\n')]:
            options[selected][1]()
            return
        elif key in [curses.KEY_HOME, curses.KEY_DC]:
            return

        window.refresh()
