import datetime
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from scrape.data import GameInformations, GameScore


def scrape_game_informations(url: str):
    if url.__contains__("flashscore.de"):
        return scrape_game_informations_flashscore(url)
    if url.__contains__("kicker.de"):
        return scrape_game_informations_kicker(url)


def scrape_game_scores(url: str):
    if url.__contains__("flashscore.de"):
        return scrape_game_score_flashscore(url)
    if url.__contains__("kicker.de"):
        return scrape_game_score_kicker(url)


def scrape_game_informations_flashscore(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    country = soup.find('span', {'class': "description__country"})

    country_league = country.text
    country_league = country_league.split(':')
    country = country_league[0]
    league = re.sub('- [0-9]+. Spieltag', '', country_league[1], )

    test = soup.find(text=re.compile('var game_utime = [0-9]+;'))

    test = test.split('\n')
    test = re.sub('(.*?)var game_utime = ', '', test[12])[:-1]

    home_team = soup.select('div.tname-home.team-text')
    home_team = home_team[0].text.replace('\n', '')

    away_team = soup.select('div.tname-away.team-text')
    away_team = away_team[0].text.replace('\n', '')

    return GameInformations(country, league, test, home_team, away_team)


def scrape_game_informations_kicker(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    teams = soup.find_all('div', {'class': 'kick__v100-gameCell__team__name'})

    league = soup.find('div', {'class': 'kick__v100-scoreboardInfo'}).text
    league = re.sub('[0-9]+/[0-9]+, [0-9]+. Spieltag', '', league)[2:].strip()

    table = soup.findAll('div', attrs={"class": "kick__gameinfo-block"})
    date_time = re.sub('(.*?)Anstoß', '', table[0].text)[:-1]
    date_time = re.sub(',', '', date_time)[3:].strip()

    date_time = date_time.split(' ')
    date = date_time[0].split('.')
    time = date_time[1].split(':')
    date_time = datetime(int(date[2]), int(date[1]),
                         int(date[0]), int(time[0]), int(time[1]))

    return GameInformations("", league, datetime.timestamp(date_time), teams[0].text, teams[1].text)

    return


def scrape_game_score_flashscore(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    response = soup.find_all('span', {'class': 'scoreboard'})

    return GameScore(response[0].text, response[1].text)


def scrape_game_score_kicker(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    response = soup.find_all('div', {'class': 'kick__v100-scoreBoard__scoreHolder__score'})

    return GameScore(response[0].text, response[1].text)


'''
if __name__ == "__main__":
    scrape_game_informations("https://www.flashscore.de/spiel/hzDoWwk8/#spiel-zusammenfassung")
    test = scrape_game_scores("https://www.flashscore.de/spiel/xUXeO6sA/#spiel-zusammenfassung")
    test2 = scrape_game_informations("https://www.kicker.de/ama-41552876/spielinfo/tsv-schoenau/fv-leutershausen-ii-64008")
    test3 = scrape_game_scores("https://www.kicker.de/ama-22975449/spielinfo/sc-kaefertal-ii-39507/tsv-schoenau")
'''
