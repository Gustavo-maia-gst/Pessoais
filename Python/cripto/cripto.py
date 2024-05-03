import sys
import rsa, gm, gamal, ww2 as ww2

nome_metodo = sys.argv[1]

encriptar, decriptar = eval(f'{nome_metodo}.encriptar, {nome_metodo}.decriptar')


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
