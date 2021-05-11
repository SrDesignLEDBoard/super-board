import utils
import config
import constants
from typing import List, Tuple, Dict

from .teams import abbreviations
from .fix_names import *


class Game:
    """Represent a scheduled NHL game

    Game object first parses the JSON dict information.
    Also contains methods to check if the game is scheduled today and if the game is of a favorite team.

    Args:
        game_info (Dict[str, any]): Dictionary generated from JSON object
    """

    def __init__(self, game_info: Dict[str, any]):
        """Parse JSON to attributes

        Args:
            game_info (Dict[str, any]): Dictionary generated from JSON object
        """
        self.game_id = str(game_info['id'])
        self.game_clock = game_info['ts']
        self.game_stage = game_info['tsc']
        self.game_status = game_info['bs']
        self.away_name = abbreviations[fix_name(game_info['atv'])]
        self.away_score = game_info['ats']
        self.home_name = abbreviations[fix_name(game_info['htv'])]
        self.home_score = game_info['hts']

    def get_matchup(self) -> Dict[str, str]:
        """Get information of a single game.

        Simply game information into a dictionary to be used by the draw_board() function.
        Returns a dictionary with names for home and away team, game stage, game status, game clock,
        score. If the game stage is in progress and the status is live or pre, then also includes time and period fields.

        Returns:
            Dict[str, str]: Game information in a dictionary.
        """
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

    def is_scheduled_for_today(self) -> bool:
        """Check if game is scheduled for today.

        The scoreboard is used to show only the games scheduled for the current day.
        Since the NHL API returns a JSON with games for the entire week, this function is used to pick out the games
        for the current day.

        Returns:
            bool: True if game if scheduled for today.
        """
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

    def is_favorite_match(self) -> bool:
        """Check if game has a team favorited by the user.

        Since only the games included in the favorite config are shown, this function checks that
        either home or away team is a favorite.

        Returns:
            bool: True if game if either home or away team is a favorite.
        """
        for team in config.NHL_FAVS:
            if team == self.home_name or team == self.away_name:
                return True
        return False


class Scores:
    """Scores Class with static function to get scores for the leauge.
    """
    @staticmethod
    def get_scores() -> List[Tuple[str, str]]:
        """Get a list of favorite scores/games that are on-going or planned for the day.

        First, calls for the request of JSON from NHL API and creates Game objects from the data.
        Then, checks for the games scheduled for the day and if the games are favorites.

        Returns:
            List[Tuple[str, str]]: List of python dicts that contain information of today's games. Empty list if no games fit the criteria.
        """
        try:
            data = utils.get_JSON(constants.NHL_API)
            games = []

            for game_info in data['games']:
                game = Game(game_info)
                if game.is_scheduled_for_today():
                    games.append(game)

            gs = []
            for game in games:
                if not game.is_favorite_match():
                    continue

                gs.append(game.get_matchup())

            return gs
        except Exception as e:
            return print(e)
