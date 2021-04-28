import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps

from gpiozero import Button

from .game import Scores
from config import COLS, ROWS, INTERVAL, BRIGHTNESS

def draw_board():
    """Render board for NBA"""

    games = Scores.get_scores()
    if len(games) == 0:
        return -1

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

    # Control button
    button = Button(25)

    it = 0
    wait = 0

    while it < len(games):
        canvas.Clear()

        if games[it]['status']:
            # Print score final or live
            score_len = len(games[it]['score'])*4
            graphics.DrawText(canvas, font,
                                int((COLS - score_len) / 2),
                                height_second_row, textColor, games[it]['score'])
            if games[it]['period']['current'] > 0:
                # If game is in progress, print period \
                # and time left in the period
                period_len = len(games[it]['period']['current'])*4
                time_len = len(games[it]['clock'])*4
                graphics.DrawText(canvas, font,
                                    int((COLS - period_len) / 2),
                                    height_first_row, textColor,
                                    games[it]['period'])
                graphics.DrawText(canvas, font,
                                    int((COLS - time_len) / 2),
                                    height_third_row, textColor,
                                    games[it]['clock'])
        else:
            # If planned game, print @ and time
            graphics.DrawText(canvas, font,
                                int((COLS - 4) / 2),
                                height_first_row, textColor, "@")

        # Get x coords for logos
        image_space = (COLS - score_len - 4) / 2
        x_away = -ROWS + image_space
        x_away = x_away if games[it]['period'] != '' else x_away-5
        x_home = image_space + score_len + 4
        x_home = x_home if games[it]['period'] != '' else x_home+5

        # Get logos as thumbnails; home is flipped for right
        image_away = Image.open(f"logos/NBA/{games[it]['away']}_logo.png")
        image_away.thumbnail((image_size, image_size), Image.ANTIALIAS)

        image_home = Image.open(f"logos/NBA/{games[it]['home']}_logo.png")
        # image_home = ImageOps.mirror(image_home)
        image_home.thumbnail((image_size, image_size), Image.ANTIALIAS)

        # Print logos
        canvas.SetImage(image_away.convert('RGB'), x_away, 0)
        canvas.SetImage(image_home.convert('RGB'),
                        x_home, 0)

        # Handle control button and wait
        is_button_pressed = button.wait_for_press(5)

        # Increment iterator if button was pressed
        if is_button_pressed:
            it += 1
            time.sleep(2)

        # Mention to the user that they should wait after pressing the button
        # for about 5-10 seconds as it takes a while to fetch score
        wait += 1
        if wait > 12:
            wait = 0
            tmp = Scores.get_scores()

            # Check if new fixes
            if games[it]['away'] != games[it]['away'] and \
                tmp[it]['home'] != tmp[it]['home']:
                it = 0
            games = tmp

        canvas = matrix.SwapOnVSync(canvas)
