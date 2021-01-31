# import datetime
# import json
# import requests
import utils
import config
import constants
from typing import List, Tuple, Dict

from nhl.teams import abbreviations
import nhl.fixes as fixes


class Game:
    """Game represents a scheduled NHL game"""
    def __init__(self, game_info: Dict[str, any]):
        """Parse JSON to attributes"""
        self.game_id = str(game_info['id'])
        self.game_clock = game_info['ts']
        self.game_stage = game_info['tsc']
        self.game_status = game_info['bs']
        self.away_locale = fixes.fix_locale(game_info['atn'])
        self.away_name = abbreviations[fixes.fix_name(game_info['atv'])]
        self.away_score = game_info['ats']
        self.away_result = game_info['atc']
        self.home_locale = fixes.fix_locale(game_info['htn'])
        self.home_name = abbreviations[fixes.fix_name(game_info['htv'])]
        self.home_score = game_info['hts']
        self.home_result = game_info['htc']

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
            "score": f"{self.away_score} - {self.home_score}"
        }
        return score

    def get_matchup(self, width: int) -> str:
        """Get full names of both teams"""
        matchup = f"{self.away_name} @ {self.home_name}"
        return matchup

    def get_playoff_info(self, width: int) -> str:
        """Get title of playoff series"""
        playoff_info = fixes.playoff_series_info(self.playoff_round,
                                                 self.playoff_series_id)
        playoff_info += ' -- GAME ' + self.playoff_series_game
        return playoff_info.center(width)

    def get_clock(self, width: int) -> str:
        """Get game clock and status"""
        clock = self.game_clock + ' (' + self.game_status + ')'
        # return clock.center(width)
        return clock

    def is_scheduled_for(self, date: str) -> bool:
        """True if this game is scheduled for the given date"""
        if date.upper() in self.game_clock:
            return True
        else:
            return False

    def normalize_today(self) -> bool:
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

    def is_scheduled_for_today(self) -> bool:
        """True if this game is scheduled for today"""
        if self.normalize_today():
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

                game_summary = None

                if game.game_stage != '':
                    game_summary = (game.get_scoreline(config.COLS),
                                    game.get_clock(config.COLS))
                else:
                    game_summary = (game.get_matchup(config.COLS),
                                    game.get_clock(config.COLS))

                gs.append(game_summary)
            return gs
        except Exception as e:
            return print(e)
