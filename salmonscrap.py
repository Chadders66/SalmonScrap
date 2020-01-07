import json

startingMoney = 4000
playerList = []

with open('SalmonScrap/v0.2/boats.json') as json_file:
    boats = json.load(json_file)

class Player:
    def __init__(self, name):
        self.pnum = len(playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = 0
        playerList.append(self)

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

    def buyBoat(self, player, choice, newname):            #add boat to player.boats
        self.name = newname
        self.type = choice
        self.hold = 0
        self.crew = []
        self.cost = (boats[choice]['cost'])*0.6
        self.relB = boats[choice]['relB']
        self.relI = boats[choice]['relI']
        self.cspB = boats[choice]['cspB']
        self.cspI = boats[choice]['cspI']
        self.loc = "In Harbour"
        player.money = player.money - boats[choice]['cost']
        player.boats.append(self)
        

def initBoats():
    global fishingBoat
    global longliner
    global smallYacht
    global yacht
    global smallTrawler
    global trawler
    global smallSeine
    global seineBoat
    fishingBoat = Boat('Fishing Boat')
    longliner = Boat('Longliner')
    smallYacht = Boat('Small Yacht')
    yacht = Boat('Yacht')
    smallTrawler = Boat('Small Trawler')
    trawler = Boat('Trawler')
    smallSeine = Boat('Small Seine')
    seineBoat = Boat('Seine Boat')

initBoats()

player1 = Player("Andrew")

player1.printStats()

fishingBoat.buyBoat(player1, 'Fishing Boat', 'H.M.S. Riven')

