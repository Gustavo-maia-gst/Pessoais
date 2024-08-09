from lexical_scanner import LexicalScanner, TokenType
from solvers import _solvers, PrecedenceOrder, LOWEST_ORDER, GREATEST_ORDER
from typing import *
from sys import argv
from tree import *

class FuncDefinition:
    def __init__(self, label: str, params: List[str], code = []) -> None:
        self.label = label
        self.params = {params[i]: 8 * (len(params) - i + 1) for i in range(len(params))}
        self.code = code
        self.locals = {}

class ASTParser:
    def __init__(self, input: str, scanner: LexicalScanner = None):
        self.scanner = LexicalScanner(input) if not scanner else scanner
    
    def new_label(self):
        self.label_count += 1
        return f'l{self.label_count:03}'

    def post_label(self, l):
        self.code.append(f'\n{l}:')
    
    def call_func(self, context, name):
        if name not in self.subroutines:
            self.scanner.error(f'call to not defined function {name}')
        
        funcdef = self.subroutines[name]
            
        self.scanner.match('(')

        readen = 0

        if self.scanner.look() != ')':
            self.expr(context)
            self.code.append('push rax')
            readen += 1
            if (self.scanner.look() != ')'):
                while self.scanner.look() != ')':
                    self.scanner.match(',')
                    self.expr(context)
                    self.code.append('push rax')
                    readen += 1
        
        if readen != len(funcdef.params):
            self.scanner.error(f'invalid parameter list size for function {name}, expected {len(funcdef.params)}, got {readen}')

        self.scanner.match(')')
        self.code.append(f'call {funcdef.label}')
        self.code.append(f'add rsp, {8 * len(funcdef.params)}')
    
    def get_name(self, context):
        name = self.scanner.getname()
        funcdef = self.subroutines[context]
        if self.scanner.look() == '(':
            self.call_func(context, name)
        else:
            if name in funcdef.params:
                self.code.append(f'mov rax, [{self.get_real_param(context, name)}]')
            elif name in funcdef.locals:
                self.code.append(f'mov rax, [rbp - {funcdef.locals[name]}]')
            elif name in self.bss:
                self.code.append(f'mov rax, [{name}]')
            else:
                self.scanner.error(f'unresolved name: {name}')

        return name
    
    def doif(self, context, retTo):
        self.scanner.match('(')
        self.expr(context)
        self.scanner.match(')')
        l1 = self.new_label()
        l2 = l1
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l1}')
        self.block(context, retTo)
        nex = self.scanner.lookword()
        if nex == 'else':
            self.scanner.matchword('else')
            l2 = self.new_label()
            self.code.append(f'jmp {l2}')
            self.post_label(l1)
            self.block(context, retTo)

        self.post_label(l2)
    
    def dowhile(self, context):
        l1 = self.new_label()
        l2 = self.new_label()

        self.post_label(l1)
        self.scanner.match('(')
        self.expr(context)
        self.scanner.match(')')
        self.code.append(f'cmp rax, 0')
        self.code.append(f'je {l2}')
        self.block(context, retTo=l2)
        self.code.append(f'jmp {l1}')

        self.post_label(l2)
    
    def dobreak(self, retTo):
        if not retTo:
            self.scanner.error('break statement used outside loop block')
        self.code.append(f'jmp {retTo}')
    
    def resolveidentifier(self, context, name):
        if self.scanner.look() == '(':
            self.call_func(context, name)
            return
            
        self.scanner.matchword(':=')
        self.expr(context)

        if name in self.scanner.keywords:
            self.scanner.error(f'Cannot assign a variable with the keyword {name}')

        funcdef = self.subroutines[context]
        if name in funcdef.params:
            self.code.append(f'mov [{self.get_real_param(context, name)}], rax')
        elif name in funcdef.locals:
            self.code.append(f'mov [rbp - {funcdef.locals[name]}], rax')
        elif name in self.bss:
            self.code.append(f'mov [{name}], rax')
        else:
            funcdef.locals[name] = 8 * (len(funcdef.locals) + 1)
            self.code.append(f'sub rsp, 8')
            self.code.append(f'mov [rbp - {funcdef.locals[name]}], rax')
    
    def doreturn(self, context):
        if self.scanner.look() != ';':
            self.expr(context)
        self.endfunc(context)
    
    def block(self, context = 'main', retTo = None):
        self.scanner.matchword('{')
        token = self.scanner.scan()
        while token != '}':
            if not token:
                self.scanner.expected('keyword or identifier', token)

            match token.type:
                case TokenType.IF:
                    self.doif(context, retTo)
                case TokenType.WHILE:
                    self.dowhile(context)
                case TokenType.IDENTIFIER:
                    self.resolveidentifier(context, token.value)
                    self.scanner.match(';')
                case TokenType.BREAK:
                    self.dobreak(retTo)
                    self.scanner.match(';')
                case TokenType.RETURN:
                    self.doreturn(context)
                    self.scanner.match(';')
                    if self.scanner.look() != '}': self.scanner.error('Expected end of block after return statement')
                case _:
                    self.scanner.expected('keyword or identifier', token)
            token = self.scanner.scan()
    
    def get_real_param(self, context, name):
        if not name in self.subroutines[context].params:
            self.scanner.error(f"local variable doesn't exists")
        
        offset = self.subroutines[context].params[name]
        return f'rbp + {offset}'

    def read_formal_params(self, funcname):
        params = []
        self.scanner.match('(')

        if self.scanner.look() != ')':
            name = self.scanner.getname()
            params.append(name)
            if (self.scanner.look() != ')'):
                while self.scanner.look() != ')':
                    self.scanner.match(',')
                    params.append(self.scanner.getname())

        self.scanner.match(')')

        self.subroutines[funcname] = FuncDefinition(self.new_label() if funcname != 'main' else '_start', params)

    def doFunc(self, ident):
        if ident.value in self.scanner.keywords:
            self.scanner.error(f'cannot define a function with the keyword {funcname}')
        if ident.value in self.subroutines:
            self.scanner.error(f'function {funcname} has already declared')

        params = self.doDefineParams(funcname)
        block = self.doBlock(funcname)

        return FunctionNode(ident, params, block)
    
    def doProgram(self):
        main = None
        funcDefinitions = []

        token = self.scanner.scan()
        while token and token.type == TokenType.IDENTIFIER:
            funcDef = self.doFunc(token)
            funcDefinitions.append(funcDef)
            if funcDef.rawToken === 'main': main = funcDef

            token = self.scanner.scan()

        if not main:
            self.scanner.error('main function not defined')

        return ProgramNode(main.rawToken, funcDefinitions)

    def expr(self, context, order = LOWEST_ORDER):
        if order == GREATEST_ORDER:
            looked = self.scanner.look()
            if looked in _solvers[order]:
                solver = _solvers[order][looked]
                solver(self, context)
            elif looked.isdigit():
                self.code.append(f'mov rax, {self.scanner.getnum()}')
            elif looked.isalpha():
                self.get_name(context)
            else:
                self.scanner.expected('expression', looked)
            return

        self.expr(context, PrecedenceOrder((order.value-1,)))

        op = self.scanner.lookword()
        while op in _solvers[order]:
            solver = _solvers[order][op]
            solver(self, context)
            op = self.scanner.lookword()

if __name__ == '__main__':
    if len(argv) == 2:
        file = argv[1]
    else:
        file = 'input.gm'

    a = Assembler(file)
    a.doprogram()
    print(a.compile())
