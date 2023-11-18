#  ▄▄· ▄• ▄▌▄▄▄  .▄▄ · ▄▄▄ .▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▄▄▄ .
# ▐█ ▌▪█▪██▌▀▄ █·▐█ ▀. ▀▄.▀·•██  ▐█▪██▌▐█ ▄█▀▄.▀·
# ██ ▄▄█▌▐█▌▐▀▀▄ ▄▀▀▀█▄▐▀▀▪▄ ▐█.▪▐█▌▐█▪ ██▀·▐▀▀▪▄
# ▐███▌▐█▄█▌▐█•█▌▐█▄▪▐█▐█▄▄▌ ▐█▌· ▐█▀·.▐█▪·•▐█▄▄▌
# ·▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀▀  ▀▀▀  ▀▀▀   ▀ • .▀    ▀▀▀        
# author: https://github.com/ianshapiro1
# 
# Oxford 3/5000 from https://github.com/tgmgroup/Word-List-from-Oxford-Longman-5000
# 1000 most common US words from https://gist.github.com/deekayen/4148741
# ASCII text art from http://www.patorjk.com/software/taag 

import curses
import random
import time

def main(window):
    
    class Game:
        def __init__(self):
            self.w1000 = open('1-1000.txt', 'r').read().splitlines()
            self.wordlen = 0
            self.letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]  
            self.y = window.getmaxyx()[0]
            self.x = window.getmaxyx()[1]
            self.length = self.x//2
            self.posx = 0
            self.posy = 0
            self.commands = ['quit', 'q', 'sentence', 's', 'paragraph', 'p', 'help', 'settings', 'c']
            self.openingmessage = 'Welcome to CurseType! Type "sentence" or "help" and press enter.'
            self.consolebanner = f'CurseType Console'
            self.errormessage = 'Not understood. Type "help" for a list of commands.'
            self.ency = open('guide.txt', 'r').read().splitlines()
            self.specialchars = [chr(39), chr(32), chr(45), 'KEY_BACKSPACE']
            self.settings = ['color', 'vocabulary']
            self.settingscolor = ['correct letter', 'incorrect letter', 'menu color']
            self.settingsdifficulty = ['common words', 'oxford 3000', 'oxford 5000']
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

        def setgamedifficulty(self, difficulty):
            if difficulty == 0:
                with open('1-1000.txt', 'r') as f1:
                    self.w1000 = f1.read().splitlines()
            elif difficulty == 1:
                with open('1-1000.txt', 'r') as f1, open('o3000.txt', 'r') as f2:
                    self.w1000 = f1.read().splitlines()
                    self.w1000 += f2.read().splitlines()
            elif difficulty == 2:
                with open('o5000.txt', 'r') as f1, open('1-1000.txt', 'r') as f2, open('o3000.txt', 'r') as f3:
                    self.w1000 = f1.read().splitlines()
                    self.w1000 += f2.read().splitlines()
                    self.w1000 += f3.read().splitlines()

        def settingsdifficultymenu(self):
            window.clear()
            self.resetyx()
            y, x = self.y//2, self.x//2
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(0)
            option = 0
            #init screen content
            y -= len(self.settingsdifficulty)//2
            textstart = y
            def sdminit(y, x, o):
                window.addstr(y+len(self.settingsdifficulty)+1, x, 'Back(home/del) | Select(enter)', color.session)
                for i in range(len(self.settingsdifficulty)):
                    if i == option:
                        window.addstr(y, x, self.settingsdifficulty[i], curses.A_REVERSE)
                    else:
                        window.addstr(y, x, self.settingsdifficulty[i], color.session)
                    y += 1
            sdminit(y, x, option)
            y -= len(self.settingsdifficulty)
            starty = y
            maxy = y+len(self.settingsdifficulty)-1
            window.move(y, x)
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= 1
                        window.clear()
                        sdminit(textstart, x, option)
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += 1
                        window.clear()
                        sdminit(textstart, x, option)
                elif key == '\n':
                    if option == 0:
                        #menu color
                        self.setgamedifficulty(0)
                        window.addstr(textstart-3, x, f'Set to {game.settingsdifficulty[0]}')
                        
                    elif option == 1:
                        #correct
                        self.setgamedifficulty(1)
                        window.addstr(textstart-3, x, f'Set to {game.settingsdifficulty[1]}')
                    elif option == 2:
                        #incorrect
                        self.setgamedifficulty(2)
                        window.addstr(textstart-3, x, f'Set to {game.settingsdifficulty[2]}')
                
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.settingsmainmenu()
                    #init next screen
                #init next
                window.move(y, x)
            #end

        def setincorrectcolor(self):
            window.clear()
            self.resetyx()
            y, x = self.y//3, self.x//5
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(1)
            starty = y
            startx = x
            maxx = int(self.x-(1/5*self.x))
            screenrange = maxx-startx
            #init screen content
            for i in range(0, curses.COLORS):
                if x < maxx:
                    window.addstr(y, x, '0', curses.color_pair(i+1))
                    x += 1
                else:
                    x = self.x//5
                    y += 1
            maxy = y
            option = 1
            window.move(starty, startx)
            y, x = starty, startx
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= screenrange+1
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += screenrange+1
                elif key == 'KEY_LEFT':
                    if x != startx:
                        x -= 1
                        option -= 1
                elif key == 'KEY_RIGHT':
                    if x != maxx:
                        x += 1
                        option += 1
                elif key == '\n':
                    color.incorrect = curses.color_pair(option)
                    self.settingscolormenu()
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.settingscolormenu()

                #init next
                window.move(y, x)
            #end

        def setcorrectcolor(self):
            window.clear()
            self.resetyx()
            y, x = self.y//3, self.x//5
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(1)
            starty = y
            startx = x
            maxx = int(self.x-(1/5*self.x))
            screenrange = maxx-startx
            #init screen content
            for i in range(0, curses.COLORS):
                if x < maxx:
                    window.addstr(y, x, '0', curses.color_pair(i+1))
                    x += 1
                else:
                    x = self.x//5
                    y += 1
            maxy = y
            option = 1
            window.move(starty, startx)
            y, x = starty, startx
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= screenrange+1
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += screenrange+1
                elif key == 'KEY_LEFT':
                    if x != startx:
                        x -= 1
                        option -= 1
                elif key == 'KEY_RIGHT':
                    if x != maxx:
                        x += 1
                        option += 1
                elif key == '\n':
                    color.correct = curses.color_pair(option)
                    self.settingscolormenu()
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.settingscolormenu()

                #init next
                window.move(y, x)
            #end

        def setmenucolor(self):
            window.clear()
            self.resetyx()
            y, x = self.y//3, self.x//5
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(1)
            starty = y
            startx = x
            maxx = int(self.x-(1/5*self.x))
            screenrange = maxx-startx
            #init screen content
            for i in range(0, curses.COLORS):
                if x < maxx:
                    window.addstr(y, x, '0', curses.color_pair(i+1))
                    x += 1
                else:
                    x = self.x//5
                    y += 1
            maxy = y
            option = 1
            window.move(starty, startx)
            y, x = starty, startx
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= screenrange+1
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += screenrange+1
                elif key == 'KEY_LEFT':
                    if x != startx:
                        x -= 1
                        option -= 1
                elif key == 'KEY_RIGHT':
                    if x != maxx:
                        x += 1
                        option += 1
                elif key == '\n':
                    color.session = curses.color_pair(option)
                    self.settingscolormenu()
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.settingscolormenu()

                #init next
                window.move(y, x)
            #end

        def settingscolormenu(self):
            window.clear()
            self.resetyx()
            y, x = self.y//2, self.x//2
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(0)
            option = 0
            #init screen content
            y -= len(self.settingscolor)//2
            textstart = y
            def scminit(y, x, o):
                window.addstr(y+len(self.settingscolor)+1, x, 'Back(home/del) | Select(enter)', color.session)
                for i in range(len(self.settingscolor)):
                    if i == option:
                        window.addstr(y, x, self.settingscolor[i], curses.A_REVERSE)
                    else:
                        window.addstr(y, x, self.settingscolor[i], color.session)
                    y += 1
            scminit(y, x, option)
            y -= len(self.settingscolor)
            starty = y
            maxy = y+len(self.settingscolor)-1
            window.move(y, x)
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= 1
                        window.clear()
                        scminit(textstart, x, option)
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += 1
                        window.clear()
                        scminit(textstart, x, option)
                elif key == '\n':
                    if option == 0:
                        #menu color
                        self.setcorrectcolor()
                    elif option == 1:
                        #correct
                        self.setincorrectcolor()
                    elif option == 2:
                        #incorrect
                        self.setmenucolor()
                
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.settingsmainmenu()
                    #init next screen
                #init next
                window.move(y, x)
            #end

        def settingsmainmenu(self):
            window.clear()
            self.resetyx()
            y, x = self.y//2, self.x//2
            window.nodelay(1)
            window.timeout(100)
            curses.curs_set(0)
            #init screen content
            y -= len(self.settings)//2
            option = 0
            textstart = y
            def smminit(y, x, o):
                window.addstr(y+len(self.settings)+1, x, 'Back(home/del) | Select(enter)', color.session)
                for i in range(len(self.settings)):
                    if i == option:
                        window.addstr(y, x, self.settings[i], curses.A_REVERSE)
                    else:
                        window.addstr(y, x, self.settings[i], color.session)
                    y += 1
            smminit(y, x, option)
            y -= len(self.settings)
            starty = y
            maxy = y+len(self.settings)-1
            window.move(y, x)
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES
                if key == 'KEY_UP':
                    if y != starty:
                        y -= 1
                        option -= 1
                        window.clear()
                        smminit(textstart, x, option)
                elif key == 'KEY_DOWN':
                    if y != maxy:
                        y += 1
                        option += 1
                        window.clear()
                        smminit(textstart, x, option)
                elif key == '\n':
                    if option == 0:
                        self.settingscolormenu()
                    elif option == 1:
                        self.settingsdifficultymenu()
                
                elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                    self.menu()
                #init next
                window.move(y, x)
            #end

        def displayinfo(self):
            self.centeryx()
            self.x -= 10
            window.clear()
            window.move(self.y, self.x) 
            window.addstr(self.y+1, self.x, 'Menu(home/del) New(enter)', color.session)
            window.addstr(self.y-3, self.x, f'{self.wpm:.2f} wpm', curses.color_pair(color.indicators[int(self.wpm)//10-1]))
            window.addstr(self.y-2, self.x, f'{self.acc:.2f} % ', curses.color_pair(color.indicators[int(self.acc)//10-1]))
            window.addstr(self.y-1, self.x, f'{self.seconds:.2f} (s) ')
            window.addstr(self.y, self.x, f'C: {self.realcch} I: {self.realich} M: {self.ich} F: {self.ich-self.realich}')
            self.y -= 3
            while True:
                key = window.getkey()
                if key == 'KEY_HOME' or key == 'KEY_DC':
                    self.menu()
                elif key == '\n':
                    if game.mode == 1:
                        self.sentence_mode()
                    if game.mode == 2:
                        self.paragraph_mode()
        
        def consolemessage(self, display, message, y, x):
            display.addstr(y, x, message, color.session)
            display.refresh()

        def generate_sentence(self, l):
            sentence = []
            slen = 0
            while True:
                word = random.choice(self.w1000)
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
        
        def avgwordlength(self, sentencelist):
            l = 0
            n = 0
            for w in sentencelist:
                l += len(w)
                n += 1
            return l/n
        
        def updatewpm(self, counter):
            counter.clear()
            if self.wpm < 200:
                counter.addstr(0, 0, f'{self.wpm:.2f} wpm ', curses.color_pair(color.indicators[max((int(self.wpm)//10-1), 0)]))
                counter.addstr(0, 11, f'| {self.acc:.2f} %', curses.color_pair(color.indicators[max(int((self.acc//10)-1), 0)]))
            else:
                counter.addstr(0, 0, f'{self.wpm:.2f} wpm ')
                counter.addstr(0, 11, f'| {self.acc:.2f} %', curses.color_pair(color.indicators[int(self.acc*2)//10-1]))
            counter.refresh()
   
        def paragraph_mode(self):
            #INIT
            window.nodelay(1)
            window.timeout(100)
            self.mode = 2
            self.resetyx()
            y, x = self.y//2-2, self.x//2
            s0 = self.generate_sentence(self.length)
            s1 = self.generate_sentence(self.length)
            s2 = self.generate_sentence(self.length)
            sentence = s0
            sentences = [s0, s1, s2]
            self.wordlen = self.avgwordlength((s0+s1+s2).split())
            stops = [[0 for i in s0], [0 for i in s1], [0 for i in s2]]  
            self.resetpos()
            self.resetstats()
            window.clear()
            wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)  
            x -= len(sentence)//2
            window.addstr(y, x, sentence) 
            window.addstr(y, x, sentence[self.posx], curses.A_UNDERLINE) #POS MARKER
            window.addstr(y, x+1, sentence[self.posx+1], curses.A_BOLD)
            window.addstr(y+1, x, s1) 
            window.addstr(y+2, x, s2)
            window.addstr(y+4, x, 'Exit(home/del) | New(enter)', color.session)
            window.move(y, x)
            curses.noecho()
            curses.curs_set(0)
            self.end_sentence = False
            window.refresh()
            while True:
                try:
                    letter = window.getkey()
                except:
                    letter = None
                if letter == 'KEY_HOME' or letter == 'KEY_DC':
                    self.menu()
                if self.posx == len(sentence) and self.posy == len(sentences)-1 and letter != None:
                    break
                # CHECK LETTER (CASE 1: correct letter, incorrect letter)
                if letter in self.letters or letter == chr(32) or letter == chr(39) or letter == chr(45):
                    #START AT FIRST LETTER
                    if self.posx == 0 and self.posy == 0:
                        start = time.time()
                        self.cch = 0
                        self.ich = 0
                    # CASE 2: END OF SENTENCE
                    if self.posx == len(sentence):
                        y += 1
                        x -= self.posx
                        self.posx = 0
                        self.end_sentence = True
                        if self.posy == 2:
                            break
                        elif self.posy == 1:
                            sentence = s2
                            self.posy = 2
                        elif self.posy == 0:
                            sentence = s1
                            self.posy = 1
                    # CORRECT
                    if letter == sentence[self.posx] and self.end_sentence == False:
                        stops[self.posy][self.posx] = 1
                        window.addch(y, x, sentence[self.posx], color.correct)
                        x += 1
                        self.posx += 1
                        self.cch += 1
                        self.realcch += 1
                    # INCORRECT
                    elif letter != sentence[self.posx] and self.end_sentence == False:
                        if sentence[self.posx] == ' ':
                            window.addch(y, x, letter, color.incorrect)
                            x += 1
                            self.posx += 1
                            self.ich += 1
                            self.realich += 1
                        else:
                            window.addch(y, x, sentence[self.posx], color.incorrect)
                            x += 1
                            self.posx += 1
                            self.ich += 1
                            self.realich += 1
                # CASE 3: BACKSPACE
                elif letter == 'KEY_BACKSPACE' and self.posx > 0:
                    if self.posx == len(sentence):
                        window.addch(y, x-1, sentence[self.posx-1])
                        x -= 1
                        self.posx -= 1
                    else:
                        if stops[self.posy][self.posx-1] == 0:
                            window.addch(y, x-1, sentence[self.posx-1])
                            x -= 1
                            self.posx -= 1
                            self.realich -= 1
                        elif stops[self.posy][self.posx-1] == 1:
                            stops[self.posy][self.posx-1] = 0
                            window.addch(y, x-1, sentence[self.posx-1])
                            x -= 1
                            self.posx -= 1
                            self.realcch -= 1
                elif letter == 'KEY_BACKSPACE' and self.posx == 0 and self.posy > 0:
                    self.end_sentence = True
                    window.addch(y, x, sentence[self.posx])
                    y -= 1
                    self.posy -= 1
                    sentence = sentences[self.posy]
                    self.posx = len(sentence)
                    x += len(sentence)
                
                elif letter == '\n':
                    self.paragraph_mode()
                
                # UPDATE
                if self.posx > 1 and self.posx != len(sentence) and self.end_sentence == False and (letter in self.letters or letter in self.specialchars):
                    self.seconds = (time.time()-start)
                    cchpersecond = self.cch/self.seconds
                    self.wpm = (cchpersecond/min(max(1, self.cch), self.wordlen))*60
                    self.acc = (self.cch/(self.cch+self.ich))*100
                    self.updatewpm(wpmcounter)
                if self.posx < len(sentence):
                    window.addch(y, x, sentence[self.posx], curses.A_UNDERLINE)
                    if self.posx < len(sentence)-1:
                        window.addch(y, x+1, sentence[self.posx+1], curses.A_BOLD)
                #INIT NEXT 
                self.end_sentence = False
                window.move(y, x)


            #DISPLAY INFO
            window.nodelay(0)
            self.displayinfo()

        def sentence_mode(self):
            window.nodelay(1)
            window.timeout(100)
            self.mode = 1
            self.resetyx()
            self.resetstats()
            self.resetpos()
            y, x = self.y//2, self.x//2
            sentence = self.generate_sentence(self.length)
            self.wordlen = self.avgwordlength(sentence.split())
            stops = [0 for i in sentence]
            wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
            window.clear()
            x -= len(sentence)//2
            window.addstr(y, x, sentence)
            window.addstr(y, x, sentence[self.posx], curses.A_UNDERLINE)
            window.addstr(y, x+1, sentence[self.posx+1], curses.A_BOLD)
            window.addstr(y+2, x, 'Exit(home/del) | New(enter)', color.session)
            window.move(y, x)
            curses.noecho()
            curses.curs_set(0)
            while True:
                try:
                    letter = window.getkey()
                except:
                    letter = None
                # CHECK LETTER (CASE 1: correct letter, incorrect letter)
                if letter in self.letters or letter == chr(32) or letter == chr(39) or letter == chr(45):
                    #START AT FIRST LETTER
                    if self.posx == 0:
                        self.cch = 0
                        self.ich = 0
                        start = time.time()
                    # CASE 3: END OF SENTENCE
                    if self.posx > len(sentence)-1:
                        break
                    # CORRECT
                    if letter == sentence[self.posx]:
                        stops[self.posx] = 1
                        window.addch(y, x, sentence[self.posx], color.correct)
                        x += 1
                        self.posx += 1
                        self.cch += 1
                        self.realcch += 1
                    # INCORRECT
                    elif letter != sentence[self.posx]:
                        if sentence[self.posx] == ' ':
                            window.addch(y, x, letter, color.incorrect)
                            x += 1
                            self.posx += 1
                            self.ich += 1
                            self.realich += 1
                        else:
                            window.addch(y, x, sentence[self.posx], color.incorrect)
                            x += 1
                            self.posx += 1
                            self.ich += 1
                            self.realich += 1
                # CASE 2: BACKSPACE
                elif letter == 'KEY_BACKSPACE' and self.posx > 0:
                    if self.posx > len(sentence)-1:
                        break
                    else:
                        if stops[self.posx-1] == 0:
                            window.addch(y, x-1, sentence[self.posx-1])
                            x -= 1
                            self.posx -= 1
                            self.realich -= 1
                        elif stops[self.posx-1] == 1:
                            stops[self.posx-1] = 0
                            window.addch(y, x-1, sentence[self.posx-1])
                            x -= 1
                            self.posx -= 1
                            self.realcch -= 1
                
                elif letter == 'KEY_HOME' or letter == 'KEY_DC':
                    self.menu()
                # CASE 3: END OF SENTENCE
                elif self.posx > len(sentence)-1 and letter != None:
                    break
                elif letter == '\n':
                    self.sentence_mode()
                # UPDATE
                if self.posx > 1 and self.posx != len(sentence) and (letter in self.letters or letter in self.specialchars):
                    self.seconds = (time.time()-start)
                    cchpersecond = self.cch/self.seconds
                    wps = cchpersecond/min(max(1, self.cch), self.wordlen)
                    self.wpm = wps*60
                    self.acc = (self.cch/(self.cch+self.ich))*100
                    self.updatewpm(wpmcounter)
                if self.posx < len(sentence):
                    window.addch(y, x, sentence[self.posx], curses.A_UNDERLINE)
                if self.posx < len(sentence)-1:
                    window.addch(y, x, sentence[self.posx], curses.A_UNDERLINE)
                    window.addch(y, x+1, sentence[self.posx+1], curses.A_BOLD)
                #INIT NEXT
                window.move(y, x)
            #DISPLAY INFO
            window.nodelay(0)
            self.displayinfo()

        def guide(self):
            #INIT GUIDE
            curses.curs_set(0)
            self.resetyx()
            self.resetpos()
            window.clear()
            y, x = 1, game.x//2-len(self.ency[1])//2
            for i in range(len(self.ency)):
                window.addstr(y+i, x, str(self.ency[i]), color.session)
            y -= len(self.ency)
            window.nodelay(1)
            window.timeout(100)
            window.refresh()
            page = 0
            #LOOP GUIDE
            while True:
                try:
                    key = window.getkey()
                except:
                    key = None
                #CASES GUIDE
                if key == 'KEY_HOME' or key == 'KEY_DC':
                    self.menu()

        def menu(self):
            curses.curs_set(1)
            self.resetyx()
            self.resetpos()
            window.clear()
            y, x = self.y//2, self.x//2-len(self.consolebanner)//2
            window.addstr(y-1, x, self.consolebanner, color.session)
            window.move(y, x)
            window.addstr(y, x, '$', color.session)
            x+=1
            start = x
            displayline = curses.newwin(self.y//2-1, curses.COLS, y+1, 0)
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
                    if userinput in self.commands:
                        if userinput == self.commands[0]:
                            exit()
                        elif userinput == self.commands[1]:
                            exit()
                        elif userinput == self.commands[2]:
                            self.sentence_mode()
                        elif userinput == self.commands[3]:
                            self.sentence_mode()
                        elif userinput == self.commands[4]:
                            self.paragraph_mode()
                        elif userinput == self.commands[5]:
                            self.paragraph_mode()
                        #help
                        elif userinput == self.commands[6]:
                            displayline.clear()
                            self.guide()
                        elif userinput == self.commands[7]:
                            self.settingsmainmenu()
                        elif userinput == self.commands[8]:
                            self.settingsmainmenu()
                    else:
                        for i in range(len(userinput)+1):
                            window.delch(y, x)
                            x -= 1
                        displayline.clear()
                        self.consolemessage(displayline, self.errormessage, 0, self.x//2-len(self.errormessage)//2)
                        errortick = tick
                        window.move(y, max(start, x))

                elif key == 'KEY_BACKSPACE':
                    if start < x:
                        window.delch(y, x-1)
                        x -= 1
                        window.move(y, max(start, x))
                elif key == 'KEY_HOME' or key == 'KEY_DC':
                    displayline.clear()
                    displayline.refresh()
                    window.move(y, max(start, x))
                elif key in self.letters or key == chr(32):
                    window.addstr(y, x, key, color.session)
                    x += 1
                    window.move(y, max(start, x))

                #OUTPUT
                if tick < errortick+32 and tick > errortick+30:
                    displayline.clear()
                    displayline.refresh()
                    window.move(y, max(start, x))
                if start >= x:
                    x = start

    class Color:
        def __init__(self):
            self.seed = random.randint(0, 232)
            self.correct = curses.color_pair(11)
            self.incorrect = curses.color_pair(10)
            self.session = curses.color_pair(self.seed)
            #self.indicators = [x for x in range(160, 154, -1)]+[x for x in range(227, 202, -6)]+[x for x in range(197, 202)]+[166, 130, 136, 142, 58]
            self.indicators = [10, 10, 197, 203, 215, 227, 191, 155, 119, 122, 124, 82, 76, 70, 64, 100, 142, 184, 226, 254]
        
                                    
    #-------------------------------------------------------------------------------------
    #  INIT COLORS
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    # INIT OBJECTS
    color = Color()  
    game = Game()
    # REJECT SCREEN SIZE < 65x15
    if game.x < 65 or game.y < 15:
        window.addstr(0, 0, f'Error: Terminal Size({game.x}x{game.y}) too small.')
        window.addstr(2, 0, f'Press any key to quit')
        window.getch()
        exit()
    #START GAME
    game.guide()
    


curses.wrapper(main)