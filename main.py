"""Root file of the project.
"""

import sys
import nhl, mlb, nba, laliga


def main():
  """Runs main loop for the four leagues
  """
  try:
      print("Press CTRL-C to stop.")
      while True:
          nhl.draw_board()
          nba.draw_board()
          mlb.draw_board()
          laliga.draw_board()
  except KeyboardInterrupt:
      sys.exit(0)

if __name__ == "__main__":
  main()