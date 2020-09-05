import requests
import re
from bs4 import BeautifulSoup

from scrape.data import GameInformations, GameScore


def scrape_game_informations(url: str):
    if url.__contains__("flashscore.de"):
        return scrape_game_informations_flashscore(url)

def scrape_game_scores(url: str):
    if url.__contains__("flashscore.de"):
        return scrape_game_score_flashscore(url)


def scrape_game_informations_flashscore(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    country = soup.find('span', {'class':"description__country"})

    countryLeague = country.text
    countryLeague = countryLeague.split(':')
    country = countryLeague[0]
    league = re.sub('- [0-9]+. Spieltag', '', countryLeague[1],)

    test = soup.find(text=re.compile('var game_utime = [0-9]+;'))

    test = test.split('\n')
    test = re.sub('(.*?)var game_utime = ', '', test[12])[:-1]


    homeTeam = soup.select('div.tname-home.team-text')
    homeTeam = homeTeam[0].text.replace('\n', '')

    awayTeam = soup.select('div.tname-away.team-text')
    awayTeam = awayTeam[0].text.replace('\n', '')

    return GameInformations(country, league, test, homeTeam, awayTeam)


def scrape_game_score_flashscore(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    response = soup.find_all('span', {'class': 'scoreboard'})

    return GameScore(response[0].text, response[1].text)


if __name__ == "__main__":
    scrape_game_informations("https://www.flashscore.de/spiel/hzDoWwk8/#spiel-zusammenfassung")
    test = scrape_game_scores("https://www.flashscore.de/spiel/xUXeO6sA/#spiel-zusammenfassung")
    print("")