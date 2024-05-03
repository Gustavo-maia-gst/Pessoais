"""
1 - Gera dois numeros primos p e q
2 - Calcula n = p * q
2 - Encontra um a aleatório tal que a seja residuo quadratico de p e q simultaneamente 

ENCRIPTAR: Para cada bit mi, ci = bi² * a^mi mod n, sendo que bi é um aleatório mod n e coprimo 
DECRIPTAR: Para cada bit ci, se ci for residuo quadratico, mi = 0, senão mi = 1
"""

from random import randint

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
    
    print("B = ", b)

    cypher = [((b[i] ** 2) * (a ** mensagem[i])) % n for i in range(len(mensagem))]
    return cypher

def decriptar(cypher):
    cypher = [int(c) for c in cypher.split()]
    return [0 if pow(c, (p-1)//2, p) == 1 and pow(c, (q-1)//2, q) == 1 else 1 for c in cypher]

while True:
    opcao = input("Você quer encriptar ou decriptar? [E/D/Q para sair] ").upper()
    if opcao == 'E':
        plain = input("Digite os bits para ser encriptado ")
        print(f"Cypher: {encriptar(plain)} ")
    elif opcao == 'D':
        cypher = input("Digite os números para ser decriptado ")
        print(f"Plain: {decriptar(cypher)} ")
    elif opcao == 'Q':
        print("Até mais ver! ")
        break
    else:
        print("Deixa de ser burro pow!")