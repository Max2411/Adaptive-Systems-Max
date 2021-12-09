from assignment_1.Agent import Agent


if __name__ == "__main__":
    start_state = [[3, 2], 0, False]
    agent1 = Agent(start_state)
    agent1.value_iteration()
