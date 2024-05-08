# Material ref: 
'''
    0 DOOR 2500
    1 OUTSIDE DOOR 8500
    2 WINDOW 3450
    3 WALL 75000
    4 TOILET 2995
    5 TAB 2350
    6 SHOWER 8300
'''
import random
from material_agent import MaterialAgent
from builder_agent import BuilderAgent

BUILDER_COUNT = 10
CROSSOVER_RATE = 0.6
MUATATION_RATE = 0.05
INITIAL_FUNDS = 1000000

def init_pop():
    return [BuilderAgent(INITIAL_FUNDS) for _ in range(BUILDER_COUNT)]

def evaluate(population):
    return [builder.CalcFitness() for builder in population]

def select(indexes, fitnesses):
    total_fitness = sum(fitnesses)
    cum_fitness = [f / total_fitness for f in fitnesses]
    #cum_fitness = [sum(cum_fitness[:i+1]) for i in range(len(cum_fitness))]
    parents = random.choices(indexes, weights=cum_fitness, k=2)
    return parents[0], parents[1]

def crossover(builder1: BuilderAgent, builder2: BuilderAgent):
    if random.random() < CROSSOVER_RATE:
        cp = random.randint(0, len(builder1.BuildOrder) - 1)
        builder1.BuildOrder = builder1.BuildOrder[:cp] + builder2.BuildOrder[cp:]
        builder2.BuildOrder = builder2.BuildOrder[:cp] + builder1.BuildOrder[cp:]
        return builder1, builder2
    else:
        return builder1, builder2

def Run():
    g = 0
    population = init_pop()
    fitnesses = evaluate(population)
    print(fitnesses)
    matAgent = MaterialAgent()

    #while max(fitnesses) < 1:
    for g in range(100):
        if any(matAgent.Inventory[i] == 0 for i in range(len(matAgent.Inventory))):
            matAgent.Restock()
        #print(matAgent.Inventory)
        g += 1
        for i in range(len(population)//2):
            i1, i2 = select(range(0, len(population)), fitnesses)
            population[i1], population[i2] = crossover(population[i1], population[i2])
            population[i1].Mutate(MUATATION_RATE)
            population[i2].Mutate(MUATATION_RATE)

        fitnesses = evaluate(population)
        #population.sort(key=lambda b: b.Fitness, reverse=True)
        buy = select(range(0, len(population)), fitnesses)
        for i in buy:
            population[i].TryBuy(matAgent)
        print(f"----GEN: {g}----")
        for i in range(len(population)):
            print(population[i].BuildOrder)
            print(population[i].Fitness)
            print(population[i].Funds)


Run()