from Maze import Maze
from Policy import Policy


class Agent:
    def __init__(self, start_state):
        self.policy = Policy()
        self.maze = Maze()
        self.state = start_state
        self.discount = 1

    def value_function(self):

        location = self.state[0]
        table_for_next_loc = self.create_action_list(location)
        value = 0
        for shift_for_next_loc in table_for_next_loc:
            coord = list(map(lambda x, y: x + y, shift_for_next_loc, location))
            new_value = self.maze.rewards[coord[0]][coord[1]] + self.discount * self.maze.value[coord[0]][coord[1]]
            if value < new_value:
                value = new_value
        self.maze.value[location[0]][location[1]] = value

    def value_iteration(self):      # TODO
        potential_actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        while not self.state[2]:    # TODO get different while statement for stop
            new_value_list = [[0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]]
            for location in self.maze.locations:
                actions = self.create_action_list(location)
                old_value = self.maze.value[location[0]][location[1]]
                new_values = []
                for action in actions:

                    next_loc = list(map(lambda x, y: x + y, location, action))
                    new_values.append(self.maze.rewards[next_loc[0]][next_loc[1]] + self.discount * self.maze.value[next_loc[0]][next_loc[1]])
                if not self.maze.done_list[location[0]][location[1]]:
                    max_value = max(new_values)
                    new_value_list[location[0]][location[1]] = max_value
                    new_best_action = potential_actions.index(actions[new_values.index(max_value)])
                    self.policy.actions_list[location[0]][location[1]] = new_best_action
            if new_value_list == self.maze.value:
                print(self.policy.__str__())
                break
            self.maze.value = new_value_list
            self.action()
            self.__str__()

    def create_action_list(self, location):
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


    def action(self):
        """Goes to next state on based on the action obtained out of the policy."""
        location = self.state[0]
        action = self.policy.pick_action(self.maze.value, self.state)
        if action == 0:
            self.state[0] = [self.state[0][0]-1, self.state[0][1]]
        elif action == 1:
            self.state[0] = [self.state[0][0], self.state[0][1]+1]
        elif action == 2:
            self.state[0] = [self.state[0][0]+1, self.state[0][1]]
        elif action == 3:
            self.state[0] = [self.state[0][0], self.state[0][1]-1]

    def __str__(self):
        for row in self.maze.value:
            line = ""
            for item in row:
                line += f"{item}".ljust(10)
            print(line)
        print("--------------------------")



if __name__ == "__main__":
    start_state = [[3,2], 0, False]
    agent1 = Agent(start_state)
    agent1.value_iteration()
    # for i in range(100000):
    #     agent1.value_function()
    #     agent1.action()
