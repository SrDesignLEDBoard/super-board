import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps

from gpiozero import Button

from .game import Scores
from config import COLS, ROWS, BRIGHTNESS, GPIO_CONTROL


def draw_board() -> int:
    """Draw components of NHL game.

    Firstly, creates a canvas for the LED matrix using various configurations.
    Requests games for the day for NHL and draws various components of the game such as team logos, scores, period, and time.

    Also, draws "SCORE!!!" animation for the game if there is an update in the score.

    If button is pressed during the execution, it will load the next game. If the game is the last one for the day in NHL, then it will
    go to the next league.

    Returns:
        int: Return -1 if no favorite game.
    """

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
    anifont = graphics.Font()
    anifont.LoadFont("./fonts/cherry-10-b.bdf")
    textColor = graphics.Color(225, 225, 0)

    height_first_row = 9
    height_second_row = 18
    height_third_row = 27

    # Control button
    button = Button(GPIO_CONTROL)

    it = 0
    wait = 0

    # Loading NHL
    canvas.Clear()
    graphics.DrawText(canvas, font,
                      11,
                      height_second_row, textColor, 'Loading NHL')
    canvas = matrix.SwapOnVSync(canvas)

    games = Scores.get_scores()
    if len(games) == 0:
        # Print no games scheduled
        canvas.Clear()
        graphics.DrawText(canvas, font,
                          4,
                          height_second_row, textColor, 'NHL - no games')
        canvas = matrix.SwapOnVSync(canvas)
        # Handle control button and wait
        button.wait_for_press(15)
        return -1

    while it < len(games):
        canvas.Clear()

        score_len = 20
        if 'score' in games[it]:
            # Change score len if 2 digit score
            score_len = 28 if games[it]['score'][3] == '-' else 20

        # Get x coords for logos
        image_space = (COLS - score_len - 4) / 2
        x_away = -ROWS + image_space - 2
        x_home = image_space + score_len + 2

        # Get logos as thumbnails; home is flipped for right
        image_away = Image.open(f"logos/NHL/{games[it]['away']}_logo.png")
        image_away.thumbnail((image_size, image_size), Image.ANTIALIAS)

        image_home = Image.open(f"logos/NHL/{games[it]['home']}_logo.png")
        image_home.thumbnail((image_size, image_size), Image.ANTIALIAS)

        # Print logos
        canvas.SetImage(image_away.convert('RGB'), x_away, 0)
        canvas.SetImage(image_home.convert('RGB'), x_home, 0)

        if games[it]['stage'] != '':
            # Print score final or live
            score_len = len(games[it]['score'])*4
            graphics.DrawText(canvas, font,
                              int((COLS - score_len) / 2),
                              height_second_row, textColor, games[it]['score'])
            if games[it]['stage'] == 'progress':
                # If game is in progress, print period \
                # and time left in the period
                if 'period' in games[it]:
                    period_len = len(games[it]['period'])*4
                    time_len = len(games[it]['time'])*4
                    graphics.DrawText(canvas, font,
                                      int((COLS - period_len) / 2),
                                      height_first_row, textColor,
                                      games[it]['period'])
                    graphics.DrawText(canvas, font,
                                      int((COLS - time_len) / 2),
                                      height_third_row, textColor,
                                      games[it]['time'])
                else:
                    graphics.DrawText(canvas, font,
                                      int((COLS - 12) / 2),
                                      height_first_row, textColor,
                                      'PRE')
            # elif games[it]['stage'] == 'final':
            else:
                # Else print 'fin' to indicate final score
                graphics.DrawText(canvas, font,
                                  int((COLS - 12) / 2),
                                  height_first_row, textColor, "FIN")
        else:
            # If planned game, print @ and time
            tmptime = games[it]['status'].split()
            time_len = len(tmptime[0])*4

            graphics.DrawText(canvas, font,
                              int((COLS - 8) / 2),
                              height_first_row, textColor, "AT")
            graphics.DrawText(canvas, font,
                              int((COLS - time_len) / 2),
                              height_second_row, textColor, tmptime[0])
            graphics.DrawText(canvas, font,
                              int((COLS - 20) / 2),
                              height_third_row, textColor, tmptime[1] + ' ET')

        # Handle control button and wait
        is_button_pressed = button.wait_for_press(5)

        # Increment iterator if button was pressed
        if is_button_pressed:
            it += 1
            time.sleep(1)

        # Mention to the user that they should wait after pressing the button
        # for about 5-10 seconds as it takes a while to fetch score
        wait += 1
        if wait > 12 and it < len(games):
            wait = 0
            tmp = Scores.get_scores()

            # Check if new fixes
            if games[it]['away'] != games[it]['away'] and \
                    tmp[it]['home'] != tmp[it]['home']:
                it = 0
            elif games[it]['stage'] == 'progress' and games[it]['score'] != tmp[it]['score']:
                # check for score update
                pos = ROWS
                rounds = 0
                while True:
                    canvas.Clear()
                    l = graphics.DrawText(
                        canvas, anifont, pos, height_second_row, textColor, 'GOAL!!!')
                    pos -= 1
                    if (pos + l < 0):
                        pos = ROWS
                        rounds += 1
                        if rounds > 3:
                            break

                    time.sleep(0.05)
                    canvas = matrix.SwapOnVSync(canvas)

            games = tmp

        canvas = matrix.SwapOnVSync(canvas)
