import numpy as np


class Robot:
    def __init__(self, beginning_position_x, beginning_position_y, map_size):
        self.x = beginning_position_x
        self.y = beginning_position_y
        self.map_size = map_size

    def __str__(self):
        return f"{self.x}, {self.y}"

    def move(self, x, y):
        """control the move of the robot"""
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x

        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        """when out of bounds"""
        if self.x < 0:
            self.x = 0
        elif self.x > self.map_size - 1:
            self.x = self.map_size -1
        if self.y < 0:
            self.y = 0
        elif self.y > self.map_size - 1:
            self.y = self.map_size -1

    def action(self, choice):
        """ the robot can move in eight directions"""
        if choice == 0:
            self.move(x=1, y=1)
        if choice == 1:
            self.move(x=1,y=-1)
        if choice == 2:
            self.move(x=-1,y=1)
        if choice == 3:
            self.move(x=-1,y=-1)
        if choice == 4:
            self.move(x=1,y=0)
        if choice == 5:
            self.move(x=-1,y=0)
        if choice == 6:
            self.move(x=0,y=1)
        if choice == 7:
            self.move(x=0,y=-1)