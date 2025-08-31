"""
Core typing logic module for CurseType

This module contains the main typing test functionality including:
- Sentence generation and word list management
- Character-by-character typing validation
- Real-time WPM and accuracy calculation
- Backspace handling and cursor management
- Multi-line paragraph mode support
"""

import curses
import random
import time
from core import constants, ui, config


def avg_word_length(words):
    """
    Calculate the average word length from a list of words.
    
    Args:
        words: List of words to calculate average length for
        
    Returns:
        float: Average word length
    """
    if not words:
        return 0
    return sum(len(word) for word in words) / len(words)


def generate_sentence(length):
    """
    Generate a random sentence that fits within the specified length.
    
    Args:
        length: Maximum character length for the sentence
        
    Returns:
        str: Generated sentence with spaces between words
    """
    sentence = []
    current_length = 0
    while True:
        word = random.choice(constants.WORDS)
        # Check if adding this word would exceed the length limit
        if current_length + len(word) + 1 < length:
            sentence.append(word)
            current_length += len(word) + 1  # +1 for space
        elif current_length + len(word) + 1 == length:
            sentence.append(word)
            return ' '.join(sentence)
        else:
            return ' '.join(sentence)


def draw_sentence_lines(window, sentences, start_y, start_x):
    """
    Draw multiple sentence lines on the window.
    
    Args:
        window: Curses window to draw on
        sentences: List of sentences to display
        start_y: Starting Y coordinate
        start_x: Starting X coordinate
    """
    for idx, line in enumerate(sentences):
        window.addstr(start_y + idx, start_x, line)


def highlight_characters(window, y, x, sentence, char_position):
    """
    Highlight the current character position with underline and bold.
    
    Args:
        window: Curses window to draw on
        y: Y coordinate for highlighting
        x: X coordinate for highlighting
        sentence: Current sentence being typed
        char_position: Current character position in the sentence
    """
    if char_position < len(sentence):
        window.addch(y, x, sentence[char_position], curses.A_UNDERLINE | curses.A_BOLD)


def handle_backspace(window, y, x, char_position, stops, sentence, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars):
    """
    Handle backspace functionality by restoring the previous character.
    
    Args:
        window: Curses window to draw on
        y: Y coordinate
        x: X coordinate
        char_position: Current character position
        stops: List tracking correct/incorrect characters
        sentence: Current sentence being typed
        final_correct_chars: Count of final correct characters
        final_incorrect_chars: Count of final incorrect characters
        correct_chars: Count of total correct characters typed
        incorrect_chars: Count of total incorrect characters typed
        
    Returns:
        tuple: Updated (x, char_position, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars)
    """
    # Decrement the appropriate counter based on what was typed
    if stops[char_position - 1] == 0:
        final_incorrect_chars -= 1
        incorrect_chars -= 1
    else:
        final_correct_chars -= 1
        correct_chars -= 1
        stops[char_position - 1] = 0
    
    # Restore the previous character to its original state
    window.addch(y, x - 1, sentence[char_position - 1])
    # Clear the underline at the current position (only if char_position is valid)
    if char_position < len(sentence):
        window.addch(y, x, sentence[char_position])
    return x - 1, char_position - 1, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars


def typing_loop(window, sentences, center_y, center_x, is_paragraph):
    """
    Main typing test loop that handles character input and validation.
    
    This function manages the core typing experience including:
    - Character-by-character validation
    - Real-time WPM and accuracy calculation
    - Visual feedback for correct/incorrect typing
    - Backspace handling
    - Multi-line navigation in paragraph mode
    
    Args:
        window: Curses window for the typing interface
        sentences: List of sentences to type (single sentence for sentence mode)
        center_y: Center Y coordinate for text positioning
        center_x: Center X coordinate for text positioning
        is_paragraph: Boolean indicating if this is paragraph mode
    """
    # Calculate column width for text wrapping
    col_width = curses.COLS - 2 * center_x
    
    # Initialize position tracking variables
    char_position = sentence_position = 0
    cursor_x_offset = center_x
    sentence = sentences[0]

    # Initialize character counters
    correct_chars = 0
    incorrect_chars = 0
    final_correct_chars = 0
    final_incorrect_chars = 0
    
    # Track correct/incorrect status for each character position
    stops = [[0 for _ in s] for s in sentences]
    
    # Performance tracking variables
    wpm = accuracy = seconds = 0
    start = None
    
    # Create WPM display window
    wpm_display_window = curses.newwin(1, curses.COLS, center_y - 2, center_x)
    moved_to_previous_line = False
    just_backspaced = False  # Flag to track if we just backspaced

    # Configure window for non-blocking input
    window.nodelay(True)
    window.timeout(100)
    curses.noecho()
    curses.curs_set(0)
    window.clear()

    # Draw initial sentence and UI elements
    draw_sentence_lines(window, sentences, center_y, center_x)
    window.addstr(center_y + (len(sentences) + 1), center_x, 
                  'Exit(home/del) | New(enter)', 
                  curses.color_pair(int(config.config_parser['default']['colorsession'])))
    highlight_characters(window, center_y, center_x, sentence, char_position)
    window.move(center_y, center_x)
    window.refresh()

    # Main typing loop
    while True:
        try:
            letter = window.getkey()
        except curses.error:
            letter = None

        # Handle exit commands
        if letter in ('KEY_HOME', 'KEY_DC'):
            # Reset terminal to normal mode before returning to menu
            window.nodelay(False)
            window.timeout(-1)  # Reset to blocking mode
            curses.curs_set(0)  # Hide cursor
            curses.echo()  # Re-enable echo
            ui.menu(window)
            return  # Actually exit the typing loop

        # Handle valid character input
        if letter is not None and (letter in constants.LETTERS or letter in " '-"):
            # Reset backspace flag when typing new characters
            just_backspaced = False
            
            # Start timing on first character or restart if backspaced to beginning
            if char_position == 0 and sentence_position == 0:
                start = time.time()

            # Check if we've reached the end of the current sentence
            if char_position >= len(sentence):
                if is_paragraph and sentence_position < len(sentences) - 1:
                    # Move to next line in paragraph mode
                    center_y += 1
                    cursor_x_offset -= char_position
                    char_position = 0
                    sentence_position += 1
                    sentence = sentences[sentence_position]
                    continue
                else:
                    # End of typing test
                    break

            # Validate the typed character against expected character
            expected_char = sentence[char_position]
            is_correct = letter == expected_char
            color_correct = curses.color_pair(int(config.config_parser['default']['colorcorrect']))
            color_incorrect = curses.color_pair(int(config.config_parser['default']['colorincorrect']))
            stops[sentence_position][char_position] = 1 if is_correct else 0

            # Handle correct character typing
            if is_correct:
                correct_chars += 1
                final_correct_chars += 1
                window.addch(center_y, cursor_x_offset, expected_char, color_correct)
            else:
                # Handle incorrect character typing
                incorrect_chars += 1
                final_incorrect_chars += 1
                if expected_char == ' ':
                    # Show the incorrect character that was typed over a space
                    window.addch(center_y, cursor_x_offset, letter, color_incorrect)
                else:
                    # Show the correct character that should have been typed
                    window.addch(center_y, cursor_x_offset, expected_char, color_incorrect)
            
            # Move cursor to next position
            cursor_x_offset += 1
            char_position += 1

            # Update WPM and accuracy display (ONLY when typing new characters)
            if start is not None:
                seconds = time.time() - start
                # Only calculate WPM if we have characters typed and positive time
                if final_correct_chars > 0 and seconds > 0:
                    # Standard character-based WPM calculation (5 characters per word)
                    # This matches industry standards used by MonkeyType, TypeRacer, etc.
                    # Use final_correct_chars to reflect actual final performance
                    wpm = (final_correct_chars / seconds / 5) * 60
                    accuracy = (final_correct_chars / (final_correct_chars + final_incorrect_chars)) * 100
                    ui.updatewpm(wpm_display_window, wpm, accuracy)
                else:
                    # Reset WPM display when no characters are typed
                    ui.updatewpm(wpm_display_window, 0, 0)

            # Check if we've completed the entire test
            if char_position >= len(sentence) and sentence_position == len(sentences) - 1:
                break

        elif letter == 'KEY_BACKSPACE':
            # Handle backspace functionality
            if char_position > 0:
                # Regular backspace within the same line
                cursor_x_offset, char_position, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars = handle_backspace(
                    window, center_y, cursor_x_offset, char_position, 
                    stops[sentence_position], sentence, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars
                )
                just_backspaced = True
            elif char_position == 0 and sentence_position > 0:
                # Backspace to previous line in paragraph mode
                # Clear highlight from current line before moving
                window.addch(center_y, center_x, sentence[0])
                sentence_position -= 1
                sentence = sentences[sentence_position]
                char_position = len(sentence) - 1
                center_y -= 1
                cursor_x_offset = center_x + char_position
                # Update highlight for the new line
                highlight_characters(window, center_y, cursor_x_offset, sentence, char_position)
                moved_to_previous_line = True
                just_backspaced = True  # Set backspace flag for line-to-line backspace too
            
            # Reset everything if we've backspaced to the very beginning
            if char_position == 0 and sentence_position == 0:
                # Reset all counters and timing
                correct_chars = 0
                incorrect_chars = 0
                final_correct_chars = 0
                final_incorrect_chars = 0
                start = None
                wpm = accuracy = seconds = 0
                just_backspaced = False  # Reset backspace flag when starting over
                # Clear WPM display
                ui.updatewpm(wpm_display_window, 0, 0)

        elif letter == '\n':
            # Start a new typing test
            return sentence_mode(window) if not is_paragraph else paragraph_mode(window)

        # Update character highlighting (skip if we just moved to previous line)
        if not moved_to_previous_line:
            highlight_characters(window, center_y, cursor_x_offset, sentence, char_position)
        moved_to_previous_line = False
        window.move(center_y, cursor_x_offset)

    # End of typing test - restore normal input mode and show results
    window.nodelay(False)
    
    # Calculate final WPM and accuracy using final character counts
    if start is not None and final_correct_chars > 0:
        final_seconds = time.time() - start
        # Standard character-based WPM calculation (5 characters per word)
        # This matches industry standards used by MonkeyType, TypeRacer, etc.
        final_wpm = (final_correct_chars / final_seconds / 5) * 60
        final_accuracy = (final_correct_chars / (final_correct_chars + final_incorrect_chars)) * 100
    else:
        final_wpm = wpm
        final_accuracy = accuracy
        final_seconds = seconds
    
    ui.displayinfo(window, final_wpm, final_accuracy, final_seconds, final_correct_chars, final_incorrect_chars, 
                   correct_chars, incorrect_chars, 2 if is_paragraph else 1)


def paragraph_mode(window):
    """
    Initialize and start paragraph mode typing test.
    
    Paragraph mode displays multiple lines of text and allows typing across
    multiple sentences with automatic line wrapping and navigation.
    
    Args:
        window: Curses window for the typing interface
    """
    max_y, max_x = window.getmaxyx()
    center_y, center_x = max_y // 2 - 2, max_x // 4
    col_width = max_x - 2 * center_x
    
    # Generate 3 sentences for paragraph mode
    sentences = [generate_sentence(col_width) for _ in range(3)]
    typing_loop(window, sentences, center_y, center_x, is_paragraph=True)


def sentence_mode(window):
    """
    Initialize and start sentence mode typing test.
    
    Sentence mode displays a single sentence for typing practice.
    
    Args:
        window: Curses window for the typing interface
    """
    max_y, max_x = window.getmaxyx()
    center_y, center_x = max_y // 2, max_x // 4
    col_width = max_x - 2 * center_x
    
    # Generate a single sentence for sentence mode
    sentence = generate_sentence(col_width)
    typing_loop(window, [sentence], center_y, center_x, is_paragraph=False)
