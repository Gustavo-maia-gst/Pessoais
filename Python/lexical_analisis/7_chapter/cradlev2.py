from collections import deque
from sys import exit
from typing import *

class CradleV2:
    solvers = {}
    def __init__(self, input: str):
        self._buffer = deque(input)
        pass

    def expected(self, msg, got = None) -> None:
        print(f"\033[31mExpected: {msg}{f', got: {got}' if got else ''}\033[0m")
        exit(1)

    def look(self) -> str:
        if not self._buffer: return
        return self._buffer[0]
    
    def getch(self) -> str:
        if not self._buffer: return
        ch = self._buffer.popleft()
        return ch
    
    def getname(self) -> str:
        if not self.look().isalpha():
            self.expected('identifier')
        name = self.getch()
        while self.look() and self.look().isalnum():
            name += self.getch()
        return name
    
    def genum(self) -> str:
        if not self.look().isdigit(): self.expected('number')
        num = self.getch()
        while self.look() and self.look().isdigit():
            num += self.getch()
        return num
    
    def scan(self) -> str:
        nch = self.look()
        if nch is None: self.expected('semicolumn')

        scan = ''
        if nch.isalpha(): scan = self.getname()
        elif nch.isdigit(): scan = self.genum()
        else: scan = self.getch()

        while self.look() in ['\t', '\r', '\n', ' ']: self.getch()
        return scan

if __name__ == '__main__':
    cradle = CradleV2(input())
    tokens = []
    while cradle.look() != ';':
        tokens.append(cradle.scan())
    print(tokens)