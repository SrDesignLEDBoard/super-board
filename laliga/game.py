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
            self.game_period = 0
        else:
            # self.game_clock = game_info['status']['displayClock']
            self.game_clock = game_info['status']['type']['shortDetail']
            self.game_period = game_info['status']['period']

        self.away_name = a_name
        self.away_score = game_info['competitions'][0]['competitors'][1]['score']
        self.home_name = h_name
        self.home_score = game_info['competitions'][0]['competitors'][0]['score']

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

        matchup['period'] = 'H' + str(self.game_period)
        return matchup


class Scores:
    @staticmethod
    def get_scores() -> List[Tuple[str, str]]:
        """Get a list of scores/games that are on-going
                or planned for the day (in that order)"""

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
