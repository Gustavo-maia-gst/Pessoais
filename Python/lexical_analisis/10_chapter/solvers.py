from enum import Enum
from typing import *

class PrecedenceOrder(Enum):
    UNARY = 0,
    MULTIPLICATION = 1,
    SUM = 2,
    RELATION = 3,
    LOG_AND = 4,
    LOG_OR = 5,

    def __init__(self, value) -> None:
        super().__init__(self, (value,))
    
    @property
    def value(self):
        return super().value[0]

_solvers: Dict[PrecedenceOrder, Dict[str, Callable]] = {}
LOWEST_ORDER = PrecedenceOrder.LOG_OR
GREATEST_ORDER = PrecedenceOrder.UNARY

def solver(ch: str, order: PrecedenceOrder):
    def dec(func):
        def new_func(self):
            self.scanner.matchword(ch)
            func(self)

        if order not in _solvers:
            _solvers[order] = {}

        if ch in _solvers[order]:
            raise Exception(f'Solver for {ch} already registered ({_solvers[order][ch]})')
        _solvers[order][ch] = new_func

        return new_func
    return dec

@solver('|', PrecedenceOrder.LOG_OR)
def _or(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.LOG_OR)
    self.code.append(f'pop rbx')
    self.code.append(f'or rax, rbx')

@solver('^', PrecedenceOrder.LOG_OR)
def _xor(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.LOG_OR)
    self.code.append(f'pop rbx')
    self.code.append(f'xor rax, rbx')

@solver('&', PrecedenceOrder.LOG_AND)
def _and(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.LOG_AND)
    self.code.append(f'pop rbx')
    self.code.append(f'and rax, rbx')

@solver('=', PrecedenceOrder.RELATION)
def _eq(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'sete al')
    self.code.append(f'movzx rax, al')

@solver('!=', PrecedenceOrder.RELATION)
def _neq(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'sete al')
    self.code.append(f'xor al, 1')
    self.code.append(f'movzx rax, al')

@solver('>', PrecedenceOrder.RELATION)
def _gt(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'setl al')
    self.code.append(f'movzx rax, al')

@solver('>=', PrecedenceOrder.RELATION)
def _gte(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'setle al')
    self.code.append(f'movzx rax, al')

@solver('<', PrecedenceOrder.RELATION)
def _lt(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'setg al')
    self.code.append(f'movzx rax, al')

@solver('<=', PrecedenceOrder.RELATION)
def _lt(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.RELATION)
    self.code.append(f'pop rbx')
    self.code.append(f'cmp rax, rbx')
    self.code.append(f'setge al')
    self.code.append(f'movzx rax, al')

@solver('+', PrecedenceOrder.SUM)
def add(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.SUM)
    self.code.append(f'pop rbx')
    self.code.append(f'add rax, rbx')

@solver('-', PrecedenceOrder.SUM)
def sub(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.SUM)
    self.code.append(f'pop rbx')
    self.code.append(f'sub rax, rbx')
    self.code.append(f'neg rax')

@solver('*', PrecedenceOrder.MULTIPLICATION)
def mult(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.MULTIPLICATION)
    self.code.append(f'pop rbx')
    self.code.append(f'mul rbx')

@solver('/', PrecedenceOrder.MULTIPLICATION)
def div(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.MULTIPLICATION)
    self.code.append(f'mov rbx, rax')
    self.code.append(f'pop rax')
    self.code.append(f'xor rdx, rdx')
    self.code.append(f'div rbx')

@solver('%', PrecedenceOrder.MULTIPLICATION)
def mod(self):
    self.code.append(f'push rax')
    self.expr(PrecedenceOrder.MULTIPLICATION)
    self.code.append(f'mov rbx, rax')
    self.code.append(f'xor rdx, rdx')
    self.code.append(f'pop rax')    
    self.code.append(f'div rbx')
    self.code.append(f'mov rax, rdx')
    
@solver('!', PrecedenceOrder.UNARY)
def _not(self):
    self.expr(PrecedenceOrder.UNARY)
    self.code.append('cmp rax, 0')
    self.code.append('xor rax, rax')
    self.code.append('sete al')

@solver('+', PrecedenceOrder.UNARY)
def _plus(self):
    self.code.append(f'mov rax, +{self.scanner.getnum()}')

@solver('-', PrecedenceOrder.UNARY)
def _plus(self):
    self.code.append(f'mov rax, -{self.scanner.getnum()}')

@solver('(', PrecedenceOrder.UNARY)
def parenteses(self):
    self.expr()
    self.scanner.match(')')