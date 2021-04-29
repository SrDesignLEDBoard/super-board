import sys
# import nhl, mlb, nba
import laliga

try:
    print("Press CTRL-C to stop.")
    while True:
        laliga.draw_board()
        # nhl.draw_board()
        # mlb.draw_board()
        # nba.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
