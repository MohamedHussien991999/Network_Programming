import random 
from tkinter import *
from tkinter import messagebox

from socket import * 

# global variables
player = 0 # indicate which player has to play (1 me , 0 other )
meScore = 100 # indicate which turn used to show if we finish game or not 
oppositeScore = 100

# check
def check():
	if meScore <= 0 :
            win("Client")
	elif oppositeScore <= 0 :
            win("Server")

	
def win(player):
	messagebox.showinfo("win", player +" is win")
	wind.destroy()


def clicked1():
	global player
	global meScore
	if(player==1):
		player=0 # make turn to other player
		# claculate rand value
		p = random.randint(0,20)
		meScore -= p
		sendPlay(p)	
		check()


def sendPlay(p):
    showStatus("Me played -{}\n Opposite Turn".format(p))
    # display
    lbMe["text"] = "Me:{}".format(meScore)
    n = str(meScore)
    n = n.encode()
    soc.send(n)

def handlePlay(n):
    global player
    global oppositeScore
    oppositeScore = n 
    lbOpposite["text"] = "Opposite:{}".format(oppositeScore)
    player = 1
    check()


def applayPlay(p):
    showStatus("opposite played \n Your Turn")
    p = p.decode()
    p = int(p)
    handlePlay(p)


def showStatus(msg):
    lbStatus["text"] = msg
    

#window
wind = Tk()
wind.title("Mo3TrAND") # title
#wind.geometry("400x400")  # size

# labels one and two players
lbMe = Label(wind,text="Me:100" ,font=('Helvetiica',35))
lbMe.grid(row = 0,column=0)

lbOpposite = Label(wind,text="Opposite:100" ,font=('Helvetiica',35))
lbOpposite.grid(row = 0,column=2)


lbStatus = Label(wind,text="Waiting" ,font=('Helvetiica',35))
lbStatus.grid(row = 2,column=1)

btn1=Button(wind,text="Roll",fg="black",width=10,height=5,font='Helvetiica',command=clicked1)
btn1.grid(row=1,column=1)



# session with server
soc = socket(AF_INET , SOCK_STREAM)
showStatus("Waiting")

from threading import Thread


def connectServer():
    global soc
    soc.connect(("127.0.0.1" , 6002) )
    showStatus("Connected")
    t = Thread(target = rec )
    t.start()

    

def rec():
    while True:
      p = soc.recv(10)
      applayPlay(p)

tConnect  =Thread(target = connectServer)
tConnect.start()


#to run the window
wind.mainloop()
    