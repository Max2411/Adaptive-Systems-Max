from assignment_1.Maze import Maze
from assignment_1.Policy import Policy


class Agent:
    def __init__(self, start_state):
        self.policy = Policy()
        self.maze = Maze()
        self.state = start_state
        self.discount = 1

    def value_function(self) -> None:
        """This is the value function."""
        location = self.state[0]
        table_for_next_loc = self.create_action_list(location)
        value = 0
        for shift_for_next_loc in table_for_next_loc:
            coord = list(map(lambda x, y: x + y, shift_for_next_loc, location))
            new_value = self.maze.rewards[coord[0]][coord[1]] + self.discount * self.maze.value[coord[0]][coord[1]]
            if value < new_value:
                value = new_value
        self.maze.value[location[0]][location[1]] = value

    def value_iteration(self) -> None:
        """
        This is the value iteration.
        """
        potential_actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        while True:
            new_value_list = [[0, 0, 0, 0],     # Is to save the new values so that the old values can be used for
                              [0, 0, 0, 0],     # the calculations.
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]]
            for location in self.maze.locations:    # Loops through all states
                actions = self.create_action_list(location) # Creates all possible action you van make in a state.
                new_values = []     # List of all generated values.
                for action in actions:  # Loops through all possible actions.

                    next_loc = list(map(lambda x, y: x + y, location, action))
                    new_values.append(self.maze.rewards[next_loc[0]][next_loc[1]] + self.discount * self.maze.value[next_loc[0]][next_loc[1]])
                if not self.maze.done_list[location[0]][location[1]]:
                    max_value = max(new_values)
                    new_value_list[location[0]][location[1]] = max_value    # Updates the value for the current state with the optimal value
                    new_best_action = potential_actions.index(actions[new_values.index(max_value)])     # Selects the best action
                    self.policy.actions_list[location[0]][location[1]] = new_best_action    # Saves the best possible action.
            if new_value_list == self.maze.value:       # Breaks the loop if there are no more changes
                print(self.policy.__str__())
                break
            self.maze.value = new_value_list    # Updates value list.
            self.action()
            self.__str__()

    def create_action_list(self, location):
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
            self.state[0] = [x-1, y]
        elif action == 1:
            self.state[0] = [x, y+1]
        elif action == 2:
            self.state[0] = [x+1, y]
        elif action == 3:
            self.state[0] = [x, y-1]

    def __str__(self) -> None:
        """
        Prints a grid of the values of each state.
        """
        print("Values:")
        for row in self.maze.value:
            line = ""
            for item in row:
                line += f"{item}".ljust(10)
            print(line)
        print("--------------------------")
