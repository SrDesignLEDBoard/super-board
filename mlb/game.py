import utils
import config
import datetime
import constants
from typing import List, Tuple, Dict

from .teams import abbreviations_full

class Game:
    """Game represents a scheduled NHL game"""
    def __init__(self, game_info: Dict[str, any], a_name: str, h_name: str): 
        """Open new json file that includes live updates to the game"""
        liveData = utils.get_JSON('http://statsapi.mlb.com'+game_info['link'])

        """Parse JSON to attributes"""
        self.game_id = str(game_info['gamePk'])

        """Possible States: Scheduled, Pre-Game, Warmup, In Progress, Final"""
        self.game_stage = game_info['status']['detailedState']

        """Capitalize the status of the game so its easier to be displayed"""
        self.game_status = game_info['status']['abstractGameState'].upper()

        if 'score' in game_info['teams']['away'] or \
           'score' in game_info['teams']['home'] :
            self.away_score = str(game_info['teams']['away']['score'])
            self.home_score = str(game_info['teams']['home']['score']) 
        else :
            self.away_score = '0'
            self.home_score = '0'

        #self.away_name = liveData['gameData']['teams']['away']['abbreviation']
        #self.home_name = liveData['gameData']['teams']['home']['abbreviation']
        self.away_name = a_name
        self.home_name = h_name

        """Inning information only available when the game starts"""
        if 'currentInningOrdinal' in liveData['liveData']['linescore'] :
            self.game_clock = liveData['liveData']['linescore']['currentInningOrdinal'] + ' Inning'
        else :
            self.game_clock = ('TODAY @ ' + liveData['gameData']['datetime']['time'] +
                               ' '  + liveData['gameData']['datetime']['ampm'])

        """Top Inning variable only available when the game starts"""
        if 'isTopInning' in liveData['liveData']['linescore']:
            self.top_inning = liveData['liveData']['linescore']['isTopInning']
            self.strikes = liveData['liveData']['linescore']['strikes']
            self.outs = liveData['liveData']['linescore']['outs']
        else:
            self.top_inning = 'false'
            self.strikes = '0'
            self.outs = '0'

    def get_scoreline(self, width: int) -> Dict[str, str]:
        """Get current score in a dict with team names and score"""
        score = {
            "home": self.home_name,
            "away": self.away_name,
            "score": f"{self.away_score} - {self.home_score}",
            "status": self.game_status
        }
        return score

    def get_matchup(self, width: int) -> Dict[str, str]:
        """Get full names of both teams"""
        matchup = {
            "home": self.home_name,
            "away": self.away_name,
            "stage": self.game_stage,
            "status": self.game_status,
            "clock": self.game_clock
        }
        if self.game_stage != '':
            if self.away_score == '' and self.home_score == '':
                matchup["score"] = "0 - 0"
            else:
                matchup["score"] = f"{self.away_score} - {self.home_score}"

        if self.game_stage == 'progress' and self.game_status == 'LIVE' and 'PRE' not in self.game_clock:
            tmp = self.game_clock.split(' ')
            matchup["time"], matchup["period"] = tmp[0], tmp[1]
        return matchup

    def get_clock(self, width: int) -> str:
        """Get game clock and status"""
        clock = self.game_clock + ' (' + self.game_status + ')'
        return clock

    def is_scheduled_for(self, date: str) -> bool:
        """True if this game is scheduled for the given date"""
        if date.upper() in self.game_clock:
            return True
        else:
            return False

    def is_scheduled_for_today(self) -> bool:
        """True if this game is scheduled for today"""
        date = utils.get_date(0)

        # must be today
        if date.upper() in self.game_clock or \
                'TODAY' in self.game_clock[0:5]:
            return True
        elif 'Inning' in self.game_clock[-6:]:
            return True
        return False

    def is_favorite_match(self, favorites: List[str]) -> bool:
        """True if game has a team favorited by the user."""
        for team in favorites:
            if team == self.home_name or team == self.away_name:
                return True
        return False


class Scores:
    @staticmethod
    def get_scores() -> List[Tuple[str, str]]:
        """Get a list of scores/games that are on-going
                or planned for the day (in that order)"""
        # format = [
        #     {'home': 'NYR', 'away': 'PIT', 'stage': 'progress', 'status': 'LIVE', 'time': '17:22', 'period': '1st', 'score': '2 - 0'},
        #     {'home': 'MTL', 'away': 'VAN', 'stage': 'final', 'status': 'FINAL', 'clock': 'TODAY', 'score': '2 - 6'},
        #     {'home': 'WIN', 'away': 'CGY', 'stage': '', 'status': '5:00 PM', 'clock': 'TODAY'}
        # ]

        try:
            data = utils.get_JSON(constants.MLB_API)

            """Only focus on the games scheduled today in the JSON file"""
            all_games = data['dates'][0]['games']

            gs = []

            for game_info in all_games:
                """Converts team full name to its abbreviation"""
                away_name = abbreviations_full[game_info['teams']['away']['team']['name']]
                home_name = abbreviations_full[game_info['teams']['home']['team']['name']]

                """Only find information for teams that the user designates as their favorite"""
                if away_name not in config.MLB_FAVS and \
                   home_name not in config.MLB_FAVS:
                    continue

                game = Game(game_info, away_name, home_name)

                if game.is_scheduled_for_today():
                    gs.append(game.get_matchup(config.COLS)) 

            return gs
        except Exception as e:
            return print(e)
