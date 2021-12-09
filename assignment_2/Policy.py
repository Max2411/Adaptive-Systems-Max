import random


class Policy:
    """This class defines the action that will be taken in each state"""
    def __init__(self):
        self.actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.actions_list = [[0, 0, 0, 4],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [4, 0, 0, 0]]  # 4 is done to print the circle in the terminal
        self.actions_list2 = [[[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0,0,0,0]],
                              [[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]],
                              [[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]],
                              [[0,0,0,0],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]]
        self.actions_list2_greedy = [[0.025, 0.925, 0.025, 0.025],[0.025, 0.925, 0.025, 0.025],[0.025, 0.925, 0.025, 0.025],[0, 0, 0, 0],
                                     [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025],
                                     [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025], [0.025, 0.025, 0.025, 0.925], [0.025, 0.025, 0.025, 0.925],
                                     [0, 0, 0, 0], [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025], [0.925, 0.025, 0.025, 0.025],]

    def pick_action(self, values, state) -> int:
        """
        Picks and saves the action that will be made in the current state.
        """
        location = state[0]
        test_value = 0
        for i, shift_for_next_loc in enumerate(self.actions):
            try:
                x, y = list(map(lambda x, y: x + y, shift_for_next_loc, location))
                new_value = values[x][y]
                if test_value < new_value:
                    test_value = new_value
                    self.actions_list[location[0]][location[1]] = i
            except:
                continue
        return self.actions_list[location[0]][location[1]]

    def random_policy(self):
        for i in range(4):
            for j in range(4):
                actions = [0, 1, 2, 3]
                if i == 0:
                    actions.pop(0)
                if i == 3:
                    actions.pop(2)
                if j == 0:
                    actions.pop(3)
                if j == 3:
                    actions.pop(1)

                self.actions_list[i][j] = random.choice(actions) if self.actions_list[i][j] == 0 else self.actions_list[i][j]

    def __str__(self, action_list:list) -> None:
        """
        Prints a grid of the action that are to be taken in each state.
        """
        if isinstance(action_list[0][0], list):
            arrow_list = ["↑", "→", "↓", "←", "○"]  # List of symbols that resemble each action.
            print("Policy:")
            for row in action_list:
                line = ""
                for item in row:
                    if len(set(item)) == 1 and item[0] == 0:
                        action = 4
                    else:
                        action = item.index(max(item))
                    line += f"{arrow_list[action]}".ljust(10)
                print(line)
        else:
            arrow_list = ["↑", "→", "↓", "←", "○"]  # List of symbols that resemble each action.
            print("Policy:")
            for row in action_list:
                line = ""
                for item in row:
                    line += f"{arrow_list[item]}".ljust(10)
                print(line)
        print("--------------------------")
