import nhl
import config
from samplebase import SampleBase
from rgbmatrix import graphics
import time

def main():
    try:
        data = nhl.get_JSON('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')
        games = []

        for game_info in data['games']:
            game = nhl.Game(game_info)
            if game.is_scheduled_for_today():
                games.append(game)

        for game in games:
                game_summary = ""

                game_summary += game.get_matchup(config.WIDTH) + " " + \
                    game.get_clock(config.WIDTH) + '\n'

                if game.game_stage != '':
                    game_summary += game.get_scoreline(config.WIDTH) + '\n'
                # print(game_summary)
                RunText.run(game_summary)
    except:
        return 0

class RunText(SampleBase):
    def __init__(self):
        pass

    def run(self, text="Hello, World!"):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
    main()