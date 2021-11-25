class Policy:
    def __init__(self):
        self.actions = 0
        self.location = [0, 0]  # extract current location
        self.actions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.actions_list = [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
        # self.actions_list = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0,
        #                      (1, 0): 0, (1, 1): 0, (1, 2): 0, (1, 3): 0,
        #                      (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 0,
        #                      (3, 0): 0, (3, 1): 0, (3, 2): 0, (3, 3): 0}

    def pick_action(self, values, state) -> int:  # TODO
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
