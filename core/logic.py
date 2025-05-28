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


def highlight_characters(window, y, x, sentence, posx):
    if posx < len(sentence):
        window.addch(y, x, sentence[posx], curses.A_UNDERLINE)
        if posx + 1 < len(sentence):
            window.addch(y, x + 1, sentence[posx + 1], curses.A_BOLD)


def handle_backspace(window, y, x, posx, stops, sentence, realcch, realich):
    if stops[posx - 1] == 0:
        realich -= 1
    else:
        realcch -= 1
        stops[posx - 1] = 0
    window.addch(y, x - 1, sentence[posx - 1])
    return x - 1, posx - 1, realcch, realich


def typing_loop(window, sentences, center_y, center_x, is_paragraph):
    col_width = curses.COLS - 2 * center_x
    posx = posy = 0
    x_offset = center_x
    sentence = sentences[0]
    wordlen = avg_word_length(" ".join(sentences).split())

    cch = ich = realcch = realich = 0
    stops = [[0 for _ in s] for s in sentences]
    wpm = acc = seconds = 0
    start = None
    wpmcounter = curses.newwin(1, curses.COLS, center_y - 2, center_x)

    window.nodelay(True)
    window.timeout(100)
    curses.noecho()
    curses.curs_set(0)
    window.clear()

    draw_sentence_lines(window, sentences, center_y, center_x)
    window.addstr(center_y + (len(sentences) + 1), center_x, 'Exit(home/del) | New(enter)', curses.color_pair(int(config.config_parser['default']['colorsession'])))
    highlight_characters(window, center_y, center_x, sentence, posx)
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
            if posx == 0 and posy == 0:
                start = time.time()

            if posx >= len(sentence):
                if is_paragraph and posy < len(sentences) - 1:
                    center_y += 1
                    x_offset -= posx
                    posx = 0
                    posy += 1
                    sentence = sentences[posy]
                    continue
                else:
                    break

            expected_char = sentence[posx]
            is_correct = letter == expected_char
            color_correct = curses.color_pair(int(config.config_parser['default']['colorcorrect']))
            color_incorrect = curses.color_pair(int(config.config_parser['default']['colorincorrect']))
            stops[posy][posx] = 1 if is_correct else 0

            if is_correct:
                cch += 1
                realcch += 1
                window.addch(center_y, x_offset, expected_char, color_correct)
            else:
                ich += 1
                realich += 1
                if expected_char == ' ' and letter != ' ':
                    window.addch(center_y, x_offset, letter, color_incorrect)
                elif expected_char != ' ' and letter == ' ':
                    window.addch(center_y, x_offset, expected_char, color_incorrect)
                else:
                    window.addch(center_y, x_offset, letter, color_incorrect)
            x_offset += 1
            posx += 1

            if posx >= len(sentence) and posy == len(sentences) - 1:
                break

        elif letter == 'KEY_BACKSPACE':
            if posx > 0:
                x_offset, posx, realcch, realich = handle_backspace(window, center_y, x_offset, posx, stops[posy], sentence, realcch, realich)
            elif posx == 0 and posy > 0:
                posy -= 1
                sentence = sentences[posy]
                posx = len(sentence)
                center_y -= 1
                x_offset += posx

        elif letter == '\n':
            return sentence_mode(window) if not is_paragraph else paragraph_mode(window)

        if posx > 1 and posx != len(sentence) and letter in constants.LETTERS + constants.SPECIAL_CHARS:
            seconds = time.time() - start
            wpm = (cch / seconds / max(1, wordlen)) * 60
            acc = (cch / (cch + ich)) * 100
            ui.updatewpm(wpmcounter, wpm, acc)

        highlight_characters(window, center_y, x_offset, sentence, posx)
        window.move(center_y, x_offset)

    window.nodelay(False)
    ui.displayinfo(window, wpm, acc, seconds, realcch, realich, cch, ich, 2 if is_paragraph else 1)


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
