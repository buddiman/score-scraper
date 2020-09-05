

class GameInformations():
    '''
    Object that holds informations for a game before it starts
    '''
    def __init__(self, country, competition,
                 dateTime, homeTeam, awayTeam):
        self.country = country
        self.competition = competition
        self.dateTime = dateTime
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        return

class GameScore():
    '''
    Object that holds informations for a score
    '''
    def __init__(self, scoreHome, scoreAway):
        self.score = scoreHome + ":" + scoreAway
