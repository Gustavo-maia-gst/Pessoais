"""
1 - Gera dois primos p e q
2 - Gera n = p * q
3 - Encontra o totiente de phi(n) = (p - 1) * (q - 1)
4 - Encontra um e que seja coprimo de n
5 - Calcula o inverso de e mod phi(n) = d

ENCRIPTAR: c = m ^ e mod n
DECRIPTAR: m = c ^ d mod n
"""
from math import gcd

def gcdExtended(a, b):
    if a == 0 :
        return b,0,1

    gcd,x1,y1 = gcdExtended(b%a, a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd,x,y

p, q = [int(x) for x in input("Digite p e q: ").split()]

n = p * q

print(f"Temos n = {n}")

totiente = (p-1) * (q-1)

print(f"Temos phi(n) = {totiente}")

for i in range(2, totiente):
    if gcd(totiente, i) == 1:
        break

e = i
_, _, d = gcdExtended(totiente, e)
d = (d % totiente + totiente) % totiente

encriptar = lambda m: pow(int(m), e, n)
decriptar = lambda c: pow(int(c), d, n)

print(f"Chegamos em e = {e} e d = {d}")

while True:
    opcao = input("Você quer encriptar ou decriptar? [E/D/Q para sair] ").upper()
    if opcao == 'E':
        plain = input("Digite o numero para ser encriptado ")
        print(f"Cypher: {encriptar(plain)} ")
    elif opcao == 'D':
        cypher = input("Digite o numero para ser decriptado ")
        print(f"Plain: {decriptar(cypher)} ")
    elif opcao == 'Q':
        print("Até mais ver! ")
        break
    else:
        print("Deixa de ser burro pow!")
