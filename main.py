import sys
import nhl

try:
    print("Press CTRL-C to stop.")
    nhl.draw_board()
except KeyboardInterrupt:
    sys.exit(0)
