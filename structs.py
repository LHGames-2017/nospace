import math
#           lvl,value, cost
HEALTHLVL = {0:[5,0],
             1:[8,10000],
             2:[10,20000],
             3:[15,30000],
             4:[20,50000],
             5:[30,100000]}

ATTACKLVL = {0:[1,0],
             1:[3,15000],
             2:[5,50000],
             3:[7,100000],
             4:[9,250000],
             5:[11,500000]}

DEFENSELVL = {0:[1,0],
             1:[3,15000],
             2:[5,50000],
             3:[7,100000],
             4:[9,250000],
             5:[11,500000]}

COLSPEEDLVL = {0:[1.0,0],
             1:[1.25,15000],
             2:[1.5,50000],
             3:[2,100000],
             4:[2.5,250000],
             5:[3.5,500000]}

CAPACITYLVL = {0:[1000,0],
             1:[1500,15000],
             2:[2500,50000],
             3:[5000,100000],
             4:[10000,250000],
             5:[25000,500000]}

class ActionTypes():
    DefaultAction, MoveAction, AttackAction, CollectAction, UpgradeAction, StealAction, PurchaseAction = range(7)

class UpgradeType():
    CarryingCapacity, AttackPower, Defence, MaximumHealth, CollectingSpeed = range(5)


class TileType():
    Tile, Wall, House, Lava, Resource, Shop = range(6)


class TileContent():
    Empty, Wall, House, Lava, Resource, Shop, Player = range(7)

class Upgrades(object):
    levels = {}
    def __init__(self, lvl=0):
        self.Lvl=0
    
    def upgrade():
        self.Lvl = self.Lvl + 1
    
    def nextLvl(currentLvl):
        if currentLvl+1<5:
            return currentLvl+1
        else:
            return -1
    def nextLvlprice(currentLvl):
        nxtlvl = nextLvl(currentLvl)
        if nxtlvl!=-1:
            return levels[nxtlvl][1]
        return -1
    def setLvls(levelDict):
        self.levels=levelDict


class Point(object):

    # Constructor
    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    # Overloaded operators
    def __add__(self, point):
        return Point(self.X + point.X, self.Y + point.Y)

    def __sub__(self, point):
        return Point(self.X - point.X, self.Y - point.Y)

    def __str__(self):
        return "{{{0}, {1}}}".format(self.X, self.Y)

    # Distance between two Points
    def Distance(self, p1, p2):
        delta_x = p1.X - p2.X
        delta_y = p1.Y - p2.Y
        return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


class GameInfo(object):

    def __init__(self, json_dict):
        self.__dict__ = json_dict
        self.HouseLocation = Point(json_dict["HouseLocation"])
        self.Map = None
        self.Players = dict()


class Tile(object):

    def __init__(self, content=None, x=0, y=0):
        self.Content = content
        self.X = x
        self.Y = y


class Player(object):

    def __init__(self, health, maxHealth, position, houseLocation, score, carriedRessources,
                 carryingCapacity=1000):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position
        self.HouseLocation = houseLocation
        self.Score = score
        self.CarriedRessources = carriedRessources
        self.CarryingCapacity = carryingCapacity

        

class PlayerInfo(object):

    def __init__(self, health, maxHealth, position):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position

class ActionContent(object):

    def __init__(self, action_name, content):
        self.ActionName = action_name
        self.Content = str(content)
