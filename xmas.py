from itertools import cycle
from random import choice, randrange
from time import sleep

import curses
from curses import wrapper

class Snowflake:
    snowflake_characters = ["❄", "❅", "❆", ".", "*"]
    snowflakes = []

    def __init__(self, y, x, character):
        self.y = y
        self.x = x
        self.character = character
        self.snowflakes.append(self)

    def write(self, screen):
        try:
            screen.addch(self.y, self.x, self.character)
        except:
            pass

    @classmethod
    def get_snowflake(cls, x):
        return cls(randrange(0, 5), randrange(0, x), choice(cls.snowflake_characters))

    @staticmethod
    def update(cls, screen, max_y, max_x):
        for idx, snowflake in enumerate(cls.snowflakes):

            if snowflake.y >= max_y - randrange(2, 5):
                # cls.snowflakes.pop(idx)
                snowflake.write(screen)
                continue

            if snowflake.x < 1:
                snowflake.x += choice([0, 1])

            elif snowflake.x >= max_x:
                snowflake.x += choice([-1, 0])

            else:
                snowflake.x += choice([-1, 0, 1])

            snowflake.write(screen)

            snowflake.y += choice([0, 1, 2])


class MessagePoint:
    points = []

    def __init__(self, y, x, character, color = None):
        self.y = y
        self.x = x
        self.character = character
        # self.colored = colored
        self.color = color
        self.points.append(self)

    def write(self, screen, y, x):
        screen.addch(y, x, self.character, self.color)

    @staticmethod
    def update(cls, screen, max_y, max_x, bottom, right):
        for point in cls.points:
            to_add_y = max_y - bottom
            to_add_x = (max_x - right) // 2

            if point.y + to_add_y in range(0, max_y) and point.x + to_add_x in range(0, max_x):
                point.write(screen, point.y + to_add_y, point.x + to_add_x)

    @classmethod
    def get_message(cls, path, base_color, blink_colors):
        with open(path) as file:
            message = file.readlines()

        right = 0
        blinking_colors = cycle(blink_colors)

        for idx, line in enumerate(message):
            for idy, character in enumerate(line):
                if idy > right:
                    right = idy
                if character != " " and character != "\n":
                    if character in ["o", "^", "%", "+", "@", "#", "*", "$"]:
                        MessagePoint(idx, idy, character, next(blinking_colors))

                    else:
                        MessagePoint(idx, idy, character, base_color)

        return len(message), right


def main(screen, message_path):
    y, x = screen.getmaxyx()
    [Snowflake.get_snowflake(x) for _ in range(int((x // 3) * 1.5))]
    count = 0

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    YELLOW = curses.color_pair(2) | curses.A_BLINK
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    BLUE = curses.color_pair(3) | curses.A_BLINK
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    RED = curses.color_pair(4) | curses.A_BLINK
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    CYAN = curses.color_pair(5) | curses.A_BLINK
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    MAGENTA = curses.color_pair(6) | curses.A_BLINK
    bottom, right = MessagePoint.get_message(message_path, GREEN, (YELLOW, BLUE, RED, CYAN, MAGENTA))

    while True:
        screen.clear()

        y, x = screen.getmaxyx()
        count += 1

        if count == 1:
            [Snowflake.get_snowflake(x) for _ in range(int((x // 3) * 1.5))]
        elif count == 3:
            count = 0

        Snowflake.update(Snowflake, screen, y, x)
        MessagePoint.update(MessagePoint, screen, y, x, bottom, right)

        sleep(0.5)
        screen.refresh()


message = "/home/aeternus/Documenten/Programming/Python_programming/xmas/message.txt"

wrapper(main, message)

# print(MessagePoint.get_message(message, None))