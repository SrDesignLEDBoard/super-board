import utils
import config
import constants
import datetime
from typing import List, Tuple, Dict

class Game:
    """Game represents a scheduled NBA game"""
    def __init__(self, game_info: Dict[str, any]):
        """Parse JSON to attributes"""
        self.game_id = str(game_info['gameId'])
        self.game_clock = game_info['clock']
        self.game_period = game_info['period']['current']
        self.game_status = game_info['isGameActivated']
        self.game_status_num = game_info['statusNum']

        self.start_time = game_info['startTimeEastern'][:-3]

        self.away_name = game_info['vTeam']['triCode']
        self.away_score = game_info['vTeam']['score']

        self.home_name = game_info['hTeam']['triCode']
        self.home_score = game_info['hTeam']['score']

    def get_matchup(self, width: int) -> Dict[str, str]:
        """Get full names of both teams"""
        matchup = {
            "home": self.home_name,
            "away": self.away_name,
            "period": str(self.game_period),
            "status": self.game_status,
            "status_num": self.game_status_num,
            "clock": self.game_clock,
            "starttime": self.start_time
        }

        if self.game_period:
            if self.away_score == '' and self.home_score == '':
                matchup["score"] = "0 - 0"
            else:
                matchup["score"] = f"{self.away_score} - {self.home_score}"

        return matchup

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

        x = datetime.datetime.now()

        try:
            data = utils.get_JSON(f"http://data.nba.net/prod/v1/{x.strftime('%Y%m%d')}/scoreboard.json")
            games = []

            for game_info in data['games']:
                games.append(Game(game_info))

            gs = []
            for game in games:
                if not game.is_favorite_match(config.NBA_FAVS):
                    continue

                gs.append(game.get_matchup(config.COLS))

            return gs
        except Exception as e:
            return print(e)
