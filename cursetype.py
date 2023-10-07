import curses
import random
import time

with open('1-1000.txt', 'r') as f:
    w1000 = f.read().splitlines()
words_by_num = [[word for word in w1000 if len(word) == i] for i in range(1, 12)]

def main(window):
    #INIT
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    class Game:
        def __init__(self):
            self.letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]  
            self.y = window.getmaxyx()[0]
            self.x = window.getmaxyx()[1]
            self.length = 80
            self.posx = 0
            self.posy = 0
            self.end_sentence = False
            self.mode = 0
            self.wpm = 0; self.acc =  0; self.seconds = 0; self.cch = 0; self.ich = 0; self.realcch = 0; self.realich = 0

        def resetstats(self):
            self.wpm = 0; self.acc =  0; self.seconds = 0; self.cch = 0; self.ich = 0; self.realcch = 0; self.realich = 0

        def resetpos(self):
            self.posx = 0; self.posy = 0

        def resetyx(self):
            self.y = window.getmaxyx()[0]
            self.x = window.getmaxyx()[1]
        
        def centeryx(self):
            self.y = window.getmaxyx()[0]//2
            self.x = window.getmaxyx()[1]//2
     
        def displayinfo(self):
            self.centeryx()
            self.x -= 10
            window.clear()
            window.move(self.y, self.x) 
            window.addstr(self.y+1, self.x, 'Menu(home) New(enter)', color.session)
            window.addstr(self.y-3, self.x, f'{self.wpm:.2f} wpm', curses.color_pair(color.indicators[int(self.wpm)//10-1]))
            window.addstr(self.y-2, self.x, f'{self.acc:.2f} % ', curses.color_pair(color.indicators[int(self.acc)//10-1]))
            window.addstr(self.y-1, self.x, f'{self.seconds:.2f} (s) ')
            window.addstr(self.y, self.x, f'C: {self.realcch} I: {self.realich} M: {self.ich} F: {self.ich-self.realich}')
            self.y -= 3
            while True:
                key = window.getkey()
                if key == 'KEY_HOME':
                    menu()
                elif key == '\n':
                    if game.mode == 1:
                        sentence_mode()
                    if game.mode == 2:
                        paragraph_mode()
        
        def consolemessage(self, display, message):
            display.addstr(0, 0, message)
            display.refresh()

        def generate_sentence(self, l):
            sentence = []
            slen = 0
            while True:
                word = random.choice(w1000)
                if slen + len(word)+1 < l:
                    sentence.append(word)
                    slen += len(word)+1
                elif slen + len(word)+1 > l:
                    return ' '.join(sentence)
                    break
                elif slen + len(word)+1 == l:
                    sentence.append(word)
                    slen += len(word)+1
                    return ' '.join(sentence)
                    break
        
        def updatewpm(self, counter):
            counter.clear()
            if self.wpm < 200:
                counter.addstr(0, 0, f'{self.wpm:.2f} wpm ', curses.color_pair(color.indicators[max((int(self.wpm)//10-1), 0)]))
                counter.addstr(0, 11, f'| {self.acc:.2f} %', curses.color_pair(color.indicators[max(int((self.acc//10)-1), 0)]))
            else:
                counter.addstr(0, 0, f'{self.wpm:.2f} wpm ')
                counter.addstr(0, 11, f'| {self.acc:.2f} %', curses.color_pair(color.indicators[int(self.acc*2)//10-1]))
            counter.refresh()      
    class Color:
        def __init__(self):
            self.seed = random.randint(0, 232)
            self.red = curses.color_pair(10)
            self.green = curses.color_pair(11)
            self.yellow = curses.color_pair(12)
            self.blue = curses.color_pair(13)
            self.hotpink = curses.color_pair(14)
            self.cyan = curses.color_pair(15)
            self.plum = curses.color_pair(91)
            self.periwinkle = curses.color_pair(70)
            self.magenta = curses.color_pair(166)
            self.lavender = curses.color_pair(100)
            self.seafoam = curses.color_pair(123)
            self.lime = curses.color_pair(155)
            self.mint = curses.color_pair(160)
            self.peach = curses.color_pair(205)
            self.salmon = curses.color_pair(212)
            self.teal = curses.color_pair(32)
            self.correct = curses.color_pair(11)
            self.incorrect = curses.color_pair(10)
            self.session = curses.color_pair(self.seed)
            #self.indicators = [x for x in range(160, 154, -1)]+[x for x in range(227, 202, -6)]+[x for x in range(197, 202)]+[166, 130, 136, 142, 58]
            self.indicators = [10, 10, 197, 203, 215, 227, 191, 155, 119, 122, 124, 82, 76, 70, 64, 100, 142, 184, 226, 254]

        def random(self):
            self.seed = random.randint(0, 232)
            return curses.color_pair(c)

        def randomizesessioncolor(self):
            curses.init_color(1, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000))
            curses.init_pair(1, 1, curses.COLOR_BLACK)
            self.session = curses.color_pair(7)

    color = Color()  
    game = Game()

    def menu():
        curses.curs_set(1)
        game.resetyx()
        game.resetpos()
        window.clear()
        openingmessage = f'CurseType Console'
        errormessage = 'Not understood. Try typing "help" or "sentence"'
        y, x = game.y//2, game.x//2-len(openingmessage)//2
        commands = ['quit', 'sentence', 's', 'paragraph', 'p', 'help']
        window.addstr(y-1, x, openingmessage, color.session)
        window.move(y, x)
        window.addstr(y, x, '>', color.session)
        x+=1
        start = x
        displayline = curses.newwin(1, curses.COLS, y+1, start)
        window.nodelay(1)
        window.timeout(100)
        window.refresh()
        tick = 0
        errortick = 0
        while True:
            #INPUT
            try:
                key = window.getkey()
            except:
                key = None
                tick += 1
            #HANDLING
            if key == '\n':
                userinput = ''
                for i in range(start, x):
                    userinput += chr(window.inch(y, i) & 0xFF)
                if userinput in commands:
                    if userinput == commands[0]:
                        exit()
                    elif userinput == commands[1]:
                        sentence_mode()
                    elif userinput == commands[2]:
                        sentence_mode()
                    elif userinput == commands[3]:
                        paragraph_mode()
                    elif userinput == commands[4]:
                        paragraph_mode()
                else:
                    for i in range(len(userinput)+1):
                        window.delch(y, x)
                        x -= 1
                    game.consolemessage(displayline, errormessage)
                    errortick = tick
                    window.move(y, max(start, x))

            elif key == 'KEY_BACKSPACE':
                if start < x:
                    window.delch(y, x-1)
                    x -= 1
                    window.move(y, max(start, x))
            elif key in game.letters or key == chr(32):
                window.addstr(y, x, key, color.session)
                x += 1
                window.move(y, max(start, x))

            #OUTPUT
            if tick < errortick+22 and tick > errortick+20:
                displayline.clear()
                displayline.refresh()
                window.move(y, max(start, x))
            if start >= x:
                x = start

    def settings():
        window.clear()
        game.resetyx()
        y, x = game.y, game.x



    def sentence_mode():
        window.nodelay(0)
        game.mode = 1
        game.resetyx()
        game.resetstats()
        game.resetpos()
        y, x = game.y//2, game.x//2
        sentence = game.generate_sentence(game.length)
        stops = [0 for i in sentence]
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
        window.clear()
        x -= len(sentence)//2
        window.addstr(y, x, sentence)
        window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE)
        window.addstr(y, x+1, sentence[game.posx+1], curses.A_BOLD)
        window.addstr(y+2, x, 'Exit(home) | New(enter)')
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        while True:
            letter = window.getkey()
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in game.letters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if game.posx == 0:
                    game.cch = 0
                    game.ich = 0
                    start = time.time()
                # CASE 3: END OF SENTENCE
                if game.posx > len(sentence)-1:
                    break
                # CORRECT
                if letter == sentence[game.posx]:
                    stops[game.posx] = 1
                    window.addstr(y, x, sentence[game.posx], color.correct)
                    x += 1
                    game.posx += 1
                    game.cch += 1
                    game.realcch += 1
                # INCORRECT
                elif letter != sentence[game.posx]:
                    if sentence[game.posx] == ' ':
                        window.addstr(y, x, letter, color.incorrect)
                        x += 1
                        game.posx += 1
                        game.ich += 1
                        game.realich += 1
                    else:
                        window.addstr(y, x, sentence[game.posx], color.incorrect)
                        x += 1
                        game.posx += 1
                        game.ich += 1
                        game.realich += 1
            # CASE 2: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and game.posx > 0:
                if game.posx > len(sentence)-1:
                    break
                else:
                    if stops[game.posx-1] == 0:
                        window.addstr(y, x-1, sentence[game.posx-1])
                        x -= 1
                        game.posx -= 1
                        game.realich -= 1
                    elif stops[game.posx-1] == 1:
                        stops[game.posx-1] = 0
                        window.addstr(y, x-1, sentence[game.posx-1])
                        x -= 1
                        game.posx -= 1
                        game.realcch -= 1
            
            elif letter == 'KEY_HOME':
                menu()
            # CASE 3: END OF SENTENCE
            elif game.posx > len(sentence)-1:
                break
            elif letter == '\n':
                sentence_mode()
            # UPDATE
            if game.posx > 1 and game.posx != len(sentence) and letter in game.letters:
                game.seconds = (time.time()-start)
                cchpersecond = game.cch/game.seconds
                wps = cchpersecond/5
                game.wpm = wps*60
                game.acc = (game.cch/(game.cch+game.ich))*100
                game.updatewpm(wpmcounter)
            if game.posx < len(sentence):
                window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE)
            if game.posx < len(sentence)-1:
                window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE)
                window.addstr(y, x+1, sentence[game.posx+1], curses.A_BOLD)
            window.refresh()
            window.move(y, x)


        #DISPLAY INFO
        game.displayinfo()

    def paragraph_mode():
        #INIT
        window.nodelay(0)
        game.mode = 2
        game.resetyx()
        y, x = game.y//3, game.x//2
        s0 = game.generate_sentence(game.length)
        s1 = game.generate_sentence(game.length)
        s2 = game.generate_sentence(game.length)
        sentence = s0
        sentences = [s0, s1, s2]
        stops = [[0 for i in s0], [0 for i in s1], [0 for i in s2]]  
        game.resetpos()
        game.resetstats()
        window.clear()
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)  
        x -= len(sentence)//2
        window.addstr(y, x, sentence) 
        window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE) #POS MARKER
        window.addstr(y, x+1, sentence[game.posx+1], curses.A_BOLD)
        window.addstr(y+1, x, s1) 
        window.addstr(y+2, x, s2)
        window.addstr(y+4, x, 'Exit(home) | New(enter)')
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        game.end_sentence = False
        window.refresh()
        while True:
            letter = window.getkey()
            if letter == 'KEY_HOME':
                menu()
            if game.posx == len(sentence) and game.posy == len(sentences)-1:
                break
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in game.letters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if game.posx == 0 and game.posy == 0:
                    start = time.time()
                    game.cch = 0
                    game.ich = 0
                # CASE 2: END OF SENTENCE
                if game.posx == len(sentence):
                    y += 1
                    x -= game.posx
                    game.posx = 0
                    game.end_sentence = True
                    if game.posy == 2:
                        break
                    elif game.posy == 1:
                        sentence = s2
                        game.posy = 2
                    elif game.posy == 0:
                        sentence = s1
                        game.posy = 1
                # CORRECT
                if letter == sentence[game.posx] and game.end_sentence == False:
                    stops[game.posy][game.posx] = 1
                    window.addstr(y, x, sentence[game.posx], color.correct)
                    x += 1
                    game.posx += 1
                    game.cch += 1
                    game.realcch += 1
                # INCORRECT
                elif letter != sentence[game.posx] and game.end_sentence == False:
                    if sentence[game.posx] == ' ':
                        window.addstr(y, x, letter, color.incorrect)
                        x += 1
                        game.posx += 1
                        game.ich += 1
                        game.realich += 1
                    else:
                        window.addstr(y, x, sentence[game.posx], color.incorrect)
                        x += 1
                        game.posx += 1
                        game.ich += 1
                        game.realich += 1
            # CASE 3: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and game.posx > 0:
                if game.posx == len(sentence):
                    window.addstr(y, x-1, sentence[game.posx-1])
                    x -= 1
                    game.posx -= 1
                else:
                    if stops[game.posy][game.posx-1] == 0:
                        window.addstr(y, x-1, sentence[game.posx-1])
                        x -= 1
                        game.posx -= 1
                        game.realich -= 1
                    elif stops[game.posy][game.posx-1] == 1:
                        stops[game.posy][game.posx-1] = 0
                        window.addstr(y, x-1, sentence[game.posx-1])
                        x -= 1
                        game.posx -= 1
                        game.realcch -= 1
            elif letter == 'KEY_BACKSPACE' and game.posx == 0 and game.posy > 0:
                game.end_sentence = True
                window.addstr(y, x, sentence[game.posx])
                y -= 1
                game.posy -= 1
                sentence = sentences[game.posy]
                game.posx = len(sentence)
                x += len(sentence)
            
            elif letter == '\n':
                paragraph_mode()
            
            # UPDATE
            if game.posx > 1 and game.posx != len(sentence) and game.end_sentence == False and letter in game.letters:
                game.seconds = (time.time()-start)
                cchpersecond = game.cch/game.seconds
                game.wpm = (cchpersecond/5)*60
                game.acc = (game.cch/(game.cch+game.ich))*100
                game.updatewpm(wpmcounter)
            if game.posx < len(sentence):
                window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE)
                if game.posx < len(sentence)-1:
                    window.addstr(y, x+1, sentence[game.posx+1], curses.A_BOLD)
            #INIT NEXT 
            game.end_sentence = False
            window.refresh()
            window.move(y, x)


        #DISPLAY INFO
        game.displayinfo()


    #LOOP
    while True:
        menu()
    


curses.wrapper(main)