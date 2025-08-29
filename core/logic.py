import curses, random, time
from core import constants, ui, config


def avg_word_length(words):
    return sum(len(word) for word in words) / len(words)


def generate_sentence(length):
    sentence = []
    current_length = 0
    while True:
        word = random.choice(constants.WORDS)
        if current_length + len(word) + 1 < length:
            sentence.append(word)
            current_length += len(word) + 1
        elif current_length + len(word) + 1 == length:
            sentence.append(word)
            return ' '.join(sentence)
        else:
            return ' '.join(sentence)


def draw_sentence_lines(window, sentences, start_y, start_x):
    for idx, line in enumerate(sentences):
        window.addstr(start_y + idx, start_x, line)


def highlight_characters(window, y, x, sentence, char_position):
    if char_position < len(sentence):
        window.addch(y, x, sentence[char_position], curses.A_UNDERLINE | curses.A_BOLD)


def handle_backspace(window, y, x, char_position, stops, sentence, final_correct_chars, final_incorrect_chars):
    if stops[char_position - 1] == 0:
        final_incorrect_chars -= 1
    else:
        final_correct_chars -= 1
        stops[char_position - 1] = 0
    window.addch(y, x - 1, sentence[char_position - 1])
    return x - 1, char_position - 1, final_correct_chars, final_incorrect_chars


def typing_loop(window, sentences, center_y, center_x, is_paragraph):
    col_width = curses.COLS - 2 * center_x
    char_position = sentence_position = 0
    cursor_x_offset = center_x
    sentence = sentences[0]
    average_word_length = avg_word_length(" ".join(sentences).split())

    correct_chars = 0
    incorrect_chars = 0
    final_correct_chars = 0
    final_incorrect_chars = 0
    stops = [[0 for _ in s] for s in sentences]
    wpm = accuracy = seconds = 0
    start = None
    wpm_display_window = curses.newwin(1, curses.COLS, center_y - 2, center_x)

    window.nodelay(True)
    window.timeout(100)
    curses.noecho()
    curses.curs_set(0)
    window.clear()

    draw_sentence_lines(window, sentences, center_y, center_x)
    window.addstr(center_y + (len(sentences) + 1), center_x, 'Exit(home/del) | New(enter)', curses.color_pair(int(config.config_parser['default']['colorsession'])))
    highlight_characters(window, center_y, center_x, sentence, char_position)
    window.move(center_y, center_x)
    window.refresh()

    while True:
        try:
            letter = window.getkey()
        except:
            letter = None

        if letter in ('KEY_HOME', 'KEY_DC'):
            ui.menu(window)

        if letter is not None and (letter in constants.LETTERS or letter in " '-"):
            if char_position == 0 and sentence_position == 0:
                start = time.time()

            if char_position >= len(sentence):
                if is_paragraph and sentence_position < len(sentences) - 1:
                    center_y += 1
                    cursor_x_offset -= char_position
                    char_position = 0
                    sentence_position += 1
                    sentence = sentences[sentence_position]
                    continue
                else:
                    break

            expected_char = sentence[char_position]
            is_correct = letter == expected_char
            color_correct = curses.color_pair(int(config.config_parser['default']['colorcorrect']))
            color_incorrect = curses.color_pair(int(config.config_parser['default']['colorincorrect']))
            stops[sentence_position][char_position] = 1 if is_correct else 0

            if is_correct:
                correct_chars += 1
                final_correct_chars += 1
                window.addch(center_y, cursor_x_offset, expected_char, color_correct)
            else:
                incorrect_chars += 1
                final_incorrect_chars += 1
                if expected_char == ' ' and letter != ' ':
                    window.addch(center_y, cursor_x_offset, letter, color_incorrect)
                elif expected_char != ' ' and letter == ' ':
                    window.addch(center_y, cursor_x_offset, expected_char, color_incorrect)
                else:
                    window.addch(center_y, cursor_x_offset, letter, color_incorrect)
            cursor_x_offset += 1
            char_position += 1

            if char_position >= len(sentence) and sentence_position == len(sentences) - 1:
                break

        elif letter == 'KEY_BACKSPACE':
            if char_position > 0:
                cursor_x_offset, char_position, final_correct_chars, final_incorrect_chars = handle_backspace(window, center_y, cursor_x_offset, char_position, stops[sentence_position], sentence, final_correct_chars, final_incorrect_chars)
            elif char_position == 0 and sentence_position > 0:
                sentence_position -= 1
                sentence = sentences[sentence_position]
                char_position = len(sentence)
                center_y -= 1
                cursor_x_offset += char_position

        elif letter == '\n':
            return sentence_mode(window) if not is_paragraph else paragraph_mode(window)

        if char_position > 1 and char_position != len(sentence) and letter in constants.LETTERS + constants.SPECIAL_CHARS:
            seconds = time.time() - start
            wpm = (correct_chars / seconds / max(1, average_word_length)) * 60
            accuracy = (correct_chars / (correct_chars + incorrect_chars)) * 100
            ui.updatewpm(wpm_display_window, wpm, accuracy)

        highlight_characters(window, center_y, cursor_x_offset, sentence, char_position)
        window.move(center_y, cursor_x_offset)

    window.nodelay(False)
    ui.displayinfo(window, wpm, accuracy, seconds, final_correct_chars, final_incorrect_chars, correct_chars, incorrect_chars, 2 if is_paragraph else 1)


def paragraph_mode(window):
    max_y, max_x = window.getmaxyx()
    center_y, center_x = max_y // 2 - 2, max_x // 4
    col_width = max_x - 2 * center_x
    sentences = [generate_sentence(col_width) for _ in range(3)]
    typing_loop(window, sentences, center_y, center_x, is_paragraph=True)


def sentence_mode(window):
    max_y, max_x = window.getmaxyx()
    center_y, center_x = max_y // 2, max_x // 4
    col_width = max_x - 2 * center_x
    sentence = generate_sentence(col_width)
    typing_loop(window, [sentence], center_y, center_x, is_paragraph=False)
