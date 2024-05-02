from math import gcd
import sys
from random import randint

def rsa():
    """
    1 - Gera dois primos p e q
    2 - Gera n = p * q
    3 - Encontra o totiente de phi(n) = (p - 1) * (q - 1)
    4 - Encontra um e que seja coprimo de n
    5 - Calcula o inverso de e mod phi(n) = d

    ENCRIPTAR: c = m ^ e mod n
    DECRIPTAR: m = c ^ d mod n
    """
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

    return encriptar, decriptar

def gm():
    """
    1 - Gera dois numeros primos p e q
    2 - Calcula n = p * q
    2 - Encontra um a aleatório tal que a seja residuo quadratico de p e q simultaneamente 
    
    ENCRIPTAR: Para cada bit mi, ci = bi² * a^mi mod n, sendo que bi é um aleatório mod n e coprimo 
    DECRIPTAR: Para cada bit ci, se ci for residuo quadratico, mi = 0, senão mi = 1
    """

    p, q = [int(x) for x in input("Digite p e q: ").split()]
    n = p * q

    print(f"Temos n = {n}")
    
    for a in range(2, n):
        if pow(a, (p - 1)//2, p) == p-1:
            if pow(a, (q-1)//2, q) == q-1:
                break

    print(f"Chegamos em a = {a}")

    def encriptar(mensagem):
        mensagem = [int(c) for c in mensagem]
        b = []
        while len(b) < len(mensagem):
            novo_b = randint(1, n)
            if n % novo_b != 0: b.append(novo_b)

        cypher = [((b[i] ** 2) * (a ** mensagem[i])) % n for i in range(len(mensagem))]
        return cypher

    def decriptar(cypher):
        cypher = [int(c) for c in cypher.split()]
        return [1 if pow(c, (p-1)//2, p) == p-1 and pow(c, (q-1)//2, q) == q-1 else 0 for c in cypher]

    return encriptar, decriptar

nome_metodo = sys.argv[1]
encriptar, decriptar = eval(f'{nome_metodo}()')

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
