#!/usr/bin/env python
# Display a runtext with double-buffering.
import time

from samplebase import SampleBase
from rgbmatrix import graphics

import nhl
from config import COLS, INTERVAL


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text",
                                 help="The text on the RGB LED panel",
                                 default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 255)

        while True:
            # Will not run. Have to modify the import
            # I remodled the nhl before merging into main
            games = nhl.Scores.get_scores()
            for game in games:
                matchup, game_time = game
                score_line = f"{matchup['away']} {matchup['score']} {matchup['home']}"
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, font,
                                  int((COLS - (len(score_line)*4 - 1)) / 2),
                                  13, textColor, score_line)
                graphics.DrawText(offscreen_canvas, font,
                                  int((COLS - (len(game_time)*4 - 1)) / 2),
                                  24, textColor, game_time)
                time.sleep(INTERVAL)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()