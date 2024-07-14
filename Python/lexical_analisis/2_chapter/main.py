from cradle import Assembler

s = input()
a = Assembler(s)
a.expr()
print(a.compile())