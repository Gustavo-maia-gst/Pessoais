from lexical_scanner import LexicalScanner, TokenType
from sys import argv

_solvers = {}

def solver(ch: str):
    def dec(func):
        def new_func(self):
            self.scanner.match(ch)
            func(self)

        if ch in _solvers:
            raise Exception(f'Solver for {ch} already registered ({_solvers[ch]})')
        _solvers[ch] = new_func

        return new_func
    return dec

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
    
    def doif(self):
        self.boolexpr()
        l1 = self.new_label()
        l2 = l1
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l1}')
        self.block()
        nex = self.scanner.lookword()
        if nex == 'else':
            self.scanner.matchword('else')
            l2 = self.new_label()
            self.code.append(f'jmp {l2}')
            self.post_label(l1)
            self.block()

        self.post_label(l2)
    
    def dowhile(self):
        l1 = self.new_label()
        l2 = self.new_label()

        self.post_label(l1)
        self.boolexpr()
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l2}')
        self.block()
        self.code.append(f'jmp {l1}')

        self.post_label(l2)
    
    def resolveidentifier(self, name):
        if self.scanner.look() == '(':
            self.call_func(name)
            return
            
        self.scanner.matchword(':=')
        self.boolexpr()
        self.code.append(f'mov [{name}], al')
        self.bss.add(name)
    
    def block(self):
        self.scanner.matchword('{')
        token = self.scanner.scan()
        while token != '}':
            if not token:
                self.scanner.expected('keyword or identifier', token)

            match token.type:
                case TokenType.IF:
                    self.doif()
                case TokenType.WHILE:
                    self.dowhile()
                case TokenType.IDENTIFIER:
                    self.resolveidentifier(token.value)
                case _:
                    self.scanner.expected('keyword or identifier', token)
            token = self.scanner.scan()
    

    def doprogram(self):
        self.block()

    def factor(self):
        looked = self.scanner.look()
        if looked == '(':
            self.scanner.match('(')
            self.expr()
            self.scanner.match(')')
        elif looked.isdigit():
            self.code.append(f'mov rax, {self.scanner.getnum()}')
        elif looked.isalpha():
            return self.get_name()
        else:
            self.scanner.expected('Expected expression')
    
    def term(self):
        if self.scanner.look() in ['+', '-']:
            self.factor()
            op = self.scanner._getch()
            self.code.append(f'mult rax, {'1' if op == '+' else '-1'}')
        else:
            self.factor()

        op = self.scanner.look()
        while op in ['*', '/', '%']:
            solver = _solvers[op]
            solver(self)
            op = self.scanner.look()
    
    def expr(self):
        self.term()

        op = self.scanner.look()
        while op in ['+', '-']:
            solver = _solvers[op]
            solver(self)
            op = self.scanner.look()

    def relation(self):
        self.expr()

        op = self.scanner.look()
        if self.scanner.look() in ['=', '>', '<', '#']:
            solver = _solvers[op]
            solver(self)
            op = self.scanner.look()
        
    def notfactor(self):
        if self.scanner.look() == '!':
            self.scanner.match('!')
            self.relation()
            self.code.append('cmp rax, 0')
            self.code.append('sete al')
        else:
            self.relation()

    def boolterm(self):
        self.notfactor()

        op = self.scanner.look()
        while op in ['&']:
            solver = _solvers[op]
            solver(self)
            op = self.scanner.look()
   
    def boolexpr(self):
        self.boolterm()

        op = self.scanner.look()
        while op in ['|', '^']:
            solver = _solvers[op]
            solver(self)
            op = self.scanner.look()
    
    @solver('|')
    def _or(self):
        self.code.append(f'push rax')
        self.boolterm()
        self.code.append(f'pop rbx')
        self.code.append(f'or rax, rbx')

    @solver('^')
    def _xor(self):
        self.code.append(f'push rax')
        self.boolterm()
        self.code.append(f'pop rbx')
        self.code.append(f'xor rax, rbx')
    
    @solver('&')
    def _and(self):
        self.code.append(f'push rax')
        self.boolterm()
        self.code.append(f'pop rbx')
        self.code.append(f'and rax, rbx')
    
    @solver('=')
    def _eq(self):
        self.code.append(f'push rax')
        self.expr()
        self.code.append(f'pop rbx')
        self.code.append(f'cmp rax, rbx')
        self.code.append(f'sete al')
        self.code.append(f'movzx rax, al')
    
    @solver('#')
    def _eq(self):
        self.code.append(f'push rax')
        self.expr()
        self.code.append(f'pop rbx')
        self.code.append(f'cmp rax, rbx')
        self.code.append(f'sete al')
        self.code.append(f'xor al, 1')
        self.code.append(f'movzx rax, al')
    
    @solver('>')
    def _eq(self):
        self.code.append(f'push rax')
        self.expr()
        self.code.append(f'pop rbx')
        self.code.append(f'cmp rax, rbx')
        self.code.append(f'setle al')
        self.code.append(f'movzx rax, al')
    
    @solver('<')
    def _eq(self):
        self.code.append(f'push rax')
        self.expr()
        self.code.append(f'pop rbx')
        self.code.append(f'cmp rax, rbx')
        self.code.append(f'setge al')
        self.code.append(f'movzx rax, al')
    
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
    
    @solver('%')
    def mod(self):
        self.code.append(f'push rax')
        self.factor()
        self.code.append(f'mov rbx, rax')
        self.code.append(f'xor rdx, rdx')
        self.code.append(f'pop rax')
        self.code.append(f'div rbx')
        self.code.append(f'mov rax, rdx')
    
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