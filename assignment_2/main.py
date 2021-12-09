from assignment_2.Agent import Agent


if __name__ == "__main__":
    start_state = [[3, 2], 0, False]
    agent1 = Agent(start_state, discount=1)
    agent2 = Agent(start_state, discount=0.9)
    # agent1.monte_carlo_evaluation()
    # agent2.monte_carlo_evaluation()
    # agent1.td_evaluation()
    # agent2.td_evaluation()
    agent1.monte_carlo_control()
    agent2.monte_carlo_control()
