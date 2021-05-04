import sys
import nhl, mlb, nba, laliga

try:
    print("Press CTRL-C to stop.")
    while True:
        nhl.draw_board()
        nba.draw_board()
        mlb.draw_board()
        laliga.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
