"""
Settings management module for CurseType

This module handles all settings-related functionality including:
- Settings menu navigation with wrap-around selection
- Difficulty level configuration
- Color customization menus
- Menu drawing and input handling
"""

import curses
from core import constants, ui, config


def draw_menu(window, title_list, selected_idx, footer_msg, y_start):
    """
    Draw a menu with options and footer message.
    
    Args:
        window: Curses window to draw on
        title_list: List of menu option strings
        selected_idx: Index of currently selected option
        footer_msg: Footer message to display
        y_start: Starting Y coordinate for the menu
    """
    max_y, max_x = window.getmaxyx()
    
    # Center the footer message
    footer_x = (max_x // 2) - (len(footer_msg) // 2)
    window.addstr(y_start + len(title_list) + 1, footer_x, footer_msg,
                  curses.color_pair(int(config.config_parser['default']['colorsession'])))

    # Draw each menu option
    for i, item in enumerate(title_list):
        x_center = (max_x // 2) - (len(item) // 2)
        if i == selected_idx:
            # Highlight selected option with inverse color text
            window.addstr(y_start + i, x_center, item, curses.A_REVERSE)
        else:
            # Display unselected options in session color
            window.addstr(y_start + i, x_center, item,
                          curses.color_pair(int(config.config_parser['default']['colorsession'])))


def menu_loop(window, items, on_select, on_back):
    """
    Generic menu loop with wrap-around navigation.
    
    Handles menu display, user input, and navigation for any settings menu.
    
    Args:
        window: Curses window for the menu
        items: List of menu item strings
        on_select: Callback function called when an item is selected
        on_back: Callback function called when back is pressed
    """
    max_y, max_x = window.getmaxyx()
    selected = 0
    y_start = (max_y // 2) - (len(items) // 2)
    
    # Configure window for menu interaction
    curses.curs_set(0)  # Hide cursor
    window.nodelay(1)
    window.timeout(100)

    while True:
        window.clear()
        draw_menu(window, items, selected, 'Back(home/del) | Select(enter)', y_start)
        window.refresh()

        try:
            key = window.getkey()
        except curses.error:
            key = None

        # Handle navigation with wrap-around
        if key == 'KEY_UP':
            selected = (selected - 1) % len(items)
        elif key == 'KEY_DOWN':
            selected = (selected + 1) % len(items)
        elif key == '\n':
            on_select(selected)
        elif key in ('KEY_HOME', 'KEY_BACKSPACE', 'KEY_DC'):
            on_back()
            break


def settingsmainmenu(window):
    """
    Display and handle the main settings menu.
    
    Shows options for color settings and vocabulary/difficulty settings.
    """
    def on_select(idx):
        """Handle selection of settings options."""
        if idx == 0:
            settingscolormenu(window)
        elif idx == 1:
            settingsdifficultymenu(window)

    def on_back():
        """Return to main menu."""
        ui.menu(window)

    menu_loop(window, constants.SETTINGS, on_select, on_back)


def settingsdifficultymenu(window):
    """
    Display and handle the difficulty/vocabulary settings menu.
    
    Allows users to select different word lists for varying difficulty levels.
    """
    def on_select(idx):
        """Handle difficulty selection and save to configuration."""
        config.config_parser['default']['difficulty'] = str(idx)
        config.setgamedifficulty(idx)
        config.save_config()
        
        # Show confirmation message
        max_y, max_x = window.getmaxyx()
        msg = f"Set to {constants.SETTINGS_DIFFICULTY[idx]}"
        window.addstr((max_y // 2) - len(constants.SETTINGS_DIFFICULTY) // 2 - 3,
                      (max_x // 2) - (len(msg) // 2), msg)
        window.refresh()
        curses.napms(600)  # Show message for 600ms

    def on_back():
        """Return to settings main menu."""
        settingsmainmenu(window)

    menu_loop(window, constants.SETTINGS_DIFFICULTY, on_select, on_back)


def settingscolormenu(window):
    """
    Display and handle the color settings menu.
    
    Allows users to customize colors for correct letters, incorrect letters,
    and menu elements.
    """
    def on_select(idx):
        """Handle color setting selection."""
        if idx == 0:
            config.setcorrectcolor(window)
        elif idx == 1:
            config.setincorrectcolor(window)
        elif idx == 2:
            config.setmenucolor(window)

    def on_back():
        """Return to settings main menu."""
        settingsmainmenu(window)

    menu_loop(window, constants.SETTINGS_COLOR, on_select, on_back)
