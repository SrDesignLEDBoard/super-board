"""Configurations for LEDScorebard program"""
from typing import List

COLS = 64
"""int: Number of columnns in the LED matrix"""

ROWS = 32
"""int: Number of rows in the LED matrix"""

GPIO_MAPPING = "adafruit-hat"
"""str: Type of GPIO mappings for LED matrix bonet"""

GPIO_CONTROL = 25
"""int: GPIO for control button"""

BRIGHTNESS = 60
"""int: Brightness (1-100) for LEDs of the matrix"""

MLB_FAVS = ['BOS']
"""List[str]: List of abbreviations of favorite teams in MLB"""

NBA_FAVS = ['BKN', 'DAL']
"""List[str]: List of abbreviations of favorite teams in NBA"""

NHL_FAVS = ['PIT', 'EDM']
"""List[str]: List of abbreviations of favorite teams in NHL"""

LALIGA_FAVS = ['FCB', 'ATB']
"""List[str]: List of abbreviations of favorite teams in La Liga"""

