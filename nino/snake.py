from collections import deque
import nino
from time import sleep
import random


class Snake:
    moving_up = (-1, 0)
    moving_down = (1, 0)
    moving_left = (0, -2)
    moving_right = (0, 2)

    def __init__(self, line, column, size=2):
        self._head = line, column
        self.body = deque([self._head])
        self.moving = Snake.moving_up
        
        for n in range(1, size + 1):
            self.body.append((line + n, column))

    @property
    def head(self):
        return self._head

    def move(self):
        y, x = self.body[0]
        self.body.pop()
        delta_y, delta_x = self.moving
        self.body.appendleft((y + delta_y, x + delta_x))
        self._head = self.body[0]

    def eat(self):
        y, x = self.body[0]
        delta_y, delta_x = self.moving
        self.body.appendleft((y + delta_y, x + delta_x))
        self._head = self.body[0]


class Charberry:
    def __init__(self, y, x, char):
        self.y = y
        self.x = x
        self.char = char
    
    def __hash__(self):
        return hash(self.y) ^ hash(self.x)

    def __getitem__(self, index):
        return [self.y, self.x, self.char][index]

    def __iter__(self):
        return iter([self.y, self.x, self.char])

    def __str__(self):
        return self.char

    def __eq__(self, other):
        y_other, x_other = other
        if self.x == x_other and self.y == y_other:
            return True
        return False


def main(scr):
    snake = Snake(22, 40, size=4)
    y_size = (1, scr.lines - 1)
    x_size = (3, 90)

    moves_map = {
            scr.keyboard.ecodes.KEY_J: snake.moving_down,
            scr.keyboard.ecodes.KEY_K: snake.moving_up,
            scr.keyboard.ecodes.KEY_L: snake.moving_right,
            scr.keyboard.ecodes.KEY_H: snake.moving_left
    }
    charberry_list = [chr(n) for n in range(65, 91)]

    @scr.keyboard.listener
    def controller(event):
        if event.code in moves_map.keys():
            y, x = moves_map[event.code]
            y_snake, x_snake = snake.moving
            equal = all((x == x_snake * -1, y == y_snake * -1))
            if not equal:
                snake.moving = y, x

    def write_square(lines=scr.lines, columns=90):
        for col in range(2, columns + 1):
            scr.addstr(0, col, '_')
            scr.addstr(lines - 1, col, '_')
        for lin in range(1, lines):
            scr.addstr(lin, 2, '|')
            scr.addstr(lin, columns, '|')

    def spawn(char, lines=scr.lines, columns=90):
        x = random.randint(4, (columns - 6) // 2) * 2
        y = random.randint(2, lines - 3)
        if (y, x) in snake.body:
            return spawn(char)

        return Charberry(y, x, char)

    char = random.choice(charberry_list)
    berry = spawn(char)
    score = 0

    while True:
        if not berry:
            char = random.choice(charberry_list)
            berry = spawn(char)

        for y, x in snake.body:
            try:
                scr.addstr(int(y), int(x), '*')
            except nino.ScreenOverflowError:
                return

        scr.addstr(berry[0], berry[1] - 1, '<')
        scr.addstr(*berry)
        scr.addstr(berry[0], berry[1] + 1, '>')
        scr.addstr(snake.head[0], int(snake.head[1]), '@')
        write_square()

        if snake.head[0] < y_size[0] or snake.head[0] > y_size[1]:
            return
        elif snake.head[1] < x_size[0] or snake.head[1] > x_size[1]:
            return
        
        score_size = scr.columns - x_size[1] - 2
        score_str = f'SCORE: {score}'
        scr.addstr(11, x_size[1] + 2, f"{score_str:^25}")

        snake_str = f'SNAKE SIZE: {score + 4}'
        scr.addstr(8, x_size[1] + 2, f"{snake_str:^25}")

        if berry == snake.head:
            snake.eat()
            score += 1
            berry = None
        else:
            snake.move()

        scr.refresh()
        scr.clear()
        sleep(0.12)

nino.wrapper(main)
