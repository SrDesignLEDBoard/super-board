import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from gpiozero import Button

from config import COLS, ROWS, INTERVAL, BRIGHTNESS


def draw_loading():
    """Render loading screen"""

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 1
    options.parallel = 1
    options.brightness = BRIGHTNESS
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options=options)

    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/tom-thumb.bdf")
    textColor = graphics.Color(255, 255, 255)

    height_second_row = 18

    loading_text = "Loading..."
    loading_len = len(loading_text)
    graphics.DrawText(canvas, font,
                      int((COLS - loading_len) / 2),
                      height_second_row, textColor, loading_text)

    # canvas = matrix.SwapOnVSync(canvas)
