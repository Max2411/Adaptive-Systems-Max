class Policy:
    """This class defines the action that will be taken in each state"""
    def __init__(self):
        self.actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.actions_list = [[0, 0, 0, 4],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [4, 0, 0, 0]]  # 4 is done to print the circle in the terminal

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

    def __str__(self) -> None:
        """
        Prints a grid of the action that are to be taken in each state.
        """
        arrow_list = ["↑", "→", "↓", "←", "○"]  # List of symbols that resemble each action.
        print("Policy:")
        for row in self.actions_list:
            line = ""
            for item in row:
                line += f"{arrow_list[item]}".ljust(10)
            print(line)
        print("--------------------------")
