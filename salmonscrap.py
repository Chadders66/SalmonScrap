from tkinter import *
from PIL import ImageTk,Image
import json
import os
import time

path = ''

startingMoney = 4000
playerList = []
forSaleBoats = []
forSaleNames = ['Fishing Boat', 'Longliner', 'Small Yacht', 'Yacht', 'Small Trawler', 'Trawler', 'Small Seine', 'Seine Boat']
imageList = []

help1 = [0, 0, 1, 1]
help2 = [0, 1, 0, 1]

help3 = [0, 0, 3, 3]
help4 = [0, 4, 0, 4]

help5 = [1, 1, 1, 2, 2, 2]
help6 = [0, 1, 2, 0, 1, 2]

help7 = ['W', '', 'E', 'W', '', 'E']
help8 = []

with open(path + 'boats.json') as json_file:
    boats = json.load(json_file)

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1000x600")

def initBoats():
    for x in range(len(forSaleNames)):
        forSaleBoats.append(Boat(forSaleNames[x]))

def resizeImages():
    for x in range(len(forSaleNames)):
        imageList.append(Image.open(path + "assets/" + forSaleBoats[x].image)) #resize image
        imageList[x] = imageList[x].resize((165, 130), Image.ANTIALIAS)
    imageList.append(Image.open(path + "assets/blank.png"))
    imageList[8] = imageList[8].resize((165, 130), Image.ANTIALIAS)

def hirepop():
    print('Bloop')

def launchpop():
    print('Bloop')

def renamepop():
    print('Bloop')

def firepop():
    print('Bloop')

def sellpop():
    print('Bloop')

def repairpop():
    print('Bloop')

def populateFrames():
    img_blank = ImageTk.PhotoImage(imageList[8])
    if len(playerList) > 4:
        print('Too many players!')
        exit()
    for x in range(len(playerList)):
        for y in range(4):
            playerList[x].labels.append(Label(playerList[x].frame, image=img_blank))
            playerList[x].labels[y].image = img_blank
            playerList[x].labels[y].grid(row=(help3[y]), column=(help4[y]), columnspan=3)
            buttonList = []
            for z in range(6):
                shipButtons = ['Hire', 'Launch', 'Rename', 'Fire', 'Sell', 'Repair']
                shipCommands = [hirepop, launchpop, renamepop, firepop, sellpop, repairpop]
                buttonList.append(Button(playerList[x].frame, text=shipButtons[z], command=shipCommands[z], width=6))
                if y == 0:
                    n1 = 0
                    n2 = 0   
                elif y == 1:
                    n1 = 0
                    n2 = 4
                elif y == 2:
                    n1 = 3
                    n2 = 0
                elif y == 3:
                    n1 = 3
                    n2 = 4
                buttonList[z].grid(row=(help5[z]+n1), column=(help6[z]+n2), sticky=help7[z])
                playerList[x].buttons.append(buttonList)

class Player:
    def __init__(self, name):
        self.pnum = len(playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = []
        self.frame = []
        self.labels = []
        self.buttons = []
        currentPs = len(playerList)
        playerList.append(self)
        self.frame = LabelFrame(root, text=name)
        self.frame.grid(row=help1[currentPs], column=help2[currentPs], rowspan=1, columnspan=1)

    def printStats(self):
        print("Player %d (%s):  Money: %s" %(self.pnum,self.name,self.money))

    def update(self):
        for x in range (len(self.staff)):
            self.money = self.money - (self.staff[x].count('N') * 100)      #Novice weekly wages
            self.money = self.money - (self.staff[x].count('E') * 200)      #Expert weekly wages
            self.money = self.money - (self.staff[x].count('V') * 300)      #Veteran weekly wages

        for x in range (len(self.boats)):
            self.boats[x].relB = (self.boats[x].relB + 
            (self.staff[x].count('N') * 0.4 * self.boats[x].relI) +     #Novice reliability multiplier
            (self.staff[x].count('E') * 0.75 * self.boats[x].relI) +     #Expert reliability multiplier
            (self.staff[x].count('V') * 1 * self.boats[x].relI))        #Veteran reliability multiplier


class Boat:
    def __init__(self, name):
        self.name = 'For Sale'
        self.type = name
        self.desc = boats[name]['desc']
        self.cap = boats[name]['cap']
        self.size = boats[name]['size']
        self.cost = boats[name]['cost']
        self.hold = 0
        self.crew = []
        self.relB = 0
        self.relI = 0
        self.cspB = 0
        self.cspI = 0
        self.loc = ""
        self.player = ""
        self.image = boats[name]['image']

    def buyBoat(self, player, choice, newname):  
        currentboats = len(player.boats)
        player.boats.append(Boat(choice))
        player.money = player.money - boats[choice]['cost']
        player.boats[currentboats].name = newname
        player.boats[currentboats].type = choice
        player.boats[currentboats].hold = 0
        player.boats[currentboats].crew = []
        player.boats[currentboats].cost = (boats[choice]['cost'])*0.6
        player.boats[currentboats].relB = boats[choice]['relB']
        player.boats[currentboats].relI = boats[choice]['relI']
        player.boats[currentboats].cspB = boats[choice]['cspB']
        player.boats[currentboats].cspI = boats[choice]['cspI']
        player.boats[currentboats].loc = "In Harbour"
        player.boats[currentboats].player = player
        player.boats[currentboats].image = boats[choice]['image']
        imageIndex = forSaleNames.index(choice)
        boat_img = ImageTk.PhotoImage(imageList[imageIndex])
        player.labels[currentboats].configure(image=boat_img)
        player.labels[currentboats].image = boat_img
            
    def hire(self, player, boat, rank, hirereq):
        if len(self.crew) == 0:
            emptyList = []
            player.staff.append(emptyList)
        for x in range(hirereq):
            self.crew.append(rank)
            player.staff[boat].append(rank)
            if rank == 'V':
                player.money = player.money - 200       #Novice cost to hire
            elif rank == 'E':
                player.money = player.money - 100       #Expert cost to hire
            elif rank == 'N':
                player.money = player.money - 50        #Veteran cost to hire

initBoats()

resizeImages()

player1 = Player("Andrew")
player2 = Player("Chadders")

populateFrames()

selection = 0
forSaleBoats[selection].buyBoat(player1, forSaleNames[selection], 'H.M.S. Riven')
selection = 3
forSaleBoats[selection].buyBoat(player2, forSaleNames[selection], 'H.M.S. Sleepy')


root.mainloop()
