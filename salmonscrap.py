from tkinter import *
from PIL import ImageTk,Image
import json
import os
import random
import math
import time

path = ''

startingMoney = 6000
forSaleBoats = []
forSaleNames = ['Fishing Boat', 'Longliner', 'Small Yacht', 'Yacht', 'Small Trawler', 'Trawler', 'Small Seine', 'Seine Boat']
imageList = []
masterButtons = []

help1 = [0, 0, 1, 1]
help2 = [0, 1, 0, 1]

help3 = [0, 0, 3, 3]
help4 = [0, 4, 0, 4]

help5 = [1, 1, 1, 2, 2, 2]
help6 = [0, 1, 2, 0, 1, 2]

help7 = [7, 7, 7]
help8 = [2, 3, 4]

help9 = [0, 0, 0, 0, 2, 2, 2, 2]
help10 = [0, 1, 4, 5, 0, 1, 4, 5]

with open(path + 'boats.json') as json_file:
    boats = json.load(json_file)

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1100x600+200+100")

class Gamestate:
    def __init__(self):
        self.turn = 0
        self.player = 'Andrew'
        self.playerList = []
        self.players = len(self.playerList)
        self.day = 'Monday'
        self.time = '10AM'
        self.daynum = 0
        self.timenum = 1
        self.week = 0
        self.dayList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.timeList = ['4AM', '10AM', '4PM', '10PM']
        self.stateString = self.player +' '+ self.day + ' ' + self.time + ' ' + str(self.week)

    def redoString(self):
        self.stateString = self.player.name +' '+ self.day + ' ' + self.time + ' ' + str(self.week)

    def nextTurn(self):
        if self.turn == self.players-1:
            self.turn = 0
            self.player = self.playerList[self.turn]
            if self.timenum == 3 and self.daynum < 6:
                self.timenum = 0
                self.time = self.timeList[self.timenum]
                self.daynum += 1
                self.day = self.dayList[self.daynum]
            elif self.timenum == 3 and self.daynum == 6:
                self.timenum = 0
                self.time = self.timeList[self.timenum]
                self.daynum = 0
                self.day = self.dayList[self.daynum]
                self.week += 1
            else:
                self.timenum += 1
                self.time = self.timeList[self.timenum]
        else:
            self.turn += 1
            self.player = self.playerList[self.turn]
        self.redoString()


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

def close(window):
    closed = window
    closed.destroy()
    playerEnable()

def mainDisable():
    for x in masterButtons:
        x.configure(state=DISABLED)

def mainEnable():
    for x in masterButtons:
        x.configure(state=NORMAL)

def playerEnable():
    mainDisable()
    player = game.playerList[game.turn]
    buttons = player.buttons
    for x in buttons:
        for y in x:
            y.configure(state=NORMAL)

def endTurnpop():
    mainDisable()
    endTurnPop = Toplevel()
    endTurnPop.geometry("250x120+620+300")
    conMessage = Label(endTurnPop, text='Are you sure you want to end your turn?', justify=CENTER)
    conMessage.grid(row=0, column=0, columnspan=2, pady=30, padx=10)
    turnButtons = []
    turnButtons.append(Button(endTurnPop, text='Confirm', width=10, command=lambda p=endTurnPop: conTurn(p)))
    turnButtons[0].grid(row=1, column=0)
    turnButtons.append(Button(endTurnPop, text='Cancel', width=10, command=lambda p=endTurnPop: close(p)))
    turnButtons[1].grid(row=1, column=1)

def conTurn(window):
    game.nextTurn()
    close(window)

def selBoat(selBoat, selList):
    index = forSaleNames.index(selBoat)
    if selList[index].cget('bg') == 'SystemButtonFace':
        for x in selList:
            x.configure(bg='SystemButtonFace')
        selList[index].configure(bg='Blue')
    else:
        selList[index].configure(bg='SystemButtonFace')

def conBoat(window, selList, player):
    for x in selList:
        if x.cget('bg') == 'Blue':
            selection = selList.index(x)
            forSaleBoats[selection].buyBoat(player, forSaleNames[selection], 'H.M.S. Riven')
    close(window)

def buyBoatpop():
    mainDisable()
    buyBoatPop = Toplevel()
    player = game.playerList[game.turn]
    buyBoatPop.title(player.name + ": choose a boat")
    buyBoatPop.geometry("950x400+280+180")
    saleLabels = []
    saleButtons = []
    for x in forSaleBoats:
        stats = (str(x.type))+'\n'+(str(x.desc))+'\n Holds '+(str(x.cap))+'kg of fish'+'\n Holds '+(str(x.size))+' crew members'+'\n £'+(str(x.cost))
        index = forSaleBoats.index(x)
        imagio = ImageTk.PhotoImage(imageList[index])
        saleLabels.append(Label(buyBoatPop, image=imagio, text=stats, justify=CENTER, compound=CENTER, font='Arial 10 bold'))
        saleLabels[index].image = imagio
        saleLabels[index].grid(row=help9[index], column=help10[index], padx=10, pady=10)
        saleButtons.append(Button(buyBoatPop, text=x.type, command=selBoat))
        saleButtons[index].configure(command=lambda h=x.type, i=saleLabels: selBoat(h, i))
        saleButtons[index].grid(row=(help9[index])+1, column=help10[index])
    saleButtons.append(Button(buyBoatPop, text='Confirm', width=10, command=lambda p=buyBoatPop, i=saleLabels, q=player: conBoat(p, i, q)))
    saleButtons[(len(saleButtons))-1].grid(row=4, column=2)
    saleButtons.append(Button(buyBoatPop, text='Cancel', width=10, command=lambda p=buyBoatPop: close(p)))
    saleButtons[(len(saleButtons))-1].grid(row=4, column=3)
    buyBoatPop.mainloop()
    
def sellFishpop():
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
    if len(game.playerList) > 4:
        print('Too many players!')
        exit()
    for x in range(len(game.playerList)):
        buttonList1 = []
        game.playerList[x].labels.append(Label(game.playerList[x].frame, text=game.playerList[x].stats))
        game.playerList[x].labels[0].grid(row=6, column=2, columnspan=3, padx=10, pady=10)
        for a in range(3):
            playerButtons = ['Sell Fish', 'End Turn', 'Buy Boat']
            playerCommands = [sellFishpop, endTurnpop, buyBoatpop]
            buttonList1.append(Button(game.playerList[x].frame, text=playerButtons[a], command=playerCommands[a]))
            masterButtons.append(buttonList1[a])
            buttonList1[a].grid(row=help7[a], column=help8[a])
        game.playerList[x].buttons.append(buttonList1)
        for y in range(4):
            noBoatStats = 'No boat to view \n Purchase a boat \n to view its stats'
            game.playerList[x].labels.append(Label(game.playerList[x].frame, image=img_blank, text=noBoatStats, justify=CENTER, compound=CENTER))
            game.playerList[x].labels[y+1].image = img_blank
            game.playerList[x].labels[y+1].grid(row=(help3[y]), column=(help4[y]), columnspan=3, padx=5, pady=10)
            buttonList2 = []
            for z in range(6):
                shipButtons = ['Hire', 'Launch', 'Rename', 'Fire', 'Sell', 'Repair']
                shipCommands = [hirepop, launchpop, renamepop, firepop, sellpop, repairpop]
                buttonList2.append(Button(game.playerList[x].frame, text=shipButtons[z], command=shipCommands[z], width=8))
                masterButtons.append(buttonList2[z])
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
            game.playerList[x].buttons.append(buttonList2)

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
        self.pnum = len(game.playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = []
        self.stats = str(self.name + '  Money: '+str(self.money)+'  Boats: '+str(len(self.boats))+'  Staff: '+str(len(self.staff)))
        self.frame = []
        self.labels = []
        self.buttons = []
        currentPs = len(game.playerList)
        game.playerList.append(self)
        game.players = len(game.playerList)
        self.frame = LabelFrame(root, text=name)
        self.frame.grid(row=help1[currentPs], column=help2[currentPs], rowspan=1, columnspan=1, padx=20, pady=20)

    def printStats(self):
        print("Player %d (%s):  Money: %s" %(self.pnum,self.name,self.money))
        
    def redoStats(self):
        self.stats = str(self.name + '  Money: '+str(self.money)+'  Boats: '+str(len(self.boats))+'  Staff: '+str(len(self.staff)))

    def update(self):
        game.nextTurn()
        if game.day == 'Friday':
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

playerEnable()

root.mainloop()
