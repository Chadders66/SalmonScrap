from tkinter import *
from PIL import ImageTk,Image
import json
import os

startingMoney = 4000
playerList = []
forSaleBoats = []
forSaleNames = ['Fishing Boat', 'Longliner', 'Small Yacht', 'Yacht', 'Small Trawler', 'Trawler', 'Small Seine', 'Seine Boat']
imageList = []

help1 = [0, 0, 2, 2]
help2 = [0, 2, 0, 2]

help3 = [0, 0, 1, 1]
help4 = [0, 1, 0, 1]

with open('SalmonScrap/GUI/SalmonScrap/boats.json') as json_file:
    boats = json.load(json_file)

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1000x600")

def initBoats():
    for x in range(len(forSaleNames)):
        forSaleBoats.append(Boat(forSaleNames[x]))

def resizeImages():
    for x in range(len(forSaleNames)):
        imageList.append(Image.open("SalmonScrap/v0.2/assets/" + forSaleBoats[x].image)) #resize image
        imageList[x] = imageList[x].resize((165, 130), Image.ANTIALIAS)
    imageList.append(Image.open("SalmonScrap/v0.2/assets/blank.png"))
    imageList[8] = imageList[8].resize((165, 130), Image.ANTIALIAS)

def populateFrames():
    img_blank = ImageTk.PhotoImage(imageList[8])
    m1 = 0
    m2 = 0
    if len(playerList) == 2:
        m2 += 2
    elif len(playerList) == 3:
        m1 += 2
    elif len(playerList) == 4:
        m1 += 2
        m2 += 2
    elif len(playerList) > 4:
        print('Too many players!')
        exit()
    for x in range(len(playerList)):
        for y in range(4):
            playerList[x].labels.append(Label(playerList[x].frame, image=img_blank))
            playerList[x].labels[y].image = img_blank
            playerList[x].labels[y].grid(row=(help3[y]+m1), column=(help4[y]+m2), padx=10, pady=5)

class Player:
    def __init__(self, name):
        self.pnum = len(playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = 0
        self.frame = []
        self.labels = []
        currentPlayers = len(playerList)
        playerList.append(self)
        self.frame = LabelFrame(root, text=name, padx=20, pady=20)
        self.frame.grid(row=help1[currentPlayers], column=help2[currentPlayers], rowspan=2, columnspan=2, padx=10, pady=5)

    def printStats(self):
        print("Player %d (%s):  Money: %s" %(self.pnum,self.name,self.money))


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
        
    def hire(self, player, rank, hirereq):
        for x in range(hirereq):
            self.crew.append(rank)
            if rank == 'V':
                player.money = player.money - 200
            elif rank == 'E': 
                player.money = player.money - 100
            elif rank == 'N':
                player.money = player.money - 50

initBoats()

resizeImages()

player1 = Player("Andrew")
player2 = Player("Chadders")

populateFrames()

# forSaleBoats[0].buyBoat(player1, 'Fishing Boat', 'H.M.S. Riven')

# player1.printStats()

root.mainloop()