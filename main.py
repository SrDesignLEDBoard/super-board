import sys
# import nhl, mlb, NBA
import NBA

try:
    print("Press CTRL-C to stop.")
    NBA.draw_board()
    # while True:
        # nhl.draw_board()
        # mlb.draw_board()
        # NBA.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
