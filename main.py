#!/usr/bin/env python3

import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps

import nhl
from config import COLS, ROWS, INTERVAL


def draw_board():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 1
    options.parallel = 1
    options.brightness = 80
    options.hardware_mapping = 'adafruit-hat'

    image_size = ROWS if ROWS < COLS else COLS
    matrix = RGBMatrix(options=options)

    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)

    while True:
        games = nhl.Scores.get_scores()
        for game in games:
            canvas.Clear()

            matchup, game_time = game
            score_len = len(matchup['score'])*4

            image_home = Image.open(f"logos/NHL/{matchup['home']}_logo.png")
            image_home = ImageOps.mirror(image_home)
            image_home.thumbnail((image_size, image_size), Image.ANTIALIAS)

            image_away = Image.open(f"logos/NHL/{matchup['away']}_logo.png")
            image_away.thumbnail((image_size, image_size), Image.ANTIALIAS)

            # Show score
            graphics.DrawText(canvas, font,
                              int((COLS - score_len) / 2),
                              13, textColor, matchup['score'])
            # TODO fix the time on the board
            # graphics.DrawText(canvas, font,
            #                       int((COLS - (len(game_time)*4 - 1)) / 2),
            #                       24, textColor, game_time)

            # Show team logos
            image_space = (COLS - score_len - 4) / 2
            canvas.SetImage(image_home.convert('RGB'),
                            image_space + score_len + 4, 0)
            canvas.SetImage(image_away.convert('RGB'), -ROWS + image_space, 0)

            time.sleep(INTERVAL)
            canvas = matrix.SwapOnVSync(canvas)


try:
    print("Press CTRL-C to stop.")
    draw_board()
except KeyboardInterrupt:
    sys.exit(0)
