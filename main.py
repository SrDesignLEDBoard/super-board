import sys
import nhl, mlb

try:
    print("Press CTRL-C to stop.")
    while True:
        nhl.draw_board()
        mlb.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
