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
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
Words = open('1-1000.txt', 'r').read().splitlines()
def main(window):

    def setgamedifficulty(difficulty):
        global Words
        if difficulty == 0:
            with open('1-1000.txt', 'r') as f1:
                Words = f1.read().splitlines()
        elif difficulty == 1:
            with open('1-1000.txt', 'r') as f1, open('o3000.txt', 'r') as f2:
                Words = f1.read().splitlines()
                Words += f2.read().splitlines()
        elif difficulty == 2:
            with open('o5000.txt', 'r') as f1, open('1-1000.txt', 'r') as f2, open('o3000.txt', 'r') as f3:
                Words = f1.read().splitlines()
                Words += f2.read().splitlines()
                Words += f3.read().splitlines()

    def settingsdifficultymenu():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//2, x//2
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(0)
        option = 0
        #init screen content
        y -= len(settingsdifficulty)//2
        textstart = y
        def sdminit(y, x, o):
            window.addstr(y+len(settingsdifficulty)+1, x, 'Back(home/del) | Select(enter)', curses.color_pair(int(config['default']['colorsession'])))
            for i in range(len(settingsdifficulty)):
                if i == option:
                    window.addstr(y, x, settingsdifficulty[i], curses.A_REVERSE)
                else:
                    window.addstr(y, x, settingsdifficulty[i], curses.color_pair(int(config['default']['colorsession'])))
                y += 1
        sdminit(y, x, option)
        y -= len(settingsdifficulty)
        starty = y
        maxy = y+len(settingsdifficulty)-1
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
                    setgamedifficulty(0)
                    config['default']['difficulty'] = '0'
                    window.addstr(textstart-3, x, f'Set to {settingsdifficulty[0]}')
                    
                elif option == 1:
                    #correct
                    setgamedifficulty(1)
                    config['default']['difficulty'] = '1'
                    window.addstr(textstart-3, x, f'Set to {settingsdifficulty[1]}')
                elif option == 2:
                    #incorrect
                    setgamedifficulty(2)
                    config['default']['difficulty'] = '2'
                    window.addstr(textstart-3, x, f'Set to {settingsdifficulty[2]}')
            
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                settingsmainmenu()
                #init next screen
            #init next
            window.move(y, x)
        #end

    def setincorrectcolor():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//3, x//5
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(1)
        starty = y
        startx = x
        maxx = int(window.getmaxyx()[1]-(1/5*window.getmaxyx()[1]))
        screenrange = maxx-startx
        #init screen content
        for i in range(0, curses.COLORS):
            if x < maxx:
                window.addstr(y, x, '0', curses.color_pair(i+1))
                x += 1
            else:
                x = window.getmaxyx()[1]//5
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
                config['default']['colorincorrect'] = str(option)
                settingscolormenu()
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                settingscolormenu()

            #init next
            window.move(y, x)
        #end

    def setcorrectcolor():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//3, x//5
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(1)
        starty = y
        startx = x
        maxx = int(window.getmaxyx()[1]-(1/5*window.getmaxyx()[1]))
        screenrange = maxx-startx
        #init screen content
        for i in range(0, curses.COLORS):
            if x < maxx:
                window.addstr(y, x, '0', curses.color_pair(i+1))
                x += 1
            else:
                x = window.getmaxyx()[1]//5
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
                config['default']['colorcorrect'] = str(option)
                settingscolormenu()
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                settingscolormenu()

            #init next
            window.move(y, x)
        #end

    def setmenucolor():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//3, x//5
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(1)
        starty = y
        startx = x
        maxx = int(window.getmaxyx()[1]-(1/5*window.getmaxyx()[1]))
        screenrange = maxx-startx
        #init screen content
        for i in range(0, curses.COLORS):
            if x < maxx:
                window.addstr(y, x, '0', curses.color_pair(i+1))
                x += 1
            else:
                x = window.getmaxyx()[1]//5
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
                config['default']['colorsession'] = str(option)
                settingscolormenu()
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                settingscolormenu()

            #init next
            window.move(y, x)
        #end

    def settingscolormenu():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//2, x//2
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(0)
        option = 0
        #init screen content
        y -= len(settingscolor)//2
        textstart = y
        def scminit(y, x, o):
            window.addstr(y+len(settingscolor)+1, x, 'Back(home/del) | Select(enter)', curses.color_pair(int(config['default']['colorsession'])))
            for i in range(len(settingscolor)):
                if i == option:
                    window.addstr(y, x, settingscolor[i], curses.A_REVERSE)
                else:
                    window.addstr(y, x, settingscolor[i], curses.color_pair(int(config['default']['colorsession'])))
                y += 1
        scminit(y, x, option)
        y -= len(settingscolor)
        starty = y
        maxy = y+len(settingscolor)-1
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
                    setcorrectcolor()
                elif option == 1:
                    #correct
                    setincorrectcolor()
                elif option == 2:
                    #incorrect
                    setmenucolor()
            
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                settingsmainmenu()
                #init next screen
            #init next
            window.move(y, x)
        #end

    def settingsmainmenu():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.clear()
        y, x = y//2, x//2
        window.nodelay(1)
        window.timeout(100)
        curses.curs_set(0)
        #init screen content
        y -= len(settings)//2
        option = 0
        textstart = y
        def smminit(y, x, o):
            window.addstr(y+len(settings)+1, x, 'Back(home/del) | Select(enter)', curses.color_pair(int(config['default']['colorsession'])))
            for i in range(len(settings)):
                if i == option:
                    window.addstr(y, x, settings[i], curses.A_REVERSE)
                else:
                    window.addstr(y, x, settings[i], curses.color_pair(int(config['default']['colorsession'])))
                y += 1
        smminit(y, x, option)
        y -= len(settings)
        starty = y
        maxy = y+len(settings)-1
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
                    settingscolormenu()
                elif option == 1:
                    settingsdifficultymenu()
            
            elif key == 'KEY_HOME' or key == 'KEY_BACKSPACE' or key == 'KEY_DC':
                menu()
            #init next
            window.move(y, x)
        #end

    def displayinfo(wpm, acc, seconds, realcch, realich, cch, ich, mode):
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        x, y = x//2, y//2
        x -= 10
        window.clear()
        window.move(y, x) 
        window.addstr(y+1, x, 'Menu(home/del) New(enter)', curses.color_pair(int(config['default']['colorsession'])))
        window.addstr(y-3, x, f'{wpm:.2f} wpm', curses.color_pair(colorindicators[int(wpm)//10-1]))
        window.addstr(y-2, x, f'{acc:.2f} % ', curses.color_pair(colorindicators[int(acc)//10-1]))
        window.addstr(y-1, x, f'{seconds:.2f} (s) ')
        window.addstr(y, x, f'C: {realcch} I: {realich} M: {ich} F: {ich-realich}')
        y -= 3
        while True:
            key = window.getkey()
            if key == 'KEY_HOME' or key == 'KEY_DC':
                menu()
            elif key == '\n':
                if mode == 1:
                    sentence_mode()
                elif mode == 2:
                    paragraph_mode()
            
    def generate_sentence(l):
        sentence = []
        slen = 0
        while True:
            word = random.choice(Words)
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
            
    def avgwordlength(sentencelist):
        l = 0
        n = 0
        for w in sentencelist:
            l += len(w)
            n += 1
        return l/n
            
    def updatewpm(counter, wpm, acc):
        counter.clear()
        if wpm < 200:
            counter.addstr(0, 0, f'{wpm:.2f} wpm ', curses.color_pair(colorindicators[max((int(wpm)//10-1), 0)]))
            counter.addstr(0, 11, f'| {acc:.2f} %', curses.color_pair(colorindicators[max(int((acc//10)-1), 0)]))
        else:
            counter.addstr(0, 0, f'{wpm:.2f} wpm ')
            counter.addstr(0, 11, f'| {acc:.2f} %', curses.color_pair(colorindicators[int(acc*2)//10-1]))
        counter.refresh()
    
    def paragraph_mode():
        #INIT
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        window.nodelay(1)
        window.timeout(100)
        posx = 0
        posy = 0
        y, x = y//2-2, x//2
        wpm = 0; acc =  0; seconds = 0; cch = 0; ich = 0; realcch = 0; realich = 0
        end_sentence = False
        s0 = generate_sentence(x//2)
        s1 = generate_sentence(x//2)
        s2 = generate_sentence(x//2)
        sentence = s0
        sentences = [s0, s1, s2]
        wordlen = avgwordlength((s0+s1+s2).split())
        stops = [[0 for i in s0], [0 for i in s1], [0 for i in s2]]
        window.clear()
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)  
        x -= len(sentence)//2
        window.addstr(y, x, sentence) 
        window.addstr(y, x, sentence[posx], curses.A_UNDERLINE) #POS MARKER
        window.addstr(y, x+1, sentence[posx+1], curses.A_BOLD)
        window.addstr(y+1, x, s1) 
        window.addstr(y+2, x, s2)
        window.addstr(y+4, x, 'Exit(home/del) | New(enter)', curses.color_pair(int(config['default']['colorsession'])))
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        end_sentence = False
        window.refresh()
        while True:
            try:
                letter = window.getkey()
            except:
                letter = None
            if letter == 'KEY_HOME' or letter == 'KEY_DC':
                menu()
            if posx == len(sentence) and posy == len(sentences)-1 and letter != None:
                break
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in letters or letter == chr(32) or letter == chr(39) or letter == chr(45):
                #START AT FIRST LETTER
                if posx == 0 and posy == 0:
                    start = time.time()
                    cch = 0
                    ich = 0
                # CASE 2: END OF SENTENCE
                if posx == len(sentence):
                    y += 1
                    x -= posx
                    posx = 0
                    end_sentence = True
                    if posy == 2:
                        break
                    elif posy == 1:
                        sentence = s2
                        posy = 2
                    elif posy == 0:
                        sentence = s1
                        posy = 1
                # CORRECT
                if letter == sentence[posx] and end_sentence == False:
                    stops[posy][posx] = 1
                    window.addch(y, x, sentence[posx], curses.color_pair(int(config['default']['colorcorrect'])))
                    x += 1
                    posx += 1
                    cch += 1
                    realcch += 1
                # INCORRECT
                elif letter != sentence[posx] and end_sentence == False:
                    if sentence[posx] == ' ':
                        window.addch(y, x, letter, curses.color_pair(int(config['default']['colorincorrect'])))
                        x += 1
                        posx += 1
                        ich += 1
                        realich += 1
                    else:
                        window.addch(y, x, sentence[posx], curses.color_pair(int(config['default']['colorincorrect'])))
                        x += 1
                        posx += 1
                        ich += 1
                        realich += 1
            # CASE 3: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and posx > 0:
                if posx == len(sentence):
                    window.addch(y, x-1, sentence[posx-1])
                    x -= 1
                    posx -= 1
                else:
                    if stops[posy][posx-1] == 0:
                        window.addch(y, x-1, sentence[posx-1])
                        x -= 1
                        posx -= 1
                        realich -= 1
                    elif stops[posy][posx-1] == 1:
                        stops[posy][posx-1] = 0
                        window.addch(y, x-1, sentence[posx-1])
                        x -= 1
                        posx -= 1
                        realcch -= 1
            elif letter == 'KEY_BACKSPACE' and posx == 0 and posy > 0:
                end_sentence = True
                window.addch(y, x, sentence[posx])
                y -= 1
                posy -= 1
                sentence = sentences[posy]
                posx = len(sentence)
                x += len(sentence)
            
            elif letter == '\n':
                paragraph_mode()
            
            # UPDATE
            if posx > 1 and posx != len(sentence) and end_sentence == False and (letter in letters or letter in specialchars):
                seconds = (time.time()-start)
                cchpersecond = cch/seconds
                wpm = (cchpersecond/min(max(1, cch), wordlen))*60
                acc = (cch/(cch+ich))*100
                updatewpm(wpmcounter, wpm, acc)
            if posx < len(sentence):
                window.addch(y, x, sentence[posx], curses.A_UNDERLINE)
                if posx < len(sentence)-1:
                    window.addch(y, x+1, sentence[posx+1], curses.A_BOLD)
            #INIT NEXT 
            end_sentence = False
            window.move(y, x)


        #DISPLAY INFO
        window.nodelay(0)
        displayinfo(wpm, acc, seconds, realcch, realich, cch, ich, 2)

    def sentence_mode():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        posx = 0
        posy = 0
        wpm = 0; acc =  0; seconds = 0; cch = 0; ich = 0; realcch = 0; realich = 0
        window.nodelay(1)
        window.timeout(100)
        y, x = y//2, x//2
        sentence = generate_sentence(x//2)
        wordlen = avgwordlength(sentence.split())
        stops = [0 for i in sentence]
        wpmcounter = curses.newwin(1, curses.COLS, y-2, x-len(sentence)//2)        
        window.clear()
        x -= len(sentence)//2
        window.addstr(y, x, sentence)
        window.addstr(y, x, sentence[posx], curses.A_UNDERLINE)
        window.addstr(y, x+1, sentence[posx+1], curses.A_BOLD)
        window.addstr(y+2, x, 'Exit(home/del) | New(enter)', curses.color_pair(int(config['default']['colorsession'])))
        window.move(y, x)
        curses.noecho()
        curses.curs_set(0)
        while True:
            try:
                letter = window.getkey()
            except:
                letter = None
            # CHECK LETTER (CASE 1: correct letter, incorrect letter)
            if letter in letters or letter == chr(32) or letter == chr(39) or letter == chr(45):
                #START AT FIRST LETTER
                if posx == 0:
                    cch = 0
                    ich = 0
                    start = time.time()
                # CASE 3: END OF SENTENCE
                if posx > len(sentence)-1:
                    break
                # CORRECT
                if letter == sentence[posx]:
                    stops[posx] = 1
                    window.addch(y, x, sentence[posx], curses.color_pair(int(config['default']['colorcorrect'])))
                    x += 1
                    posx += 1
                    cch += 1
                    realcch += 1
                # INCORRECT
                elif letter != sentence[posx]:
                    if sentence[posx] == ' ':
                        window.addch(y, x, letter, curses.color_pair(int(config['default']['colorincorrect'])))
                        x += 1
                        posx += 1
                        ich += 1
                        realich += 1
                    else:
                        window.addch(y, x, sentence[posx], curses.color_pair(int(config['default']['colorincorrect'])))
                        x += 1
                        posx += 1
                        ich += 1
                        realich += 1
            # CASE 2: BACKSPACE
            elif letter == 'KEY_BACKSPACE' and posx > 0:
                if posx > len(sentence)-1:
                    break
                else:
                    if stops[posx-1] == 0:
                        window.addch(y, x-1, sentence[posx-1])
                        x -= 1
                        posx -= 1
                        realich -= 1
                    elif stops[posx-1] == 1:
                        stops[posx-1] = 0
                        window.addch(y, x-1, sentence[posx-1])
                        x -= 1
                        posx -= 1
                        realcch -= 1
            
            elif letter == 'KEY_HOME' or letter == 'KEY_DC':
                menu()
            # CASE 3: END OF SENTENCE
            elif posx > len(sentence)-1 and letter != None:
                break
            elif letter == '\n':
                sentence_mode()
            # UPDATE
            if posx > 1 and posx != len(sentence) and (letter in letters or letter in specialchars):
                seconds = (time.time()-start)
                cchpersecond = cch/seconds
                wps = cchpersecond/min(max(1, cch), wordlen)
                wpm = wps*60
                acc = (cch/(cch+ich))*100
                updatewpm(wpmcounter, wpm, acc)
            if posx < len(sentence):
                window.addch(y, x, sentence[posx], curses.A_UNDERLINE)
            if posx < len(sentence)-1:
                window.addch(y, x, sentence[posx], curses.A_UNDERLINE)
                window.addch(y, x+1, sentence[posx+1], curses.A_BOLD)
            #INIT NEXT
            window.move(y, x)
        #DISPLAY INFO
        window.nodelay(0)
        displayinfo(wpm, acc, seconds, realcch, realich, cch, ich, 1)

    def guide():
        #INIT GUIDE
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        curses.curs_set(0)
        window.clear()
        y, x = 1, x//2-len(ency[1])//2
        for i in range(len(ency)):
            window.addstr(y+i, x, str(ency[i]), curses.color_pair(int(config['default']['colorsession'])))
        y -= len(ency)
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
                menu()

    def menu():
        y = window.getmaxyx()[0]
        x = window.getmaxyx()[1]
        curses.curs_set(1)
        window.clear()
        y, x = y//2, x//2-len(consolebanner)//2
        window.addstr(y-1, x, consolebanner, curses.color_pair(int(config['default']['colorsession'])))
        window.move(y, x)
        window.addstr(y, x, '$', curses.color_pair(int(config['default']['colorsession'])))
        x+=1
        start = x
        displayline = curses.newwin(y//2-1, curses.COLS, y+1, 0)
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
                        with open('settings.ini', 'w') as configfile:    # save
                            config.write(configfile)
                        exit()
                    elif userinput == commands[1]:
                        with open('settings.ini', 'w') as configfile:    # save
                            config.write(configfile)
                        exit()
                    elif userinput == commands[2]:
                        sentence_mode()
                    elif userinput == commands[3]:
                        sentence_mode()
                    elif userinput == commands[4]:
                        paragraph_mode()
                    elif userinput == commands[5]:
                        paragraph_mode()
                    #help
                    elif userinput == commands[6]:
                        displayline.clear()
                        guide()
                    elif userinput == commands[7]:
                        settingsmainmenu()
                    elif userinput == commands[8]:
                        settingsmainmenu()
                else:
                    for i in range(len(userinput)+1):
                        window.delch(y, x)
                        x -= 1
                    displayline.clear()
                    displayline.addstr(0, window.getmaxyx()[1]//2-len(errormessage)//2, errormessage, curses.color_pair(int(config['default']['colorsession'])))
                    displayline.refresh()
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
            elif key in letters or key == chr(32):
                window.addstr(y, x, key, curses.color_pair(int(config['default']['colorsession'])))
                x += 1
                window.move(y, max(start, x))

            #OUTPUT
            if tick < errortick+32 and tick > errortick+30:
                displayline.clear()
                displayline.refresh()
                window.move(y, max(start, x))
            if start >= x:
                x = start
                                
    #-------------------------------------------------------------------------------------
    # INIT GAME
    letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]  
    commands = ['quit', 'q', 'sentence', 's', 'paragraph', 'p', 'help', 'settings', 'c']
    openingmessage = 'Welcome to CurseType! Type "sentence" or "help" and press enter.'
    consolebanner = f'CurseType Console'
    errormessage = 'Not understood. Type "help" for a list of commands.'
    ency = open('guide.txt', 'r').read().splitlines()
    specialchars = [chr(39), chr(32), chr(45), 'KEY_BACKSPACE']
    settings = ['color', 'vocabulary']
    settingscolor = ['correct letter', 'incorrect letter', 'menu color']
    settingsdifficulty = ['common words', 'oxford 3000', 'oxford 5000']
    setgamedifficulty(int(config['default']['difficulty']))
    #  INIT COLORS
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    if int(config['default']['colorsession']) < 0:
        config['default']['colorsession'] = str(random.randint(0, 232))
    #indicators = [x for x in range(160, 154, -1)]+[x for x in range(227, 202, -6)]+[x for x in range(197, 202)]+[166, 130, 136, 142, 58]
    colorindicators = [10, 10, 197, 203, 215, 227, 191, 155, 119, 122, 124, 82, 76, 70, 64, 100, 142, 184, 226, 254]
    # REJECT SCREEN SIZE < 65x15
    y = window.getmaxyx()[0]
    x = window.getmaxyx()[1]
    if x < 65 or y < 15:
        window.addstr(0, 0, f'Error: Terminal Size({x}x{y}) too small.')
        window.addstr(2, 0, f'Press any key to quit')
        window.getch()
        exit()
    #START GAME
    guide()
    

curses.wrapper(main)

with open('settings.ini', 'w') as configfile:    # save
    config.write(configfile)