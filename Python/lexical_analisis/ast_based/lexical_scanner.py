from collections import deque
from enum import Enum
from sys import exit
from typing import *

class TokenType(Enum):
    IF = 0,
    WHILE = 1,
    FOR = 2,
    IDENTIFIER = 3,
    NUMBER = 4,
    OPERATOR = 5,
    ANY = 6,
    BREAK = 7,
    RETURN = 8,
    
class Token:
    def __init__(self, word: str, type: TokenType):
        self.value: str = word
        self.type: TokenType = type
    
    def __repr__(self) -> str:
        return f'Token({self.value}, {self.type})'
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, value) -> bool:
        return self.value == value
    
    def __hash__(self) -> int:
        return hash(self.value)

class LexicalScanner:
    keywords = {
        'if': Token('if', TokenType.IF),
        'for': Token('for', TokenType.FOR),
        'while': Token('while', TokenType.WHILE),
        'break': Token('break', TokenType.BREAK),
        'return': Token('return', TokenType.RETURN)
    }

    operators = {
        '=': Token('=', TokenType.OPERATOR),
        '!=': Token('!=', TokenType.OPERATOR),
        '>': Token('>', TokenType.OPERATOR),
        '>=': Token('>=', TokenType.OPERATOR),
        '<=': Token('<=', TokenType.OPERATOR),
        '&': Token('&', TokenType.OPERATOR),
        '|': Token('|', TokenType.OPERATOR),
        '!': Token('!', TokenType.OPERATOR),
        '+': Token('+', TokenType.OPERATOR),
        '-': Token('-', TokenType.OPERATOR),
        '*': Token('*', TokenType.OPERATOR),
        '/': Token('/', TokenType.OPERATOR),
        ':=': Token(':=', TokenType.OPERATOR),
    }

    blanks = ['\t', '\n', ' ']

    def __init__(self, input: str):
        with open(input, 'r') as file:
            self._buffer = deque(' '.join(file.readlines()))

    def expected(self, msg, got = None) -> None:
        print(f"\033[31mExpected: {msg}{f', got: {got}' if got else ''}\033[0m")
        exit(1)
    
    def error(self, msg) -> None:
        print(f"\033[31mSintax Error: {msg}\033[0m")
        exit(1)

    def look(self) -> str:
        if not self._buffer: return
        return self._buffer[0]
    
    def match(self, ch: str) -> None:
        if not self._buffer: return
        char = self._buffer.popleft()
        self.clear_white()
        if ch != char:
            self.expected(ch, char)
    
    def matchword(self, n: str):
        word = self.getword()
        self.clear_white()
        if n != word:
            self.expected(n, word)
        return word
    
    def getch(self) -> str:
        if not self._buffer: return
        ch = self._buffer.popleft()
        return ch
    
    def getword(self) -> str:
        word = ''
        while self.look() and self.look() not in self.blanks and not self.look().isalnum():
            word += self.getch()
        self.clear_white()
        return word
    
    def lookword(self) -> str:
        word = ''
        for i in range(len(self._buffer)):
            if self._buffer[i] in self.blanks:
                break
            word += self._buffer[i]

        return word
    
    def getname(self) -> Token:
        if not (self.look().isalpha() or self.look() == '_'):
            self.expected('identifier')

        name = self.getch()
        while self.look() and self.look().isalnum():
            name += self.getch()

        self.clear_white()
        if name in self.keywords: 
            return self.keywords[name]
        return Token(name, TokenType.IDENTIFIER)
    
    def getnum(self) -> Token:
        if not self.look().isdigit(): self.expected('number')
        self.clear_white()
        num = self.getch()
        while self.look() and self.look().isdigit():
            num += self.getch()
        self.clear_white()
        return Token(num, TokenType.NUMBER)
    
    def scan(self) -> Token:
        nch = self.look()
        if nch is None: return

        if nch.isalpha() or nch == '_':
            scan = self.getname()
        elif nch.isdigit():
            scan = self.getnum()
        else:
            scan = Token(self.getword(), TokenType.ANY)
            if scan.value in self.operators:
                return self.operators[scan.value]
        
        self.clear_white()
        return scan
    
    def scantoken(self, tokenType):
        token = self.scan()
        if token.type != tokenType:
            self.expected(tokenType, token.type)
        return token
    
    def clear_white(self):
        while self.look() in self.blanks: self.getch()

