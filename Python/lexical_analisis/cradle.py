from collections import deque
from sys import exit
from typing import *

class Cradle:
    solvers = {}
    def __init__(self, input: str):
        self._buffer = deque(input.replace(' ', ''))
        pass

    def _getch(self) -> str:
        return self._buffer.popleft()

    def look(self) -> str:
        if not self._buffer: return
        return self._buffer[0]
    
    def match(self, ch, validator: Callable = lambda ch, c: c == ch) -> bool:
        return validator(self._getch(), ch)
    
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

def solver(ch: str):
    def dec(func):
        def new_func(self):
            self.cradle.match(ch)
            func(self)

        if ch in Cradle.solvers:
            raise Exception(f'Solver for {ch} already registered ({Cradle.solvers[ch]})')
        Cradle.solvers[ch] = new_func

        return new_func
    return dec

class Assembler:
    def __init__(self, input: str):
        self.cradle = Cradle(input)
        self.code = []
        self.subroutines = {
            '_print': [
                "add rax, 0x30",
                "mov byte [result], al",
                "mov rax, 1",
                "mov rdi, 1",
                "mov rsi, result",
                "mov rdx, 1",
                "syscall",
                "mov byte [result], 10",
                "mov rax, 1",
                "mov rdi, 1",
                "mov rsi, result",
                "mov rdx, 1",
                "syscall",
                "ret"
            ],
            '_exit': [
                "mov rax, 60",
                "mov rdi, 0",
                "syscall"
            ]
        }
    
    def get_name(self):
        name = self.cradle.getname()
        if self.cradle.look() == '(':
            self.cradle.match('(')
            self.cradle.match(')')
            self.code.append(f'call {name}')
        else:
            self.code.append(f'mov al, byte [{name}]')
    
    def factor(self):
        looked = self.cradle.look()
        if looked == '(':
            self.cradle.match('(')
            self.expr()
            self.cradle.match(')')
        elif looked.isdigit():
            self.code.append(f'mov rax, {self.cradle.getnum()}')
        elif looked.isalpha():
            self.get_name()
    
    def term(self):
        self.factor()
        op = self.cradle.look()
        while op in ['*', '/']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
    
    def expr(self):
        if self.cradle.look() in ['+', '-']:
            self.code.append('xor rax, rax')
        else:
            self.term()

        op = self.cradle.look()
        while op in ['+', '-']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
    
    @solver('+')
    def add(self):
        self.code.append(f'push rax')
        self.term()
        self.code.append(f'pop rbx')
        self.code.append(f'add rax, rbx')
    
    @solver('-')
    def sub(self):
        self.code.append(f'push rax')
        self.term()
        self.code.append(f'pop rbx')
        self.code.append(f'sub rax, rbx')
        self.code.append(f'neg rax')
    
    @solver('*')
    def mult(self):
        self.code.append(f'push rax')
        self.factor()
        self.code.append(f'pop rbx')
        self.code.append(f'mul rbx')
    
    @solver('/')
    def div(self):
        self.code.append(f'push rax')
        self.factor()
        self.code.append(f'mov rbx, rax')
        self.code.append(f'pop rax')
        self.code.append(f'div rbx')
    
    def compile(self):
        code = 'section .bss\n'
        code += '\tresult resb 1\n'
        code += 'section .text\n'
        code += '\tglobal _start\n'
        code += '_start:\n'
        for line in self.code: code += f'\t{line}\n'
        code += '\tcall _print\n'
        code += '\tcall _exit\n\n'

        for sub in self.subroutines:
            code += f'{sub}:\n'
            for line in self.subroutines[sub]: code += f'\t{line}\n'
            code += '\n'
        
        return code