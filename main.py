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
          try:
            mlb.draw_board()
          except Exception as e:
              print("Error occured")
              print(e)

          try:
            nhl.draw_board()
          except Exception as e:
              print("Error occured")
              print(e)

          try:
            nba.draw_board()
          except Exception as e:
              print("Error occured")
              print(e)

          try:
            laliga.draw_board()
          except Exception as e:
              print("Error occured")
              print(e)
  except KeyboardInterrupt:
      sys.exit(0)

if __name__ == "__main__":
  main()
