import random
from statistics import mean
from typing import Optional

from assignment_2.Maze import Maze
from assignment_2.Policy import Policy


class Agent:
    def __init__(self, start_state, discount: float = 1, iteratie: int = 10000):
        self.policy = Policy(discount)
        self.maze = Maze()
        self.state = start_state
        self.discount = discount
        self.iteratie = iteratie

    def value_function(self) -> None:
        """
        This is the value function.
        """
        location = self.state[0]
        table_for_next_loc = self.create_action_list(location)
        value = 0
        for shift_for_next_loc in table_for_next_loc:
            coord = list(map(lambda x, y: x + y, shift_for_next_loc, location))
            new_value = self.maze.rewards[coord[0]][coord[1]] + self.discount * self.maze.value[coord[0]][coord[1]]
            if value < new_value:
                value = new_value
        self.maze.value[location[0]][location[1]] = value

    def value_iteration(self) -> [list]:
        """
        This is the value iteration.
        """
        potential_actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for i in range(self.iteratie):
            discount = self.discount ** i
            new_value_list = [[0, 0, 0, 0],  # Is to save the new values so that the old values can be used for
                              [0, 0, 0, 0],  # the calculations.
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]]
            for location in self.maze.locations:  # Loops through all states
                actions = self.create_action_list(location)  # Creates all possible action you van make in a state.
                new_values = []  # List of all generated values.
                for action in actions:  # Loops through all possible actions.

                    next_loc = list(map(lambda x, y: x + y, location, action))
                    new_values.append(
                        self.maze.rewards[next_loc[0]][next_loc[1]] + discount * self.maze.value[next_loc[0]][
                            next_loc[1]])
                if not self.maze.done_list[location[0]][location[1]]:
                    max_value = max(new_values)
                    new_value_list[location[0]][
                        location[1]] = max_value  # Updates the value for the current state with the optimal value
                    new_best_action = potential_actions.index(
                        actions[new_values.index(max_value)])  # Selects the best action
                    self.policy.actions_list[location[0]][
                        location[1]] = new_best_action  # Saves the best possible action.
            if new_value_list == self.maze.value:  # Breaks the loop if there are no more changes
                print(self.policy.__str__(self.policy.actions_list))
                break
            self.maze.value = new_value_list  # Updates value list.
            self.action()
            self.__str__()
        return self.policy.actions_list

    def monte_carlo_evaluation(self) -> None:
        """
        This is the monte carlo evaluation.
        """
        values = [[0, 0, 0, 0],  # New values.
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        value_times = [[0, 0, 0, 0],  # Times this state has been used for calculations.
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]
        for i in range(self.iteratie):
            g = 0
            episodes = self.create_episode()
            discount = self.discount ** i
            check = list(reversed(list(episodes.copy())))  # copy of episodes for checking purposes.
            for episode in reversed(list(episodes)):
                state, action, reward = episode
                x, y = state
                check.remove(episode)  # removes state to check if there are more of the same states in the episodes
                g = discount * g + reward
                if (check is None or episode not in check) and not self.maze.done_list[x][
                    y]:  # is none is for the last state
                    value_times[x][y] += 1  # Add 1 to the times this state has been used for calculations
                    values[x][y] = values[x][y] + (g - values[x][y]) / value_times[x][
                        y]  # Formula to add a number to a calculated average.
        self.maze.value = values
        self.__str__()

    def td_evaluation(self) -> None:
        """
            Temperal differance learning.
        """
        alpha = 1

        for i in range(self.iteratie):
            x, y = [random.randint(0, 3), random.randint(0, 3)]  # For random start
            discount = self.discount ** i  # calculating discount
            while not self.maze.done_list[x][y]:
                # action = random.randint(0, 3)       # for random policy
                action = self.policy.actions_list_optimal[x][y]  # for optimal policy
                next_state, reward = self.maze.step([x, y], action)
                current_val = self.maze.value[x][y]
                next_val = self.maze.value[next_state[0]][next_state[1]]
                self.maze.value[x][y] = current_val + alpha * (
                            reward + discount * next_val - current_val)  # update value
                x, y = next_state  # change x, y coordinates to the ones from the next state
        self.__str__()

    def monte_carlo_control(self) -> None:  # TODO
        """
        This is monte carlo control. In this function defines the 'epsilon' parameter only the chance to get the correct
        path. The function will pick a random other path if it doesn't pick the optimal path. All other paths have the
        same chance of being picked if the correct path is not chosen.
        """
        epsilon = 93
        values = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        value_times = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]
        value_times_all_actions = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                                   # TODO remove if unnecessary
                                   [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                                   [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                                   [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        for i in range(self.iteratie):
            g = 0  # start g
            episodes = self.create_episode(epsilon=epsilon)  # create episode
            discount = self.discount ** i  # calculates the discount
            check = list(reversed(list(episodes.copy())))  # copy of episodes for checking purposes
            for episode in reversed(list(episodes)):
                state, action, reward = episode
                x, y = state
                check.remove(episode)  # removes state to check if there are more of the same states in the episodes

                g = discount * g + reward  # calculate new g
                if (check is None or episode not in check) and not self.maze.done_list[x][
                    y]:  # is none is for the last state
                    value_times[x][y] += 1  # Add 1 to the times this state has been used for calculations
                    values[x][y] = values[x][y] + (g - values[x][y]) / value_times[x][
                        y]  # Formula to add a number to a calculated average.
        self.maze.value = values
        self.__str__()

    def sarsa(self) -> None:  # TODO
        """
        This is a SARSA function for policy control.
        """
        alpha = 1
        possible_actions = [0, 1, 2, 3]
        epsilon = 93
        policy = self.policy.actions_list2
        values_list = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        for i in range(self.iteratie):
            x, y = [random.randint(0, 3), random.randint(0, 3)]  # For random start
            discount = self.discount ** i  # calculating discount
            action = self.soft_policy(self.policy.actions_list2[x][y], epsilon)
            while not self.maze.done_list[x][y]:
                # action = self.optimal_policy[x][y]  # for optimal policy
                if action in possible_actions:
                    next_state, reward = self.maze.step([x, y], action)
                    next_action = self.soft_policy(policy[next_state[0]][next_state[1]])
                    current_val = policy[x][y][action]
                    next_val = policy[next_state[0]][next_state[1]][next_action]
                    policy[x][y][action] = current_val + alpha * (reward + discount * next_val - current_val)
                    x, y = next_state
                    action = next_action
        self.policy.__str__(self.policy.actions_list2)

    def sarsa_max(self):
        """
        This is a SARSA Max/Q learning function for policy control.
        """
        alpha = 1
        possible_actions = [0, 1, 2, 3]
        epsilon = 93
        policy = self.policy.actions_list2
        values_list = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                       [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        for i in range(self.iteratie):
            x, y = [random.randint(0, 3), random.randint(0, 3)]  # For random start
            discount = self.discount ** i  # calculating discount
            action = self.soft_policy(self.policy.actions_list2[x][y], epsilon)
            while not self.maze.done_list[x][y]:
                # action = self.optimal_policy[x][y]  # for optimal policy
                if action in possible_actions:
                    next_state, reward = self.maze.step([x, y], action)
                    next_action = self.soft_policy(policy[next_state[0]][next_state[1]], epsilon)
                    current_val = policy[x][y][action]
                    max_val_index = policy[next_state[0]][next_state[1]].index(max(policy[next_state[0]][next_state[1]]))
                    next_val = policy[next_state[0]][next_state[1]][max_val_index]
                    policy[x][y][action] = current_val + alpha * (reward + discount * next_val - current_val)
                    x, y = next_state
                    action = next_action
        self.policy.__str__(self.policy.actions_list2)

    def create_episode(self, epsilon: int = 100) -> [list, int, int]:
        """create episodes. Epsilon 100 is greedy, epsilon < 100 is soft_policy"""
        episodes = []
        done = False
        state = [random.randint(0, 3), random.randint(0, 3)]  # random start
        while not done:
            action_list = [0, 1, 2, 3]
            # action = random.randint(0,3)        # random
            action = self.policy.actions_list_optimal[state[0]][state[1]]
            if action in action_list:
                chance = random.randint(0, 100)
                action_list.pop(action)
                if chance > epsilon:
                    action = random.choices(action_list)
            next_state, reward = self.maze.step(state, action)
            episodes.append([state, action, reward])
            state = next_state
            done = self.maze.done_list[state[0]][state[1]]
        return episodes

    def soft_policy(self, actions, epsilon: int = 92) -> int:
        """
        Simple soft poolicy that chances the action into a new random action based on the likely hood presented by
        epsilon
        """
        action_list = [0, 1, 2, 3]
        chance = random.randint(0, 100)
        action = actions.index(max(actions))
        action_list.pop(action)
        if chance > epsilon:
            return random.choices(action_list)[0]
        else:
            return action

    def Q_soft_policy(self, actions) -> int:
        chance = random.random()
        if actions[0] + actions[1] + actions[2] + actions[3] == 0:
            return 4
        if chance < actions[0]:
            return 0
        elif chance < actions[0] + actions[1]:
            return 1
        elif chance < actions[0] + actions[1] + actions[2]:
            return 2
        elif chance <= actions[0] + actions[1] + actions[2] + actions[3]:
            return 3

    def create_action_list(self, location) -> list:
        """
        Create a list with all the actions that are possible. If 1 action is not possible like for example going
        up, then the an action to stay in place will be created.
        """
        actions = []
        if location[0] != 0:
            actions.append([-1, 0])
        if location[1] != 3:
            actions.append([0, 1])
        if location[0] != 3:
            actions.append([1, 0])
        if location[1] != 0:
            actions.append([0, -1])
        if len(actions) < 4:
            actions.append([0, 0])
        return actions

    def action(self) -> None:
        """
        Goes to next state on based on the action obtained out of the policy.
        """
        x, y = self.state[0]
        action = self.policy.pick_action(self.maze.value, self.state)
        if action == 0:
            self.state[0] = [x - 1, y]
        elif action == 1:
            self.state[0] = [x, y + 1]
        elif action == 2:
            self.state[0] = [x + 1, y]
        elif action == 3:
            self.state[0] = [x, y - 1]

    def __str__(self) -> None:
        """
        Prints a grid of the values of each state.
        """
        print(f"Iteraties:{self.iteratie}, discount:{self.discount}, policy: optimal")
        print("Values:")
        for row in self.maze.value:
            line = ""
            for item in row:
                line += f"{round(item, 5)}".ljust(10)
            print(line)
        print("--------------------------")
