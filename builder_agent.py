import random
from material_agent import MaterialAgent
'''
    DOOR
    OUTSIDE_DOOR
    WINDOW
    WALL
    TOILET
    TAB
    SHOWER
    HOUSE
    FLOOR
    GARRET
    HALL
    BED_ROOM
    BATH_ROOM
    LIVING_ROOM
'''
HOUSE =       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
FLOOR =       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 2, 1]
GARRET =      [1, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
HALL =        [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
BED_ROOM =    [1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
BATH_ROOM =   [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
LIVING_ROOM = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
COMPONENTS =  [HOUSE, FLOOR, GARRET, HALL, BED_ROOM, BATH_ROOM, LIVING_ROOM]
INDIVIDUAL_SIZE = 11
REQUIRED_COMPS = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 4, 2, 1]

class BuilderAgent:
    def __init__(self, funds):
        self.Inventory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.MissingItems = [0, 0, 0, 0, 0, 0, 0]
        self.BuildOrder = [random.randint(0,6) for _ in range(INDIVIDUAL_SIZE)]
        self.Funds = funds
        self.Fitness = 1/12

    def CalcFitness(self):
        fitness = 0
        self.MissingItems = [0,0,0,0,0,0,0]
        for action in self.BuildOrder:
            if self._TryBuild(COMPONENTS[action]) and self.Inventory[action+7] < REQUIRED_COMPS[action+7]:
                self.Inventory = [self.Inventory[i] - COMPONENTS[action][i] for i in range(len(self.Inventory))]
                self.Inventory[action+7] += 1
                fitness += 1
        self.Fitness += (fitness / 12)
        return self.Fitness


    def _TryBuild(self, component):
        for i in range(len(component)):
            if self.Inventory[i] < component[i]:
                if i < 7:
                    self.MissingItems[i] = component[i] - self.Inventory[i]
                return False
        return True
    
    def Mutate(self, mr):
        for i in range(len(self.BuildOrder)):
            if random.random() < mr:
                self.BuildOrder[i] = random.randint(0,6)

    def TryBuy(self, matAgent: MaterialAgent):
        for i in range(len(self.MissingItems)):
            if matAgent.Inventory[i] > self.MissingItems[i] and self.Funds > matAgent.Prices[i] * self.MissingItems[i]:
                self.Funds -= matAgent.Prices[i] * self.MissingItems[i]
                self.Inventory[i] += self.MissingItems[i]
                matAgent.Inventory[i] -= self.MissingItems[i]
                self.MissingItems[i] = 0

    def __repr__(self):
        return f'''INVENTORY: {self.Inventory}
                  BuildOrder: {self.BuildOrder}
                  MissingItems: {self.MissingItems}
                  Funds: {self.Funds}
                  Fitness: {self.Fitness}'''