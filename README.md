# LEDScoreboard

## Running the code
Since we only have a single hardware device, make a file like `tmp.py` to check your results. For example:
```py
# tmp.py for nhl
import nhl

print(nhl.Scores.get_scores())
```

Sample output
```
[('PIT 2 - NYR 1', '13:28 2nd (LIVE)'), ('NJD 3 - BUF 4', 'TODAY (FINAL SO)')]
```

## Check PEP8 conventions
They are pretty simple and standard. Just for consistency in code from 6 people

Make executable
```bash
chmod +x check_pep8.sh
```

Run to check code
```bash
./check_pep8.sh
```

Commit only if it returns no output. And, add folders to the command in `check_pep8.py` if you create any packages.