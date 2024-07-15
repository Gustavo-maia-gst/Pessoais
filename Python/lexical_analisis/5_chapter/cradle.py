from collections import deque
from sys import exit
from typing import *

class Cradle:
    solvers = {}
    def __init__(self, input: str):
        self._buffer = deque(input.replace(' ', ''))
        pass

    def _getch(self) -> str:
        if not self._buffer: return
        return self._buffer.popleft()

    def look(self) -> str:
        if not self._buffer: return
        return self._buffer[0]
    
    def match(self, ch):
        c = self._getch()
        if c == ch: return c
        self.expected(ch, c)
    
    def error(self, msg) -> None:
        print(f"\033[31mError: {msg}\033[0m")
        exit(1)

    def expected(self, msg, got = None) -> None:
        print(f"\033[31mExpected: {msg}{f', got: {got}' if got else ''}\033[0m")
        exit(1)
    
    def _getValidated(self, validator: Callable, expected: str) -> str:
        ch = self._getch()
        if not validator(ch):
            self.expected(expected, ch)
        return ch
    
    def getch(self) -> str:
        return self._getValidated(lambda ch: ch.isalpha(), "char")
    
    def getnum(self) -> int:
        number = 0
        while self.look() and self.look().isdigit():
            number = 10 * number + int(self._getch())
        return number
    
    def getname(self) -> str:
        name = self.getch()
        while self.look() and self.look().isalnum():
            name += self._getch()
        return name
    
    def lookname(self) -> str:
        name = ''
        for i in range(len(self._buffer)):
            if not self._buffer[i].isalpha(): break
            name += self._buffer[i]
        return name

    def matchname(self, name) -> str:
        n = self.getname()
        if n == name: return n
        self.expected(name, n)
    
    def getbool(self) -> str:
        if not self._buffer: return
        return self._getValidated(lambda ch: ch.upper() in ['T', 'F'], 'boolean')