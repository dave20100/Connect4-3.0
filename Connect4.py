import socket
import _thread
from tkinter import *
import winsound
turn = 1
root = Tk()
root.title("Connect Four")
canv = []
canvas = []
buttons = []
RANGEX = 7
RANGEY = 6
OBJECTIVE = 4
ONLINE = 0
SOCK = 0
IDGRACZA = 0
def bonline():
    global ONLINE 
    global SOCK
    res()
    if ONLINE == 1:
        try:
            SOCK.close()
        except:
            pass
        ONLINE = 0
        reset["state"] = "normal"
        info["text"] = "Rozlaczono"
        Online["text"] = "Zagraj Online"
    else:
        SOCK = socket.socket()
        _thread.start_new_thread(online,())

def online():
    global ONLINE
    global turn
    global SOCK
    global IDGRACZA
    host = socket.gethostname()
    port = 12346
    try:
        SOCK.connect((host, port))
    except:
        raise ConnectionError
        return
    ONLINE = 1
    reset["state"]="disabled"
    Online["text"] = "Rozlacz"
    info["text"] = "Czekanie na przeciwnika"
    sygnal = SOCK.recv(1024)
    info["text"] = "Polaczono z innym graczem"
    sygnal = int.from_bytes(sygnal, byteorder='big')
    IDGRACZA = sygnal
    if IDGRACZA != turn:
        for b in buttons:
            b["state"]="disabled"
    else:
        for b in buttons:
            b["state"]="normal"
    while True:
        sygnal = SOCK.recv(1024)
        sygnal = int.from_bytes(sygnal, byteorder='big')
        change(sygnal)
    SOCK.close()

def check():
    countr = 0
    countb = 0
    t = []
    for x in canvas:
        for y in x:
            if (y["background"]=="white"):
                countr+=1
    if(countr==0):
        info["text"]="Remis"
        for b in buttons:
            b["state"]= "disabled"
        return
    countr=0
    for x in canvas:
        cont(x)
    for x in range(RANGEY):
        for y in range(RANGEX):
            t = [canvas[y][x] for y in range(RANGEX)]
        cont(t)
        t=[]
    for x in range(RANGEX-(OBJECTIVE-1)):
        for y in range(RANGEY-(OBJECTIVE-1)):
            t = [canvas[r+x][r+y] for r in range(OBJECTIVE)]
            cont(t)
            t=[]
    for x in range(RANGEX-(OBJECTIVE-1)):
        for y in range(RANGEY-1,RANGEY-OBJECTIVE,-1):
            t = [canvas[r+x][y-r] for r in range(OBJECTIVE)]
            cont(t)
            t=[]


def cont(eq):
    countr = 0
    countb = 0
    for x in eq:
        if(x["background"]=="red"):
            countr +=1
            countb=0
        if(x["background"]=="yellow"):
            countb +=1
            countr=0
        if(x["background"]=="white"):
            countr = 0
            countb = 0
        if(countr>OBJECTIVE-1 or countb>OBJECTIVE-1):
            if(countr>OBJECTIVE-1):
                info["text"]="gracz czerwony wygral"
                reset["text"] = "Nowa gra"
            if(countb>OBJECTIVE-1):
                info["text"]="gracz zolty wygral"
                reset["text"] = "Nowa gra"
            for b in buttons:
                b["state"] = "disabled"
            return
        

def change(idb):
    global IDGRACZA
    global ONLINE
    global turn
    global SOCK
    if ONLINE == 1:
        SOCK.send((idb).to_bytes(2, byteorder='big'))
        if idb == 404:
            res()
            return
        if IDGRACZA == turn:
            for b in buttons:
                b["state"]="disabled"
        else:
            for b in buttons:
                b["state"]="normal"
    info["text"] = "..."
    for y in range(RANGEY):
        if (canvas[idb][y]["background"] != "white" or y==RANGEY-1):
            if(y==0):
                info["text"] = "Bledny ruch"
                break
            if (y==RANGEY-1 and canvas[idb][y]["background"] == "white"):
                y=0
            if(turn==1):
                canvas[idb][y-1]["background"] = "red"
                turn=2
            else:
                canvas[idb][y-1]["background"] = "yellow"
                turn=1
            break
    label["text"] = "Tura gracza "+str(turn)
    check()


def res():
    global ONLINE
    global SOCK
    global turn
    if ONLINE == 1:
        SOCK.send((404).to_bytes(2, byteorder='big'))
    turn = 1
    for x in canvas:
        for y in x:
            y["background"] = "white"
    for b in buttons:
        b["state"] = "normal"
    label["text"] = "Tura gracza "+str(turn)
    info["text"] = "..."
    winsound.PlaySound(None, winsound.SND_ASYNC)



for x in range (RANGEX):
    for y in range(RANGEY):
        canv.append(Canvas(root, width=30, height=30, background="white"))
        canv[y].grid(column=x, row=y+2)
    canvas.append(canv)    
    canv = []

for i in range (RANGEX):
    buttons.append(Button(root,text="DROP",command=lambda x=i: change(x), height=2))
    buttons[i].grid(column=i, row=1)

def song(name):
    while True:
        winsound.PlaySound(name, winsound.SND_FILENAME)

songs=[]
for i in range(0,10):
    a='sound{}.wav'.format(i)
    songs.append(a)
def nastepna():
    _thread.start_new_thread(song,(songs[0],))

bnext=Button(root, text="Play song", command=nastepna)
bnext.grid(row=RANGEY+3, columnspan=RANGEX, sticky=E)

label= Label(root, text="Tura gracza "+str(turn))
label.grid(columnspan=RANGEX,row=0)

info = Label(root, text="...")
info.grid(row=RANGEY+2, columnspan = RANGEX)

reset = Button(root, text = "Nowa gra", command=res)
reset.grid(row = RANGEY+2, columnspan=RANGEX, sticky=W)

Quit=Button(root)
Quit["text"] = "Quit"
Quit["command"] = root.quit
Quit.grid(row=RANGEY+2, columnspan=RANGEX, sticky=E)

Online = Button(root)
Online["text"] = "Zagraj Online"
Online["command"] = bonline
Online.grid(row=RANGEY+3, columnspan=RANGEX)
app = Frame(root)

mainloop()
root.destroy()
