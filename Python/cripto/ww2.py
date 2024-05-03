r = "ADFGVX" 
print("Digite a tabela:")
print(*list(r))

tab = {}
tab2 = {}
for i in range(len(r)):
    row = input().upper().split()
    for l in range(len(row)):
        tab[row[l]] = f"{r[i]}{r[l]}"
        tab2[f"{r[i]}{r[l]}"] = row[l]

word = input("Digite a palavra de transposição: ").upper()
s_word = sorted(word)

mapp = dict([(i, word.index(s_word[i])) for i in range(len(s_word))])

def encriptar(text):

    cypher = {l: [] for l in word}
    
    l = 0
    c = 0
    while True:
        drupa = tab[text[c]]
        cypher[word[l%len(word)]].append(drupa[0])
        l += 1
        cypher[word[(l)%len(word)]].append(drupa[1])
        l += 1

        c += 1
        if c > len(text)-1: break
    
    for c in cypher.keys():
        
        print(*cypher[c])
    
    sorted = list(cypher.keys())
    sorted.sort()

    cypher2 = ""
    for k in sorted:
        cypher2 += "".join(cypher[k])
        cypher2 += ' '

    return cypher2

def decriptar(cypher):
    cypher = cypher.split()

    tab = [None for _ in range(len(cypher))]
    for i in range(len(cypher)):
        tab[mapp[i]] = cypher[i]

    tabela = []
    for i in range(len(tab[0])):
        linha = []
        for j in range(len(tab)):
            try:
                linha.append(tab[j][i])
            except:
                pass
        tabela.append(linha)
    
    chars = []
    t_linha = len(tabela[0])
    for i in range(0, len(tabela) * len(tabela[0]), 2):
        try:
            chars.append(tabela[i // t_linha][i % t_linha] + tabela[(i+1) // t_linha][(i+1) % t_linha])
        except:
            break
    
    return "".join(tab2[c] for c in chars)
    
while True:
    opcao = input("Você quer encriptar ou decriptar? [E/D/Q para sair] ").upper()
    if opcao == 'E':
        plain = input("Digite o texto para ser encriptado: ").upper()
        print(f"Cypher: {encriptar(plain)} ")
    elif opcao == 'D':
        cypher = input("Digite o texto para ser decriptado: ").upper()
        print(f"Plain: {decriptar(cypher)} ")
    elif opcao == 'Q':
        print("Até mais ver! ")
        break
    else:
        print("Deixa de ser burro pow!")