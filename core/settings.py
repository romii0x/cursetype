import curses
from core import constants, ui, config


def draw_menu(window, title_list, selected_idx, footer_msg, y_start):
    max_y, max_x = window.getmaxyx()
    footer_x = (max_x // 2) - (len(footer_msg) // 2)
    window.addstr(y_start + len(title_list) + 1, footer_x, footer_msg,
                  curses.color_pair(int(config.config_parser['default']['colorsession'])))

    for i, item in enumerate(title_list):
        x_center = (max_x // 2) - (len(item) // 2)
        if i == selected_idx:
            window.addstr(y_start + i, x_center, item, curses.A_REVERSE)
        else:
            window.addstr(y_start + i, x_center, item,
                          curses.color_pair(int(config.config_parser['default']['colorsession'])))


def menu_loop(window, items, on_select, on_back):
    max_y, max_x = window.getmaxyx()
    selected = 0
    y_start = (max_y // 2) - (len(items) // 2)
    curses.curs_set(0)
    window.nodelay(1)
    window.timeout(100)

    while True:
        window.clear()
        draw_menu(window, items, selected, 'Back(home/del) | Select(enter)', y_start)
        window.refresh()

        try:
            key = window.getkey()
        except:
            key = None

        if key == 'KEY_UP' and selected > 0:
            selected -= 1
        elif key == 'KEY_DOWN' and selected < len(items) - 1:
            selected += 1
        elif key == '\n':
            on_select(selected)
        elif key in ('KEY_HOME', 'KEY_BACKSPACE', 'KEY_DC'):
            on_back()
            break


def settingsmainmenu(window):
    def on_select(idx):
        if idx == 0:
            settingscolormenu(window)
        elif idx == 1:
            settingsdifficultymenu(window)

    def on_back():
        ui.menu(window)

    menu_loop(window, constants.SETTINGS, on_select, on_back)


def settingsdifficultymenu(window):
    def on_select(idx):
        config.config_parser['default']['difficulty'] = str(idx)
        config.setgamedifficulty(idx)
        config.save_config()
        max_y, max_x = window.getmaxyx()
        msg = f"Set to {constants.SETTINGS_DIFFICULTY[idx]}"
        window.addstr((max_y // 2) - len(constants.SETTINGS_DIFFICULTY) // 2 - 3,
                      (max_x // 2) - (len(msg) // 2), msg)
        window.refresh()
        curses.napms(600)

    def on_back():
        settingsmainmenu(window)

    menu_loop(window, constants.SETTINGS_DIFFICULTY, on_select, on_back)


def settingscolormenu(window):
    def on_select(idx):
        if idx == 0:
            config.setcorrectcolor(window)
        elif idx == 1:
            config.setincorrectcolor(window)
        elif idx == 2:
            config.setmenucolor(window)

    def on_back():
        settingsmainmenu(window)

    menu_loop(window, constants.SETTINGS_COLOR, on_select, on_back)
