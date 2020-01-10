from tkinter import *
from PIL import ImageTk,Image
import json
import os
import time

path = ''

startingMoney = 6000
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

help7 = [7, 7, 7]
help8 = [2, 3, 4]

with open(path + 'boats.json') as json_file:
    boats = json.load(json_file)

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1100x600+300+100")

def initBoats():
    for x in range(len(forSaleNames)):
        forSaleBoats.append(Boat(forSaleNames[x]))

def resizeImages():
    for x in range(len(forSaleNames)):
        imageList.append(Image.open(path + "assets/" + forSaleBoats[x].image)) #resize image
        imageList[x] = imageList[x].resize((165, 130), Image.ANTIALIAS)
    imageList.append(Image.open(path + "assets/blank.png"))
    imageList[8] = imageList[8].resize((165, 130), Image.ANTIALIAS)

def sellFishpop():
    print('Bloop')

def endTurnpop():
    print('Bloop')

def buyBoatpop():
    print('Bloop')

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
        buttonList1 = []
        playerList[x].labels.append(Label(playerList[x].frame, text=playerList[x].stats))
        playerList[x].labels[0].grid(row=6, column=2, columnspan=3, padx=10, pady=10)
        for a in range(3):
            playerButtons = ['Sell Fish', 'End Turn', 'Buy Boat']
            playerCommands = [sellFishpop, endTurnpop, buyBoatpop]
            buttonList1.append(Button(playerList[x].frame, text=playerButtons[a], command=playerCommands[a]))
            buttonList1[a].grid(row=help7[a], column=help8[a])
        playerList[x].buttons.append(buttonList1)
        for y in range(4):
            noBoatStats = 'No boat to view \n Purchase a boat \n to view its stats'
            playerList[x].labels.append(Label(playerList[x].frame, image=img_blank, text=noBoatStats, justify=CENTER, compound=CENTER))
            playerList[x].labels[y+1].image = img_blank
            playerList[x].labels[y+1].grid(row=(help3[y]), column=(help4[y]), columnspan=3, padx=5, pady=10)
            buttonList2 = []
            for z in range(6):
                shipButtons = ['Hire', 'Launch', 'Rename', 'Fire', 'Sell', 'Repair']
                shipCommands = [hirepop, launchpop, renamepop, firepop, sellpop, repairpop]
                buttonList2.append(Button(playerList[x].frame, text=shipButtons[z], command=shipCommands[z], width=8))
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
                buttonList2[z].grid(row=(help5[z]+n1), column=(help6[z]+n2))
            playerList[x].buttons.append(buttonList2)

def getStats(player, boatindex):
    boatStatsView = []
    boatStatsView.append(player.boats[boatindex].name)
    boatStatsView.append(player.boats[boatindex].type)
    boatStatsView.append(player.boats[boatindex].hold)
    boatStatsView.append(player.boats[boatindex].cap)
    boatStatsView.append(len(player.boats[boatindex].crew))
    boatStatsView.append(player.boats[boatindex].size)
    boatStatsView.append(player.boats[boatindex].cost)
    boatStatsView.append(player.boats[boatindex].loc)
    for x in range(len(boatStatsView)):
        boatStatsView[x] = str(boatStatsView[x])
    return boatStatsView

class Player:
    def __init__(self, name):
        self.pnum = len(playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = []
        self.stats = str(self.name + '  Money: '+str(self.money)+'  Boats: '+str(len(self.boats))+'  Staff: '+str(len(self.staff)))
        self.frame = []
        self.labels = []
        self.buttons = []
        currentPs = len(playerList)
        playerList.append(self)
        self.frame = LabelFrame(root, text=name)
        self.frame.grid(row=help1[currentPs], column=help2[currentPs], rowspan=1, columnspan=1, padx=20, pady=20)

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
    
    def redoStats(self):
        self.stats = str(self.name + '  Money: '+str(self.money)+'  Boats: '+str(len(self.boats))+'  Staff: '+str(len(self.staff)))


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
        boatStatsView = []
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
        player.redoStats()
        player.labels[0].configure(text=player.stats)
        player.labels[currentboats+1].configure(image=boat_img)
        player.labels[currentboats+1].image = boat_img
        boatStatsView = getStats(player, currentboats)
        player.labels[currentboats+1].configure(text = boatStatsView[0]+'\n'+boatStatsView[1]+
        '\nHolding: '+boatStatsView[2]+' / '+boatStatsView[3]+
        ' kg\nCrew: '+boatStatsView[4]+' / '+boatStatsView[5]+
        '\nSells for: £'+boatStatsView[6]+
        '0 \nCurrently: '+boatStatsView[7], font='Arial 10 bold')
             
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
selection = 1
forSaleBoats[selection].buyBoat(player1, forSaleNames[selection], 'H.M.S. Dabb')
selection = 4
forSaleBoats[selection].buyBoat(player2, forSaleNames[selection], 'H.M.S. Scramble')
selection = 5
forSaleBoats[selection].buyBoat(player2, forSaleNames[selection], 'H.M.S. Munchie')

print(player1.labels)

root.mainloop()
