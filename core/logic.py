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


def paragraph_mode(window):
    max_y, max_x = window.getmaxyx()
    window.nodelay(True)
    window.timeout(100)

    center_y, center_x = max_y // 2 - 2, max_x // 4
    col_width = max_x - 2 * center_x

    sentence_list = [generate_sentence(col_width) for _ in range(3)]
    sentence = sentence_list[0]
    posx = posy = 0
    x_offset = center_x
    wordlen = avg_word_length((" ".join(sentence_list)).split())

    wpm = acc = seconds = cch = ich = realcch = realich = 0
    stops = [[0 for _ in s] for s in sentence_list]
    wpmcounter = curses.newwin(1, curses.COLS, center_y - 2, x_offset)

    curses.noecho()
    curses.curs_set(0)
    window.clear()

    draw_sentence_lines(window, sentence_list, center_y, x_offset)
    window.addstr(center_y + 4, x_offset, 'Exit(home/del) | New(enter)', curses.color_pair(int(config.config_parser['default']['colorsession'])))
    highlight_characters(window, center_y, x_offset, sentence, posx)
    window.move(center_y, x_offset)
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

            if posx == len(sentence):
                center_y += 1
                x_offset -= posx
                posx = 0
                posy += 1
                sentence = sentence_list[posy]
                continue

            if letter == sentence[posx]:
                stops[posy][posx] = 1
                color = curses.color_pair(int(config.config_parser['default']['colorcorrect']))
                cch += 1; realcch += 1
            else:
                color = curses.color_pair(int(config.config_parser['default']['colorincorrect']))
                ich += 1; realich += 1

            window.addch(center_y, x_offset, sentence[posx] if sentence[posx] != ' ' or letter != sentence[posx] else letter, color)
            x_offset += 1; posx += 1
            if posx == len(sentence) and posy == 2:
                break

        elif letter == 'KEY_BACKSPACE':
            if posx > 0:
                x_offset, posx, realcch, realich = handle_backspace(window, center_y, x_offset, posx, stops[posy], sentence, realcch, realich)
            elif posx == 0 and posy > 0:
                center_y -= 1
                posy -= 1
                sentence = sentence_list[posy]
                posx = len(sentence)
                x_offset += posx

        elif letter == '\n':
            paragraph_mode(window)

        if posx > 1 and posx != len(sentence) and letter in constants.LETTERS + constants.SPECIAL_CHARS:
            seconds = time.time() - start
            wpm = (cch / seconds / max(1, wordlen)) * 60
            acc = (cch / (cch + ich)) * 100
            ui.updatewpm(wpmcounter, wpm, acc)

        highlight_characters(window, center_y, x_offset, sentence, posx)
        window.move(center_y, x_offset)

    window.nodelay(False)
    ui.displayinfo(window, wpm, acc, seconds, realcch, realich, cch, ich, 2)


def sentence_mode(window):
    max_y, max_x = window.getmaxyx()
    center_y, center_x = max_y // 2, max_x // 4
    col_width = max_x - 2 * center_x

    sentence = generate_sentence(col_width)
    posx = 0
    wordlen = avg_word_length(sentence.split())
    stops = [0 for _ in sentence]

    wpm = acc = seconds = cch = ich = realcch = realich = 0
    wpmcounter = curses.newwin(1, curses.COLS, center_y - 2, center_x)

    window.nodelay(True)
    window.timeout(100)
    window.clear()

    curses.noecho()
    curses.curs_set(0)
    window.addstr(center_y, center_x, sentence)
    highlight_characters(window, center_y, center_x, sentence, posx)
    window.addstr(center_y + 2, center_x, 'Exit(home/del) | New(enter)', curses.color_pair(int(config.config_parser['default']['colorsession'])))
    window.move(center_y, center_x)

    while True:
        try:
            letter = window.getkey()
        except:
            letter = None

        if letter is not None and (letter in constants.LETTERS or letter in " '-"):
            if posx == 0:
                start = time.time()

            if posx >= len(sentence):
                break

            if letter == sentence[posx]:
                stops[posx] = 1
                color = curses.color_pair(int(config.config_parser['default']['colorcorrect']))
                cch += 1; realcch += 1
            else:
                color = curses.color_pair(int(config.config_parser['default']['colorincorrect']))
                ich += 1; realich += 1

            window.addch(center_y, center_x, sentence[posx] if sentence[posx] != ' ' or letter != sentence[posx] else letter, color)
            center_x += 1; posx += 1
            if posx >= len(sentence) and letter:
                break

        elif letter == 'KEY_BACKSPACE' and posx > 0:
            center_x, posx, realcch, realich = handle_backspace(window, center_y, center_x, posx, stops, sentence, realcch, realich)

        elif letter in ('KEY_HOME', 'KEY_DC'):
            ui.menu(window)

        elif letter == '\n':
            sentence_mode(window)

        if posx > 1 and posx != len(sentence) and letter in constants.LETTERS + constants.SPECIAL_CHARS:
            seconds = time.time() - start
            wpm = (cch / seconds / max(1, wordlen)) * 60
            acc = (cch / (cch + ich)) * 100
            ui.updatewpm(wpmcounter, wpm, acc)

        highlight_characters(window, center_y, center_x, sentence, posx)
        window.move(center_y, center_x)

    window.nodelay(False)
    ui.displayinfo(window, wpm, acc, seconds, realcch, realich, cch, ich, 1)