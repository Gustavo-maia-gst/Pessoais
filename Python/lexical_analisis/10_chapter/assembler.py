from lexical_scanner import LexicalScanner, TokenType
from solvers import _solvers, PrecedenceOrder, LOWEST_ORDER, GREATEST_ORDER
from typing import *
from sys import argv


class Assembler:
    def __init__(self, input: str, scanner: LexicalScanner = None):
        self.scanner = LexicalScanner(input) if not scanner else scanner
        self.code = []
        self.bss = {'result'}
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
        self.label_count = 0
    
    def new_label(self):
        self.label_count += 1
        return f'l{self.label_count:03}'

    def post_label(self, l):
        self.code.append(f'\n{l}:')
    
    def call_func(self, name):
        self.scanner.match('(')
        self.scanner.match(')')
        self.code.append(f'call {name}')
    
    def get_name(self):
        name = self.scanner.getname()
        if self.scanner.look() == '(':
            self.call_func(name)
        else:
            self.code.append(f'movzx rax, byte [{name}]')
        return name
    
    def doif(self, retTo):
        self.scanner.match('(')
        self.expr()
        self.scanner.match(')')
        l1 = self.new_label()
        l2 = l1
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l1}')
        self.block(retTo)
        nex = self.scanner.lookword()
        if nex == 'else':
            self.scanner.matchword('else')
            l2 = self.new_label()
            self.code.append(f'jmp {l2}')
            self.post_label(l1)
            self.block(retTo)

        self.post_label(l2)
    
    def dowhile(self):
        l1 = self.new_label()
        l2 = self.new_label()

        self.post_label(l1)
        self.scanner.match('(')
        self.expr()
        self.scanner.match(')')
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l2}')
        self.block(retTo=l2)
        self.code.append(f'jmp {l1}')

        self.post_label(l2)
    
    def dobreak(self, retTo):
        if not retTo:
            self.scanner.error('break statement used outside loop block')
        self.code.append(f'jmp {retTo}')
    
    def resolveidentifier(self, name):
        if self.scanner.look() == '(':
            self.call_func(name)
            return
            
        self.scanner.matchword(':=')
        self.expr()
        self.code.append(f'mov [{name}], al')
        self.bss.add(name)
    
    def block(self, retTo = None):
        self.scanner.matchword('{')
        token = self.scanner.scan()
        while token != '}':
            if not token:
                self.scanner.expected('keyword or identifier', token)

            match token.type:
                case TokenType.IF:
                    self.doif(retTo)
                case TokenType.WHILE:
                    self.dowhile()
                case TokenType.IDENTIFIER:
                    self.resolveidentifier(token.value)
                    self.scanner.match(';')
                case TokenType.BREAK:
                    self.dobreak(retTo)
                    self.scanner.match(';')
                case _:
                    self.scanner.expected('keyword or identifier', token)
            token = self.scanner.scan()
    
    def doprogram(self):
        self.block()

    def expr(self, order = LOWEST_ORDER):
        if order == GREATEST_ORDER:
            looked = self.scanner.look()
            if looked in _solvers[order]:
                solver = _solvers[order][looked]
                solver(self)
            elif looked.isdigit():
                self.code.append(f'mov rax, {self.scanner.getnum()}')
            elif looked.isalpha():
                self.get_name()
            else:
                self.scanner.expected('expression', looked)
            return

        self.expr(PrecedenceOrder((order.value-1,)))

        op = self.scanner.lookword()
        while op in _solvers[order]:
            solver = _solvers[order][op]
            solver(self)
            op = self.scanner.lookword()

    def compile(self):
        code = 'section .bss\n'
        for variable in self.bss:
            code += f'\t{variable} resb 1\n'
            
        code += 'section .text\n'
        code += '\tglobal _start\n'
        code += '_start:\n'
        for line in self.code: code += f'\t{line}\n'
        code += '\tcall _exit\n\n'

        for sub in self.subroutines:
            code += f'{sub}:\n'
            for line in self.subroutines[sub]: code += f'\t{line}\n'
            code += '\n'
        
        return code
    
if __name__ == '__main__':
    if len(argv) == 2:
        file = argv[1]
    else:
        file = 'input.gm'

    a = Assembler(file)
    a.doprogram()
    print(a.compile())
