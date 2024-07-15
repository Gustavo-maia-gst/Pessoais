from cradle import Cradle


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
    def __init__(self, input: str, cradle: Cradle = None):
        self.cradle = Cradle(input) if not cradle else cradle
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
        self.label_count = 0
    
    def new_label(self):
        self.label_count += 1
        return f'l{self.label_count:03}'

    def post_label(self, l):
        self.code.append(f'\n{l}:')
    
    def get_name(self):
        name = self.cradle.getch()
        if self.cradle.look() == '(':
            self.cradle.match('(')
            self.cradle.match(')')
            self.code.append(f'call {name}')
        else:
            self.code.append(f'mov al, byte [{name}]')
        return name
    
    def doif(self):
        while self.cradle.look() == 'i':
            self.cradle.match('i')

            self.boolexpr()
            l1 = self.new_label()
            l2 = l1
            self.code.append(f'cmp rax, 0')
            self.code.append(f'je {l1}')
            self.block()
            if self.cradle.look() == 'e':
                self.cradle.match('e')
                l2 = self.new_label()
                self.code.append(f'jmp {l2}')
                self.post_label(l1)
                self.block()

            self.cradle.match('f')
            self.post_label(l2)
    
    def dowhile(self):
        self.cradle.match('w')

        l1 = self.new_label()
        l2 = self.new_label()

        self.post_label(l1)
        self.boolexpr()
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l2}')
        self.block()
        self.code.append(f'jmp {l1}')

        self.post_label(l2)
        self.cradle.match('f')
    
    def block(self):
        while self.cradle.look() and self.cradle.look() not in ['f', 'e']:
            if self.cradle.look() == 'i': self.doif()
            elif self.cradle.look() == 'w': self.dowhile()
            else: print(self.cradle._getch())
    
    def doprogram(self):
        self.block()

    def factor(self):
        looked = self.cradle.look()
        if looked == '(':
            self.cradle.match('(')
            self.expr()
            self.cradle.match(')')
        elif looked.isdigit():
            self.code.append(f'mov rax, {self.cradle.getnum()}')
        elif looked.isalpha():
            return self.get_name()
        else:
            self.cradle.expected('Expected expression')
    
    def term(self):
        if self.cradle.look() in ['+', '-']:
            self.factor()
            op = self.cradle._getch()
            self.code.append(f'mult rax, {'1' if op == '+' else '-1'}')
        else:
            self.factor()

        op = self.cradle.look()
        while op in ['*', '/']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
    
    def expr(self):
        self.term()

        op = self.cradle.look()
        while op in ['+', '-']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()

    def relation(self):
        self.expr()

        op = self.cradle.look()
        if self.cradle.look() in ['=', '>', '<']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
        
    def notfactor(self):
        if self.cradle.look() == '!':
            self.cradle.match('!')
            self.relation()
            self.code.append('cmp rax, 0')
            self.code.append('sete al')
        else:
            self.relation()

    def boolterm(self):
        self.notfactor()

        op = self.cradle.look()
        while op in ['&']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
   
    def boolexpr(self):
        self.boolterm()

        op = self.cradle.look()
        while op in ['|', '^']:
            solver = self.cradle.solvers[op]
            solver(self)
            op = self.cradle.look()
    
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
        self.code.append(f'setg al')
        self.code.append(f'movzx rax, al')
    
    @solver('<')
    def _eq(self):
        self.code.append(f'push rax')
        self.expr()
        self.code.append(f'pop rbx')
        self.code.append(f'cmp rax, rbx')
        self.code.append(f'setl al')
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