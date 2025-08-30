"""
User interface module for CurseType

This module handles all user interface components including:
- Real-time WPM and accuracy display
- Results screen with detailed statistics
- Main menu navigation with wrap-around selection
- Visual feedback and color coding
"""

import curses
from core import constants, settings, logic, config

def updatewpm(counter, wpm, accuracy):
    """
    Update the real-time WPM and accuracy display.
    
    Displays current typing speed and accuracy with color-coded feedback.
    Colors change based on performance: blue (great) -> green (good) -> yellow (average)-> red (poor).
    
    Args:
        counter: Curses window for displaying WPM/accuracy
        wpm: Current words per minute
        accuracy: Current accuracy percentage
    """
    counter.clear()
    
    # Calculate color indices based on performance
    wpm_index = max(min(int(wpm) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    accuracy_index = max(min(int(accuracy) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    
    # Display WPM and accuracy with appropriate colors
    if wpm < 200:
        counter.addstr(0, 0, f'{wpm:.2f} wpm ', curses.color_pair(constants.COLOR_INDICATORS[wpm_index]))
        counter.addstr(0, 11, f'| {accuracy:.2f} %', curses.color_pair(constants.COLOR_INDICATORS[accuracy_index]))
    else:
        # For very high WPM, use default color for WPM to avoid color overflow
        counter.addstr(0, 0, f'{wpm:.2f} wpm ')
        counter.addstr(0, 11, f'| {accuracy:.2f} %', curses.color_pair(constants.COLOR_INDICATORS[accuracy_index]))
    counter.refresh()

def displayinfo(window, wpm, accuracy, seconds, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars, mode):
    """
    Display the final results screen after completing a typing test.
    
    Shows comprehensive statistics including WPM, accuracy, time taken,
    and character counts with color-coded performance indicators.
    
    Args:
        window: Curses window for displaying results
        wpm: Final words per minute
        accuracy: Final accuracy percentage
        seconds: Time taken for the test
        final_correct_chars: Total correct characters in final result
        final_incorrect_chars: Total incorrect characters in final result
        correct_chars: Total correct characters typed (including corrections)
        incorrect_chars: Total incorrect characters typed (including corrections)
        mode: Test mode (1 for sentence, 2 for paragraph)
    """
    # Calculate center position for results display
    y, x = window.getmaxyx()
    x //= 2
    y //= 2
    x -= 10
    
    window.clear()
    window.move(y, x)
    
    # Get session color for UI elements
    color_session = curses.color_pair(int(config.config_parser['default']['colorsession']))
    
    # Calculate color indices for performance indicators
    wpm_index = max(min(int(wpm) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)
    accuracy_index = max(min(int(accuracy) // 10 - 1, len(constants.COLOR_INDICATORS) - 1), 0)

    # Display results with color coding
    window.addstr(y+1, x, 'Menu(home/del) New(enter)', color_session)
    window.addstr(y-3, x, f'{wpm:.2f} wpm', curses.color_pair(constants.COLOR_INDICATORS[wpm_index]))
    window.addstr(y-2, x, f'{accuracy:.2f} % ', curses.color_pair(constants.COLOR_INDICATORS[accuracy_index]))
    window.addstr(y-1, x, f'{seconds:.2f} (s) ')
    
    # Display character statistics:
    # C: Final correct characters, I: Final incorrect characters
    # M: Total mistakes made, F: Mistakes that were corrected
    window.addstr(y, x, f'C: {final_correct_chars} I: {final_incorrect_chars} M: {incorrect_chars} F: {incorrect_chars - final_incorrect_chars}')

    # Wait for user input to continue
    while True:
        key = window.getkey()
        if key in ['KEY_HOME', 'KEY_DC']:
            menu(window)
        elif key == '\n':
            # Start a new test in the same mode
            if mode == 1:
                logic.sentence_mode(window)
            elif mode == 2:
                logic.paragraph_mode(window)

def menu(window):
    """
    Display and handle the main menu interface.
    
    Shows the CurseType banner and menu options with wrap-around navigation.
    Handles user selection and launches appropriate functions.
    
    Args:
        window: Curses window for the menu interface
    """
    curses.curs_set(0)  # Hide cursor
    window.clear()
    height, width = window.getmaxyx()

    # Define menu options with their corresponding functions
    options = [
        ("Sentence Mode", lambda: logic.sentence_mode(window)),
        ("Paragraph Mode", lambda: logic.paragraph_mode(window)),
        ("Settings", lambda: settings.settingsmainmenu(window)),
        ("Exit", lambda: exit())
    ]
    selected = 0

    # Get colors for UI elements
    color_session = curses.color_pair(int(config.config_parser['default']['colorsession']))
    color_highlight = curses.A_REVERSE

    # Main menu loop
    while True:
        window.clear()
        
        # Display the CurseType banner
        banner_y = height // 2 - len(options) // 2 - 2
        banner_x = width // 2 - len(constants.CONSOLE_BANNER) // 2
        window.addstr(banner_y, banner_x, constants.CONSOLE_BANNER, color_session)

        # Display menu options with highlighting for selected item
        for i, (text, _) in enumerate(options):
            x = width // 2 - len(text) // 2
            y = height // 2 - len(options) // 2 + i
            if i == selected:
                window.addstr(y, x, text, color_highlight | color_session)
            else:
                window.addstr(y, x, text, color_session)

        # Handle user input
        key = window.getch()

        # Navigation with wrap-around
        if key in [curses.KEY_UP, ord('k')]:
            selected = (selected - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord('j')]:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, ord('\n')]:
            # Execute selected option
            options[selected][1]()
            return
        elif key in [curses.KEY_HOME, curses.KEY_DC]:
            return

        window.refresh()
