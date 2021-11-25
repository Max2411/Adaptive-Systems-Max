# from Agent import Agent
# from Policy import Policy


class Maze:

    def __init__(self):
        self.locations = [[0, 0], [0, 1], [0, 2], [0, 3],
                          [1, 0], [1, 1], [1, 2], [1, 3],
                          [2, 0], [2, 1], [2, 2], [2, 3],
                          [3, 0], [3, 1], [3, 2], [3, 3]]     # ????
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
        self.actions_list = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    def step(self, state, action) -> [list, int, int]:
        location = state[0]
        reward = state[1]
        done = state[2]
        if action == 0:
            location = list(map(lambda x, y: x + y, state, [-1, 0]))
        elif action == 1:
            location = list(map(lambda x, y: x + y, state, [0, 1]))
        elif action == 2:
            location = list(map(lambda x, y: x + y, state, [1, 0]))
        elif action == 3:
            location = list(map(lambda x, y: x + y, state, [0, -1]))
        reward = reward + self.rewards[location[0]][location[1]]
        done = self.done_list[location[0]][location[1]]
        return [location, reward, done]

    def __str__(self) -> None:
        [print(row) for row in self.rewards]


if __name__ == "__main__":
    maze = Maze()
    print(maze.value)
    print(maze.rewards)
