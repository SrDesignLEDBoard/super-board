"""Root file of the project.
"""

import sys
import nhl
import mlb
import nba
import laliga


def main():
    """Runs main loop for the four leagues.

    If a user wants to remove certain leauges, they can comment out the parts from the main loop.
    They can also reorder the leagues by swapping parts of the code.

    todo: 
        Post Senior Design additions: Add functionality to enable/disable leauges and reorder them using the config file.
    """
    try:
        print("Press CTRL-C to stop.")
        while True:
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
                mlb.draw_board()
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
