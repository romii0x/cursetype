import curses
import random
import time

with open('1-1000.txt', 'r') as f:
    w1000 = f.read().splitlines()
words_by_num = [[word for word in w1000 if len(word) == i] for i in range(1, 12)]

def generate_sentence(l):
    words = [f'{random.choice(w1000)}' for i in range(l)]
    sentence = ' '.join(words)
    return sentence

def generate_paragraph(l):
    words = [f'{random.choice(w1000)}' for i in range(l*12)]
    paragraph = ' '.join(words)
    firstthird = len(paragraph)//3
    secondthird = firstthird + firstthird
    stop1, stop2 = 0, 0
    for i in range(len(paragraph)):
        if i >= firstthird:
            if paragraph[i:i+1] == ' ':
                stop1 = i
                firstthird = len(paragraph)+1
        elif i >= secondthird:
            if paragraph[i:i+1] == ' ':
                stop2 = i
                break
    return  paragraph, stop1, stop2

def main(window):
    #INIT
    y, x = window.getmaxyx()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    magenta = curses.color_pair(1)
    green = curses.color_pair(2)
    #FUNCTIONS

    def menu(y, x):
        options = [': Zen Mode', ': Paragraph mode', ': Sentence Mode', 'CurseType Menu']
        window.clear()
        for i in range(len(options)):
            window.addstr(y-i, x, options[i])
        pos = [y-2, x]
        window.move(pos[0], pos[1])
        while True:
            key = window.getkey()
            if key == 'KEY_UP':
                if pos[0] > y-2:
                    pos[0] -= 1
                    window.move(pos[0], pos[1])
            elif key == 'KEY_DOWN':
                if pos[0] < y:
                    pos[0] += 1
                    window.move(pos[0], pos[1])
            elif key == '\n':
                if pos[0] == y-2:
                    sentence_mode()
                    break
                elif pos[0] == y-1:
                    paragraph_mode()
                    break
                elif pos[0] == y-0:
                    pass


    def updatewpm(counter, wpm, accuracy):
        counter.clear()
        counter.addstr(0, 0, f'{wpm:.2f}wpm | {accuracy:.2f}%')
        counter.refresh()
    
    def sentence_mode():
        y, x = (window.getmaxyx()[0]//2, window.getmaxyx()[1]//2)
        sentence = generate_sentence(random.randint(10, 15))
        stops = [0 for i in sentence]
        lletters = [chr(i) for i in range(97, 123)]
        uletters = [chr(i) for i in range(65, 91)]
        specialchars = [chr(32), 'KEY_BACKSPACE']
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
        pos = 0
        cch = 0
        ich = 0
        window.clear()
        x -= len(sentence)//2
        window.addstr(y, x, sentence)
        window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
        window.addstr(y, x+1, sentence[pos+1], curses.A_BOLD)
        window.move(y, x)
        curses.echo()
        curses.curs_set(0)
        while True:
            letter = window.getkey()
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in lletters or letter in uletters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if pos == 0:
                    start = time.time()
                # CASE 3: END OF SENTENCE
                if pos > len(sentence)-1:
                    break
                # CORRECT
                if letter == sentence[pos]:
                    stops[pos] = 1
                    window.addstr(y, x, sentence[pos], green)
                    x += 1
                    pos += 1
                    cch += 1
                # INCORRECT
                elif letter != sentence[pos]:
                    if sentence[pos] == ' ':
                        window.addstr(y, x, letter, magenta)
                        x += 1
                        pos += 1
                        ich += 1
                    else:
                        window.addstr(y, x, sentence[pos], magenta)
                        x += 1
                        pos += 1
                        ich += 1
            # CASE 2: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and pos > 0:
                if pos > len(sentence)-1:
                    break
                else:
                    if stops[pos-1] == 0:
                        window.addstr(y, x-1, sentence[pos-1])
                        x -= 1
                        pos -= 1
                    elif stops[pos-1] == 1:
                        stops[pos-1] = 0
                        window.addstr(y, x-1, sentence[pos-1])
                        x -= 1
                        pos -= 1
            # CASE 3: END OF SENTENCE
            elif pos > len(sentence)-1:
                break
            # UPDATE
            if pos > 1:
                seconds = (time.time()-start)
                cchpersecond = cch/seconds
                wps = cchpersecond/5
                wpm = wps*60
                accuracy = (cch/(cch+ich))*100
                realwpm = (len(sentence.split())/seconds)*60
                updatewpm(wpmcounter, wpm, accuracy)
            if pos < len(sentence):
                window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
            if pos < len(sentence)-1:
                window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
                window.addstr(y, x+1, sentence[pos+1], curses.A_BOLD)
            window.refresh()
            window.move(y, x)


        #DISPLAY INFO
        curses.noecho()
        y, x = (window.getmaxyx()[0]//2, window.getmaxyx()[1]//2-10)
        window.clear()
        window.move(y, x)
        results = [f'{seconds:.2f}s ', f'{accuracy:.2f}% ', f'{realwpm:.2f} wpm', f'{wpm:.2f} wpm avg']
        for i in range(len(results)):
            window.addstr(y-i, x, results[i])
        window.getkey()
        curses.curs_set(1)


    def paragraph_mode():
        #INIT
        y, x = (window.getmaxyx()[0]//3, window.getmaxyx()[1]//2)
        sentence = generate_paragraph(3)
        stops = [0 for i in sentence]
        lletters = [chr(i) for i in range(97, 123)]
        uletters = [chr(i) for i in range(65, 91)]
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
        pos = 0
        cch = 0
        ich = 0

        #ADD SENTENCE(S)
        window.clear()
        x -= len(sentence)//2
        window.addstr(y, x, sentence)
        window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
        window.addstr(y, x+1, sentence[pos+1], curses.A_BOLD)
        window.move(y, x)
        curses.echo()
        curses.curs_set(0)
        while True:
            letter = window.getkey()
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in lletters or letter in uletters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if pos == 0:
                    start = time.time()
                # CASE 3: END OF SENTENCE
                if pos > len(sentence)-1:
                    break
                # CORRECT
                if letter == sentence[pos]:
                    stops[pos] = 1
                    window.addstr(y, x, sentence[pos], green)
                    x += 1
                    pos += 1
                    cch += 1
                # INCORRECT
                elif letter != sentence[pos]:
                    if sentence[pos] == ' ':
                        window.addstr(y, x, letter, magenta)
                        x += 1
                        pos += 1
                        ich += 1
                    else:
                        window.addstr(y, x, sentence[pos], magenta)
                        x += 1
                        pos += 1
                        ich += 1
            # CASE 2: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and pos > 0:
                if pos > len(sentence)-1:
                    break
                else:
                    if stops[pos-1] == 0:
                        window.addstr(y, x-1, sentence[pos-1])
                        x -= 1
                        pos -= 1
                    elif stops[pos-1] == 1:
                        stops[pos-1] = 0
                        window.addstr(y, x-1, sentence[pos-1])
                        x -= 1
                        pos -= 1
            # CASE 3: END OF SENTENCE
            elif pos > len(sentence)-1:
                break
            # UPDATE
            if pos > 1:
                seconds = (time.time()-start)
                cchpersecond = cch/seconds
                wps = cchpersecond/5
                wpm = wps*60
                accuracy = (cch/(cch+ich))*100
                realwpm = (len(sentence.split())/seconds)*60
                updatewpm(wpmcounter, wpm, accuracy)
            if pos < len(sentence):
                window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
            if pos < len(sentence)-1:
                window.addstr(y, x, sentence[pos], curses.A_UNDERLINE)
                window.addstr(y, x+1, sentence[pos+1], curses.A_BOLD)
            window.refresh()
            window.move(y, x)


        #DISPLAY INFO
        curses.noecho()
        y, x = (window.getmaxyx()[0]//2, window.getmaxyx()[1]//2-10)
        window.clear()
        window.move(y, x)
        results = [f'{seconds:.2f}s ', f'{accuracy:.2f}% ', f'{realwpm:.2f} wpm', f'{wpm:.2f} wpm avg']
        for i in range(len(results)):
            window.addstr(y-i, x, results[i])
        window.getkey()
        curses.curs_set(1)

    #LOOP
    while True:
        menu(y//2, x//2-10)
    


curses.wrapper(main)