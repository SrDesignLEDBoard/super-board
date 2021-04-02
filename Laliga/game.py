import utils
import config
import constants
from typing import List, Tuple, Dict

from .teams import abbreviations
from .fix_names import *


class Game:
    """Game represents a scheduled NHL game"""
    def __init__(self, game_info: Dict[str, any]):
        """Parse JSON to attributes"""
        self.game_id = str(game_info['id'])
        self.game_clock = game_info['ts']
        self.game_stage = game_info['tsc']
        self.game_status = game_info['bs']
        self.away_name = abbreviations[fix_name(game_info['atv'])]
        self.away_score = game_info['ats']
        self.home_name = abbreviations[fix_name(game_info['htv'])]
        self.home_score = game_info['hts']

        # Playoff-specific game information
        if '03' in self.game_id[4:6]:
            self.playoffs = True
            self.playoff_round = self.game_id[6:8]
            self.playoff_series_id = self.game_id[8:9]
            self.playoff_series_game = self.game_id[9]
        else:
            self.playoffs = False

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
                'TODAY' in self.game_clock:
            self.game_clock = 'TODAY'
            return True
        # or must be pre-game
        elif 'PRE GAME' in self.game_clock:
            self.game_clock = 'PRE-GAME'
            return True
        # or game must be live
        elif 'LIVE' in self.game_status:
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
            data = utils.get_JSON(constants.NHL_API)
            games = []

            for game_info in data['games']:
                game = Game(game_info)
                if game.is_scheduled_for_today():
                    games.append(game)

            gs = []
            for game in games:
                if not game.is_favorite_match(config.NHL_FAVS):
                    continue

                gs.append(game.get_matchup(config.COLS))

            return gs
        except Exception as e:
            return print(e)
