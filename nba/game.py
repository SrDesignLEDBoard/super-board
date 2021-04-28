import utils
import config
import constants
from typing import List, Tuple, Dict

from .teams import abbreviations
from .fix_names import *


class Game:
    """Game represents a scheduled NBA game"""
    def __init__(self, game_info: Dict[str, any]):
        """Parse JSON to attributes"""
        self.game_id = str(game_info['gameId'])
        self.game_clock = game_info['clock']
        self.game_period = game_info['period']['current']
        self.game_status = game_info['isGameActivated']

        self.start_date = game_info['startDateEastern']

        self.away_name = game_info['vTeam']['triCode']
        self.away_score = game_info['vTeam']['score']

        self.home_name = game_info['hTeam']['triCode']
        self.home_score = game_info['hTeam']['score']

        # Playoff-specific game information
        # if '03' in self.game_id[4:6]:
        #     self.playoffs = True
        #     self.playoff_round = self.game_id[6:8]
        #     self.playoff_series_id = self.game_id[8:9]
        #     self.playoff_series_game = self.game_id[9]
        # else:
        #     self.playoffs = False

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
            "period": self.game_period,
            "status": self.game_status,
            "clock": self.game_clock
        }
        if self.game_period:
            if self.away_score == '' and self.home_score == '':
                matchup["score"] = "0 - 0"
            else:
                matchup["score"] = f"{self.away_score} - {self.home_score}"

        if self.game_period != 0 and self.game_status :
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
                'TODAY' in self.game_clock:
            self.game_clock = 'TODAY'
            return True
        # or must be pre-game
        # elif 'PRE GAME' in self.game_clock:
        #     self.game_clock = 'PRE-GAME'
        #     return True
        # # or game must be live
        # elif 'LIVE' in self.game_status:
        #     return True
        # return False

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
        #     {"seasonStageId":2,"seasonYear":"2020","leagueName":"standard","gameId":"0022000448","arena":{"name":"Spectrum Center",
        #     "isDomestic":true,"city":"Charlotte","stateAbbr":"NC","country":"USA"},"isGameActivated":false,"statusNum":1,
        #     "extendedStatusNum":2,"startTimeEastern":"7:00 PM ET","startTimeUTC":"2021-02-20T00:00:00.000Z","startDateEastern":"20210219",
        #     "homeStartDate":"20210219","homeStartTime":"1900","visitorStartDate":"20210219","visitorStartTime":"1700",
        #     "gameUrlCode":"20210219/DENCHA","clock":"","isBuzzerBeater":false,"isPreviewArticleAvail":false,"isRecapArticleAvail":false,
        #     "nugget":{"text":""
        # ]

        try:
            data = utils.get_JSON(constants.NBA_API)
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
