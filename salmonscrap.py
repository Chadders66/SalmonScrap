startingMoney = 4000


class Player:
    def __init__(self, name):
        self.name = name
        self.money = startingMoney
        self.boats = []
        self.staff = 0

    def printStats(self):
        print("%s:  Money: %s  Boats: %s  Employees: %s" %(self.name,self.money,self.boats,self.staff))

##class Boat:

player1 = Player("Andrew")

player2 = Player("Chadders")

player1.printStats()
player2.printStats()