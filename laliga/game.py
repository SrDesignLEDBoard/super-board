import utils
import config
import constants
import datetime
from typing import List, Tuple, Dict

from .teams import abbreviations_full


class Game:
    """Represent a scheduled La Liga game.

    Game object first parses the JSON dict information.
    Also contains methods to check if the game is of a favorite team.

    Args:
        game_info (Dict[str, any]): Dictionary generated from JSON object
        a_name (str): Name of away team
        h_name (str): Name of home team
    """

    def __init__(self, game_info: Dict[str, any], a_name: str, h_name: str):
        """Parse JSON to attributes

        Args:
            game_info (Dict[str, any]): Dictionary generated from JSON object
            a_name (str): Name of away team
            h_name (str): Name of home team
        """
        self.game_id = str(game_info['id'])
        self.game_stage = game_info['status']['type']['description']
        self.game_status = game_info['status']['type']['state']

        if game_info['status']['displayClock'] == "0'":
            #self.game_clock = game_info['status']['type']['shortDetail']
            self.game_clock = datetime.datetime.strptime(game_info['date'],
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

    def get_matchup(self) -> Dict[str, str]:
        """Get information of a single game.

        Simply game information into a dictionary to be used by the draw_board() function.
        Returns a dictionary with names for home and away team, game period, game stage, game status, game clock,
        score.

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

        matchup['period'] = 'H' + str(self.game_period)
        return matchup


class Scores:
    """Scores Class with static function to get scores for the leauge.
    """
    @staticmethod
    def get_scores() -> List[Tuple[str, str]]:
        """Get a list of favorite scores/games that are on-going or planned for the day.

        First, calls for the request of JSON from La Liga API and checks if games are favorites.
        If so, then it creates Game objects from the data.

        Returns:
            List[Tuple[str, str]]: List of python dicts that contain information of today's games.
        """
        try:
            data = utils.get_JSON(constants.LALIGA_API)

            # """Only focus on the games scheduled today"""
            all_games = data['events']

            gs = []

            for game_info in all_games:
                # """Only add teams that are the user's favorites"""
                away_name = abbreviations_full[game_info['competitions']
                                               [0]['competitors'][1]['team']['name']]
                home_name = abbreviations_full[game_info['competitions']
                                               [0]['competitors'][0]['team']['name']]

                if away_name not in config.LALIGA_FAVS and \
                   home_name not in config.LALIGA_FAVS:
                    continue

                game = Game(game_info, away_name, home_name)

                gs.append(game.get_matchup())

            return gs
        except Exception as e:
            return print(e)
