from assignment_2.Agent import Agent


if __name__ == "__main__":
    start_state = [[3, 2], 0, False]
    agent1 = Agent(start_state, discount=1)
    agent2 = Agent(start_state, discount=0.9)
    agent1.monte_carlo_evaluation()
    # agent1.td_evaluation()
    # for i in range(20):
    #     print("---------------")
    #     print(agent2.create_episode())
    # agent1.value_iteration()
    # print(agent1.optimal_policy)