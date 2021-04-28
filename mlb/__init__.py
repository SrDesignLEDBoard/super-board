import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps

from .game import Scores
from config import COLS, ROWS, INTERVAL, BRIGHTNESS


def draw_board():
    """Render board for NHL"""

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 1
    options.parallel = 1
    options.brightness = BRIGHTNESS
    options.hardware_mapping = 'adafruit-hat'

    image_size = ROWS if ROWS < COLS else COLS
    matrix = RGBMatrix(options=options)

    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/tom-thumb.bdf")
    textColor = graphics.Color(255, 255, 255)

    height_first_row = 9
    height_second_row = 18
    height_third_row = 27
    score_len = 20

    while True:
        games = Scores.get_scores()

        # TODO handle no games; Will be done after all leagues \
        # are done or at last one more
        if len(games) == 0:
            return -1

        for game in games:
            canvas.Clear()

            if game['stage'] != '':
                # Print score final or live
                score_len = len(game['score'])*4
                graphics.DrawText(canvas, font,
                                  int((COLS - score_len) / 2),
                                  height_second_row, textColor, game['score'])
                if game['stage'] == 'Progress':
                    # If game is in progress, print period \
                    # and time left in the period
                    period_len = len(game['period'])*4
                    time_len = len(game['time'])*4
                    graphics.DrawText(canvas, font,
                                      int((COLS - period_len) / 2),
                                      height_first_row, textColor,
                                      game['period'])
                    graphics.DrawText(canvas, font,
                                      int((COLS - time_len) / 2),
                                      height_third_row, textColor,
                                      game['time'])
                elif game['stage'] == 'Final':
                    # Else print 'fin' to indicate final score
                    graphics.DrawText(canvas, font,
                                      int((COLS - 12) / 2),
                                      height_first_row, textColor, "fin")
            else:
                # If planned game, print @ and time
                status_len = len(game['status'])*4
                graphics.DrawText(canvas, font,
                                  int((COLS - 4) / 2),
                                  height_first_row, textColor, "@")
                graphics.DrawText(canvas, font,
                                  int((COLS - status_len) / 2),
                                  height_second_row, textColor, game['status'])

            # Get x coords for logos
            image_space = (COLS - score_len - 4) / 2
            x_away = -ROWS + image_space
            x_away = x_away if game['stage'] != '' else x_away-5
            x_home = image_space + score_len + 4
            x_home = x_home if game['stage'] != '' else x_home+5

            # Get logos as thumbnails; home is flipped for right
            image_away = Image.open(f"logos/NHL/{game['away']}_logo.png")
            image_away.thumbnail((image_size, image_size), Image.ANTIALIAS)

            image_home = Image.open(f"logos/NHL/{game['home']}_logo.png")
            image_home = ImageOps.mirror(image_home)
            image_home.thumbnail((image_size, image_size), Image.ANTIALIAS)

            # Print logos
            canvas.SetImage(image_away.convert('RGB'), x_away, 0)
            canvas.SetImage(image_home.convert('RGB'),
                            x_home, 0)

            time.sleep(INTERVAL)
            canvas = matrix.SwapOnVSync(canvas)
