from tkinter import *
from PIL import ImageTk,Image
import json
import os
import random
import math

path = ''

startingMoney = 4000
playerList = []
forSaleBoats = []
forSaleNames = ['Fishing Boat', 'Longliner', 'Small Yacht', 'Yacht', 'Small Trawler', 'Trawler', 'Small Seine', 'Seine Boat']
imageList = []

help1 = [0, 0, 2, 2]
help2 = [0, 2, 0, 2]

help3 = [0, 0, 1, 1]
help4 = [0, 1, 0, 1]

with open(path + 'boats.json') as json_file:
    boats = json.load(json_file)

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1000x600")


class Gamestate:
    def __init__(self):
        self.turn = 0

    def nextTurn(self):
        self.turn += 1
        
def initBoats():
    for x in range(len(forSaleNames)):
        forSaleBoats.append(Boat(forSaleNames[x]))

def resizeImages():
    for x in range(len(forSaleNames)):
        imageList.append(Image.open(path + "assets/" + forSaleBoats[x].image)) #resize image
        imageList[x] = imageList[x].resize((165, 130), Image.ANTIALIAS)
    imageList.append(Image.open(path + "assets/blank.png"))
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
        self.staff = []
        self.frame = []
        self.labels = []
        currentPlayers = len(playerList)
        playerList.append(self)
        self.frame = LabelFrame(root, text=name, padx=20, pady=20)
        self.frame.grid(row=help1[currentPlayers], column=help2[currentPlayers], rowspan=2, columnspan=2, padx=10, pady=5)

    def printStats(self):
        print("Player %d (%s):  Money: %s" %(self.pnum,self.name,self.money))

    def update(self):
        game.nextTurn()
        if game.turn % 28 == 27:
            for x in range (len(self.staff)):                                   #Paying Wages
                self.money = self.money - (self.staff[x].count('N') * 100)      #Novice weekly wages
                self.money = self.money - (self.staff[x].count('E') * 200)      #Expert weekly wages
                self.money = self.money - (self.staff[x].count('V') * 300)      #Veteran weekly wages
        
        if len(self.staff) > 0:
            for x in range (len(self.boats)):
                self.boats[x].relB = (self.boats[x].relB +                  #Calculating relibility
                (self.staff[x].count('N') * 0.4 * self.boats[x].relI) +     #Novice reliability multiplier
                (self.staff[x].count('E') * 0.75 * self.boats[x].relI) +    #Expert reliability multiplier
                (self.staff[x].count('V') * 1 * self.boats[x].relI))        #Veteran reliability multiplier
                if self.boats[x].relB > 100:                                #Reliability cap
                    self.boats[x].relB = 100
        #for x in range(len(self.boats)):                                   #Dice roll vs reliability
            #if random.randrange(1,100,1) > self.boats[x].relB:
                    #print('"The boat\'s fucked m8"') 
            
        loc = self.boats[x].loc
        if len(self.staff) > 0:
            for x in range (len(self.boats)):
                cspt = ((self.boats[x].cspB +
                (self.staff[x].count('N') * 0.5 * self.boats[x].cspI) +        #Novice catch speed multiplier
                (self.staff[x].count('E') * 1 * self.boats[x].cspI) +          #Expert catch speed multiplier
                (self.staff[x].count('V') * 1.5 * self.boats[x].cspI))         #Expert catch speed multiplier
                * (0.001 * self.boats[x].cap))                                 #10x the % of max hold caught
                haul = (cspt * locations[loc].fishab)
                self.boats[x].hold = self.boats[x].hold + (haul)
                if self.boats[x].hold > self.boats[x].cap:                     #Catch hold cap
                    self.boats[x].hold = self.boats[x].cap
                locations[loc].amtfished = locations[loc].amtfished + (cspt / 100)      #Updating amtfished in locations
                locations[loc].pimult = math.pi * (locations[loc].amtfished / 5)        #"locations[loc].amtfished / X" means X
                #is how quick fish run out, lower means they run out faster
                if locations[loc].amtfished > 5:
                    locations[loc].amtfished = 5
                locations[loc].fishab = ((0.9 * math.cos(locations[loc].pimult) + 1.1) / 2)
                print('Hold ' + str(player1.boats[0].hold))
                print('Last haul ' + str(haul))

        for x in range (len(locations)):
            if len(locations[x].sailing) == 0:
                locations[x].turnsempty = locations[x].turnsempty + 1
                locations[x].regrowth = (math.cos(math.pi * locations[x].fishab) +1)
                locations[x].amtfished = locations[x].amtfished - locations[x].regrowth
                if locations[x].amtfished < 0:
                    locations[x].amtfished = 0
            elif len(locations[x].sailing) > 0:
                locations[x].turnsempty = 0


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

    def buyBoat(self, player, choice, newname):  #e.g. forSaleBoats[selection].buyBoat(player1, forSaleNames[selection], 'H.M.S. 1')
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
            
    def hire(self, player, boat, rank, hirereq):        #e.g. player1.boats[0].hire(player1, 0, 'N', 1)
        if hirereq + len(self.crew) > self.size:
            print('Crew cannot exceed boat capacity')
        else:
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

class Location:
    def __init__(self, name):
        self.name = name
        self.bdamage = 0
        self.temp = 0
        self.waves = 0                                              
        self.rain = 0                                              
        self.sailing = []                                          
        self.fishtype = []                                         
        self.amtfished = 0                                         
        self.fishab = 1                                            
        self.regrowth = 0
        self.turnsempty = 0
locations = []
locations.append(Location('Harbour'))
locations.append(Location('Coast'))
locations.append(Location('Ocean'))
locations.append(Location('Deep Sea'))

def initLoc():
    locations[0].bdamage = 0
    locations[0].temp = random.randrange(1,3,1)
    locations[0].waves = random.randrange(1,3,1)
    locations[0].rain = random.randrange(1,3,1)
    locations[0].fishtype.append('Tiddlers')
    locations[1].bdamage = 5
    locations[1].temp = random.randrange(1,5,1)
    locations[1].waves = random.randrange(1,5,1)
    locations[1].rain = random.randrange(1,5,1)
    locations[1].fishtype.append('Salmon')
    locations[2].bdamage = 10
    locations[2].temp = random.randrange(1,10,1)
    locations[2].waves = random.randrange(1,10,1)
    locations[2].rain = random.randrange(1,10,1)
    locations[2].fishtype.append('idk? big ones or smth')
    locations[3].bdamage = 20
    locations[3].temp = random.randrange(5,15,1)
    locations[3].waves = random.randrange(5,15,1)
    locations[3].rain = random.randrange(5,15,1)
    locations[3].fishtype.append('yo momma')

def travel(self, boat, locfrom, locto):
    locations[locto].append(player1.boats[boat])
    locations[locfrom].remove(player1.boats[boat])

weather = random.randrange(1,10,1)

initBoats()

resizeImages()

initLoc()

game = Gamestate()

player1 = Player("Andrew")
player2 = Player("Chadders")

populateFrames()

root.mainloop()