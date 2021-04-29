import utils
import config
import constants
import datetime
from typing import List, Tuple, Dict

from .teams import abbreviations_full

class Game:
    """Game represents a scheduled NHL game"""
    def __init__(self, game_info: Dict[str, any], a_name: str, h_name: str):
        """Parse JSON to attributes"""
        self.game_id = str(game_info['id'])
        self.game_stage = game_info['status']['type']['description']
        self.game_status = game_info['status']['type']['state']

        if game_info['status']['displayClock'] == "0'":
            #self.game_clock = game_info['status']['type']['shortDetail']
            self.game_clock = datetime.datetime.strptime(game_info['date'], \
                              '%Y-%m-%dT%H:%SZ').strftime('%H:%S')
        else:
            self.game_clock = game_info['status']['displayClock']

        self.away_name = a_name
        self.away_score = game_info['competitions'][0]['competitors'][1]['score']
        self.home_name = h_name
        self.home_score = game_info['competitions'][0]['competitors'][0]['score']

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

        if self.game_stage == 'progress' and self.game_status == 'live' and 'pre' not in self.game_clock:
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
            data = utils.get_JSON(constants.LALIGA_API)
            
            """Only focus on the games scheduled today"""
            all_games = data['events']

            gs = []

            for game_info in all_games:
                """Only add teams that are the user's favorites"""
                away_name = abbreviations_full[game_info['competitions'][0]['competitors'][1]['team']['name']]
                home_name = abbreviations_full[game_info['competitions'][0]['competitors'][0]['team']['name']]

                if away_name not in config.LALIGA_FAVS and \
                   home_name not in config.LALIGA_FAVS:
                    continue

                game = Game(game_info, away_name, home_name)

                gs.append(game.get_matchup(config.COLS))

            return gs
        except Exception as e:
            return print(e)
