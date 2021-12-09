
class Maze:
    def __init__(self):
        self.locations = [[0, 0], [0, 1], [0, 2], [0, 3],
                          [1, 0], [1, 1], [1, 2], [1, 3],
                          [2, 0], [2, 1], [2, 2], [2, 3],
                          [3, 0], [3, 1], [3, 2], [3, 3]]
        self.value = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.rewards = [[-1, -1, -1, 40],
                        [-1, -1, -10, -10],
                        [-1, -1, -1, -1],
                        [10, -2, -1, -1]]
        self.done_list = [[False, False, False, True],
                          [False, False, False, False],
                          [False, False, False, False],
                          [True, False, False, False]]
        self.actions = [0, 1, 2, 3]  # Up = 0, Right = 1, Down = 2, Left = 3
        self.actions_list = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # additives for an action to a new state.

    def step(self, state: list, action: int) -> [list, int]:
        """
        Takes a step in the maze based on the action given and returns a new state that consist of location, reward, a
        boolean that tels if a state is the end state.
        """
        location = state
        action_list = [0,1,2,3]
        new_location = [0,0]
        if action == 0:
            new_location = list(map(lambda x, y: x + y, state, [-1, 0]))
        elif action == 1:
            new_location = list(map(lambda x, y: x + y, state, [0, 1]))
        elif action == 2:
            new_location = list(map(lambda x, y: x + y, state, [1, 0]))
        elif action == 3:
            new_location = list(map(lambda x, y: x + y, state, [0, -1]))
        if new_location[0] not in action_list or new_location[1] not in action_list:
            new_location = location
        reward = self.rewards[new_location[0]][new_location[1]]
        return new_location, reward

    def __str__(self) -> None:
        """
        Prints a grid of all the rewards
        """
        print("Rewards:")
        for row in self.value:
            line = ""
            for item in row:
                line += f"{item}".ljust(10)
            print(line)
        print("--------------------------")
