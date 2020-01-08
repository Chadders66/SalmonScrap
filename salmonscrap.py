import json

startingMoney = 4000
playerList = []

with open('boats.json') as json_file:
    boats = json.load(json_file)

class Player:
    def __init__(self, name):
        self.pnum = len(playerList)+1
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = []
        playerList.append(self)

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


    def buyBoat(self, player, choice, newname):            #add boat to player.boats
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

