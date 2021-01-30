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

        gs = []
        for game in games:
                if not game.is_favorite_match(config.NHL_FAVS): continue

                game_summary = None

                if game.game_stage != '':
                    game_summary = (game.get_scoreline(config.COLS), game.get_clock(config.COLS))
                else:
                    game_summary = (game.get_matchup(config.COLS), game.get_clock(config.COLS))
                
                gs.append(game_summary)
        return gs
    except Exception as e:
        return print(e)

if __name__ == "__main__":
    print(getNHLScore())
    # for i in getNHLScore():
    #     print(i)
