import utils
import config
import datetime
import constants
from typing import List, Tuple, Dict

from .teams import abbreviations_full


class Game:
    """Represent a scheduled MLB game.

    Game object first parses the JSON dict information.
    Also contains method to get matchup as a simplified dict.

    Args:
        game_info (Dict[str, any]): Dictionary generated from JSON object
    """

    def __init__(self, game_info: Dict[str, any], a_name: str, h_name: str):
        """Parse JSON to attributes

        Args:
            game_info (Dict[str, any]): Dictionary generated from JSON object
        """
        # Open new json file that includes live updates to the game
        liveData = utils.get_JSON('http://statsapi.mlb.com'+game_info['link'])

        # Parse JSON to attributes
        self.game_id = str(game_info['gamePk'])

        # Possible States: Scheduled, Pre-Game, Warmup, In Progress, Final
        self.game_stage = game_info['status']['detailedState']

        # Capitalize the status of the game so its easier to be displayed
        self.game_status = game_info['status']['abstractGameState'].upper()

        if 'score' in game_info['teams']['away'] or \
           'score' in game_info['teams']['home']:
            self.away_score = str(game_info['teams']['away']['score'])
            self.home_score = str(game_info['teams']['home']['score'])
        else:
            self.away_score = ''
            self.home_score = ''

        self.away_name = a_name
        self.home_name = h_name

        # Inning information only available when the game starts
        if 'currentInningOrdinal' in liveData['liveData']['linescore'] and \
                self.game_status == 'LIVE':
            self.game_clock = liveData['liveData']['linescore']['currentInningOrdinal']
        else:
            self.game_clock = liveData['gameData']['datetime']['time'] + ' ' + \
                liveData['gameData']['datetime']['ampm']

        # Top Inning variable only available when the game starts
        if 'isTopInning' in liveData['liveData']['linescore']:
            self.top_inning = liveData['liveData']['linescore']['isTopInning']
            self.strikes = liveData['liveData']['linescore']['strikes']
            self.outs = liveData['liveData']['linescore']['outs']
        else:
            self.top_inning = 'false'
            self.strikes = ''
            self.outs = ''

    def get_matchup(self) -> Dict[str, str]:
        """Get information of a single game.

        Simply game information into a dictionary to be used by the draw_board() function.
        Returns a dictionary with names for home and away team, game period, game status, 
        score, and starttime.

        Returns:
            Dict[str, str]: Game information in a dictionary.
        """
        matchup = {
            "home": self.home_name,
            "away": self.away_name,
            "stage": self.game_stage,
            "status": self.game_status,
            "period": self.game_clock
        }
        if self.game_stage != '':
            if self.away_score == '' and self.home_score == '':
                matchup["score"] = "0 - 0"
            else:
                matchup["score"] = f"{self.away_score} - {self.home_score}"

        return matchup


class Scores:
    """Scores Class with static function to get scores for the leauge.
    """
    @staticmethod
    def get_scores() -> List[Tuple[str, str]]:
        """Get a list of favorite scores/games that are on-going or planned for the day.

        First, calls for the request of JSON from MLB API and checks if games are favorites.
        If so, then it creates Game objects from the data.

        Returns:
            List[Tuple[str, str]]: List of python dicts that contain information of today's games.
        """
        try:
            data = utils.get_JSON(constants.MLB_API)

            # Only focus on the games scheduled today in the JSON file
            all_games = data['dates'][0]['games']

            gs = []

            for game_info in all_games:
                # Converts team full name to its abbreviation
                away_name = abbreviations_full[game_info['teams']
                                               ['away']['team']['name']]
                home_name = abbreviations_full[game_info['teams']
                                               ['home']['team']['name']]

                # Only find information for teams that the user designates as their favorite
                if away_name not in config.MLB_FAVS and \
                   home_name not in config.MLB_FAVS:
                    continue

                game = Game(game_info, away_name, home_name)

                gs.append(game.get_matchup())

            return gs
        except Exception as e:
            return print(e)
