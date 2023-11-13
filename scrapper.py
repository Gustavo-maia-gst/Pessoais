from urllib.request import urlopen
from bs4 import BeautifulSoup

class Time:
    def __init__(self, nome, gols_f, gols_s, sg, jogos):
        self.nome = nome.replace('é', 'e').replace('á', 'a')
        self.gols_f = gols_f
        self.gols_s = gols_s
        self.sg = sg
        self.jogos = jogos

    def __repr__(self):
        return f'<Time(nome={self.nome}, gols_f={self.gols_f}, gols_s={self.gols_s}, sg={self.sg}, jogos={self.jogos})>'
    
class Conflito:
    def __init__(self, casa, fora, horario):
        self.casa = casa
        self.fora = fora
        self.horario = horario

    def __repr__(self):
        return f'<Conflito(casa={self.casa.nome}, fora={self.casa.nome}, horario={self.horario})>'
    
    def __iter__(self):
        return iter((self.casa, self.fora))

def time_por_nome(times, nome):
    for time in times:
        if nome in time.nome:
            return time
    return None

def analisa_jogo(partida, perc):
    casa = partida.casa
    fora = partida.fora
    forte = 0
    if casa.gols_f / casa.jogos >= perc and fora.gols_s / fora.jogos >= perc:
        forte += 1
    if fora.gols_f / fora.jogos >= perc and casa.gols_s / casa.jogos >= perc:
        forte += 2
    return forte

LIGAS = ['esp.1', 'eng.1', 'fra.1', 'ger.1', 'ita.1', 'bra.1']
NOME_LIGAS = {
    'esp.1': 'La Liga',
    'eng.1': 'Premier League',
    'fra.1': 'League 1',
    'ita.1': 'Italiano',
    'bra.1': 'Brasileiro'
}

times = []
conflitos = []

for liga in LIGAS:
    html = urlopen(f'https://www.espn.com.br/futebol/classificacao/_/liga/{liga}')
    html = BeautifulSoup(html, 'html.parser')
    base = html.find('div', {'class': 'ResponsiveTable ResponsiveTable--fixed-left'}).find('div', {'class': 'flex'})
    t_times = base.table
    valores = t_times.next_sibling
    cabecalhos = valores.find('thead')
    valores = valores.find('table').find('tbody')
    t_times = t_times.find('tbody')

    equipes = []
    stats = {}

    i = 0
    for cel in cabecalhos.find_all('th'):
        stats[cel.text] = i
        i += 1

    for time in t_times.find_all('tr'):
        equipes.append(time.find('span', {'class': 'hide-mobile'}).text)


    rows = valores.find_all('tr')
    for l in range(len(equipes)):
        cols = [int(cel.text) for cel in rows[l].find_all('td')]
        time = Time(equipes[l], cols[stats['GP']], cols[stats['GC']], cols[stats['SG']], cols[stats['J']])
        times.append(time)

    html = urlopen(f'https://www.espn.com.br/futebol/calendario/_/liga/{liga}')
    html = BeautifulSoup(html, 'html.parser')

    for table in html.find_all('div', {'class': 'ResponsiveTable'}):
        if 'resultado' in table.thead.text.lower():
            continue
        for row in table.tbody.find_all('tr'):
            casa, fora = [e.text for e in row.find_all('span', {'class': 'Table__Team'})]
            hora = row.find('td', {'class': 'date__col'}).text
            casa = time_por_nome(times, casa)
            fora = time_por_nome(times, fora)
            if not casa or not fora:
                continue
            conflitos.append(Conflito(casa, fora, hora))

if __name__ == '__main__':
    porcentagem = float(input("Insira a taxa mínima de gols: "))

    for conflito in conflitos:
        casa = conflito.casa
        fora = conflito.fora
        forte = analisa_jogo(conflito, porcentagem)
        if not forte:
            continue
        adjetivo = 'boa'
        complemento = ''

        if forte < 3:
            if forte == 1:
                maior = casa
                menor = fora
            else:
                maior = fora
                menor = casa

            complemento = f'{maior.nome} está com uma média de {maior.gols_f / maior.jogos:.2f} gols por jogo e {menor.nome} sofre {menor.gols_s / menor.jogos:.2f} gols por jogo.'
        else:
            adjetivo = 'ótima'
            complemento = f'Ambas as equipes possuem médias de gols feitos e sofridos por jogo acima de {porcentagem:.2f}'

        print(f'{conflito.horario:<5}{casa.nome:^20} X {fora.nome:^20}\nPartida com {adjetivo} chance de gol. {complemento}\n')