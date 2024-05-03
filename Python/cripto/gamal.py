from random import randint

def gcdExtended(a, b):
    if a == 0 :
        return b,0,1

    gcd,x1,y1 = gcdExtended(b%a, a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd,x,y

q = int(input('Digite o valor de q (ordem do grupo), deve ser um número primo: '))

g = int(input("Digite um gerador do grupo: "))
x = int(input(f"X = Digite um numero entre 2 e {q-1}"))
print("X = ", x)

y = pow(g, x, q)

print(f"Temos que a chave pública é: ({y}, {q}, {g}).")

def encriptar(num):
    num = int(num)

    r = x = int(input(f"R = Digite um numero: "))
    print("R = ", r)

    c1 = pow(g, r, q)

    s = pow(y, r, q)

    c2 = (num%q)*s

    return (c1, c2)

def decriptar(cypher):
    c1, c2 = [int(m) for m in cypher.split()]

    t = pow(c1, x, q)
    _, _, t_1 = gcdExtended(q, t)
    m_1 = c2*t_1
    
    return m_1%q
   

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