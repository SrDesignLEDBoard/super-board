#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import nhlscore
import time
import config


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = 0
        game = ""

        while True:
            games = nhlscore.getNHLScore()
            for game in games:
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, game)
                time.sleep(config.SCROLL)

            if config.INTERVAL - config.SCROLL * len(games) > 0:
                time.sleep(config.INTERVAL)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
