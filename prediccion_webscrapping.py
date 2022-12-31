import requests
from bs4 import BeautifulSoup


def extract():
    req = requests.get(
        'https://www.sportytrader.es/cuotas/baloncesto/usa/nba-306/')
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup


def transform(soup):
    games = soup.find_all('div', {
                          'class': 'cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative'})  # Obtenemos todos los partidos
    partidos = []
    for game in games:
        # Obtenemos el onclick de cada partido en concreto siendo onclick el tag que contiene la informacion de cada partido
        partido = game.get('onclick')
        partidos.append(game)

    predicciones = {}
    for p in partidos:
        # Obtenemos el nombre de los equipos
        teams = p.find_all('a', {'class': ''})[0].text
        # Obtenemos las cuotas de cada equipo
        cuota = p.find_all('span', {
                           'class': 'px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 rounded-r-md w-14 md:w-18 flex justify-center items-center text-base'})

        cuotas = []
        for c in cuota:
            # Obtenemos las cuotas de cada equipo de forma limpia
            cuotas.append(c.text)
        predicciones[teams[1:-1]] = cuotas
    return predicciones


def load(predicciones):

    # comparamos las cuotas para ver quien es el favorito
    for i in predicciones:
        if predicciones[i][0] > predicciones[i][1]:
            print(' En el partido ', i, ' el favorito es', i.split(' - ')[1])
            print('------------------------------------')
        else:
            print(' En el partido ', i, ' el favorito es', i.split(' - ')[0])
            print('------------------------------------')


if __name__ == '__main__':
    data = extract()
    predicciones = transform(data)
    load(predicciones)
