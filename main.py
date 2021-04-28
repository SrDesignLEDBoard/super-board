import sys
import nhl, mlb, nba

try:
    print("Press CTRL-C to stop.")
    while True:
        nhl.draw_board()
        mlb.draw_board()
        nba.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
