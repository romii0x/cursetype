import curses
import random
import time

with open('1-1000.txt', 'r') as f:
    w1000 = f.read().splitlines()
words_by_num = [[word for word in w1000 if len(word) == i] for i in range(1, 12)]

def main(window):
    #INIT
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
            results = [f'C: {self.realcch} I: {self.realich} M: {self.ich} F: {self.ich-self.realich}', f'{self.seconds:.2f} (s) ', f'{self.acc:.2f} % ', f'{self.wpm:.2f} wpm']
            window.addstr(self.y+1, self.x, 'Menu(q) New(enter)')
            for i in range(len(results)):
                window.addstr(self.y-i, self.x, results[i])
            self.y -= len(results)
            while True:
                key = window.getkey()
                if key == 'q':
                    menu()
                elif key == '\n':
                    if game.mode == 1:
                        sentence_mode()
                    if game.mode == 2:
                        paragraph_mode()
        
        def updatewpm(self, counter):
            counter.clear()
            counter.addstr(0, 0, f'{self.wpm:.2f} wpm | {self.acc:.2f} %')
            counter.refresh()
       
    class Color:
        def __init__(self):
            curses.init_color(1, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000))
            curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(7, 1, curses.COLOR_BLACK)
            self.yellow = curses.color_pair(6)
            self.red = curses.color_pair(5)
            self.cyan = curses.color_pair(4)
            self.blue = curses.color_pair(3)
            self.green = curses.color_pair(2)
            self.magenta  = curses.color_pair(1)
            self.session = curses.color_pair(7)
            self.correct = curses.color_pair(2)
            self.incorrect = curses.color_pair(1)

        def random(self):
            curses.init_color(254, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000))
            curses.init_pair(254, 254, curses.COLOR_BLACK)
            return curses.color_pair(254)

        def randomizesessioncolor(self):
            curses.init_color(1, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000))
            curses.init_pair(7, 1, curses.COLOR_BLACK)
            self.session = curses.color_pair(7)

    color = Color()  
    game = Game()

    def generate_sentence(l):
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

    def menu():
        curses.curs_set(1)
        game.resetyx()
        y, x = game.y//2, game.x//2-10
        y-=1
        window.clear()
        openingmessage = 'Cursetype Console'
        commands = ['sentence', 's', 'paragraph', 'p', 'zen', 'z']
        window.addstr(y, x, openingmessage, color.session)
        window.move(y+1, x-len(openingmessage))
        y+=1
        window.addstr(y, x, '>', color.session)
        x+=1
        start = x
        while True:
            #INPUT
            key = window.getkey()
            #HANDLING
            if key == '\n':
                userinput = ''
                for x in range(start, x):
                    userinput += chr(window.inch(y, x))
                if userinput in commands:
                    if userinput == commands[0]:
                        sentence_mode()
                        menu()
                    if userinput == commands[1]:
                        sentence_mode()
                        menu()
                    if userinput == commands[2]:
                        paragraph_mode()
                        menu()
                    if userinput == commands[3]:
                        paragraph_mode()
                        menu()
            elif key == 'KEY_BACKSPACE':
                window.delch(y, x-1)
                x -= 1
            else:
                window.addstr(y, x, key)
                x += 1
            #OUTPUT
            if start >= x:
                x = start
            window.move(y, max(start, x))

    
    def sentence_mode():
        game.mode = 1
        game.resetyx()
        game.resetstats()
        game.resetpos()
        y, x = game.y//2, game.x//2
        sentence = generate_sentence(game.length)
        stops = [0 for i in sentence]
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
        window.clear()
        x -= len(sentence)//2
        window.addstr(y, x, sentence)
        window.addstr(y, x, sentence[game.posx], curses.A_UNDERLINE)
        window.addstr(y, x+1, sentence[game.posx+1], curses.A_BOLD)
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        while True:
            letter = window.getkey()
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in game.letters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if game.posx == 0:
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
            # CASE 3: END OF SENTENCE
            elif game.posx > len(sentence)-1:
                break
            # UPDATE
            if game.posx > 1:
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
        game.mode = 2
        game.resetyx()
        y, x = game.y//3, game.x//2
        s0 = generate_sentence(game.length)
        s1 = generate_sentence(game.length)
        s2 = generate_sentence(game.length)
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
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        game.end_sentence = False
        while True:
            letter = window.getkey()
            if game.posx == len(sentence) and game.posy == len(sentences)-1:
                break
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in game.letters or letter == chr(32) or letter == chr(39):
                #START AT FIRST LETTER
                if game.posx == 0 and game.posy == 0:
                    start = time.time()
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

            
            
            # UPDATE
            if game.posx > 1 and game.posx != len(sentence) and game.end_sentence == False:
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