from builder_agent import BuilderAgent

agent = BuilderAgent(100000)
agent.BuildOrder = [6, 5, 5, 4, 4, 4, 4, 3, 2, 1, 0]
agent.Inventory = [20, 20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0]

agent.CalcFitness()
print(agent.Fitness)
print(agent.Inventory)