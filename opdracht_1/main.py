from Agent import Agent


if __name__ == "__main__":
    start_state = [[3,2], 0, False]
    agent1 = Agent(start_state)
    agent1.value_iteration()
    for i in range(100000):
        agent1.value_function()
        agent1.action()
    agent1.__str__()
