import nhl
import config

def getNHLScore():
    try:
        data = nhl.get_JSON('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')
        games = []

        for game_info in data['games']:
            game = nhl.Game(game_info)
            if game.is_scheduled_for_today():
                games.append(game)

        for game in games:
                game_summary = ""

                game_summary += game.get_matchup(config.COLS) + " " + \
                    game.get_clock(config.COLS)

                if game.game_stage != '':
                    game_summary += game.get_scoreline(config.COLS)
                # print(game_summary)
                # RunText.run(game_summary)
                return game_summary
    except:
        return 0

if __name__ == "__main__":
    print(getNHLScore())
