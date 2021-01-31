def fix_locale(team_locale: str) -> str:
    """Expand and fix place names from the values in JSON"""
    if 'NY' in team_locale:
        team_locale = 'New York'
    elif 'Montr' in team_locale:
        team_locale = 'Montreal'
    return team_locale.title()


def fix_name(team_name: str) -> str:
    """Expand team names from the values in JSON"""
    if 'wings' in team_name:
        team_name = 'Red Wings'
    elif 'jackets' in team_name:
        team_name = 'Blue Jackets'
    elif 'leafs' in team_name:
        team_name = 'Maple Leafs'
    elif 'knights' in team_name:
        team_name = 'Golden Knights'
    return team_name.title()


def playoff_series_info(rnd: str, srs: str) -> str:
    """Get the title of current round/series"""
    title = {
        "01": {
            "1": "First Round: East #1 vs. Wildcard #2",
            "2": "First Round: Atlantic #2 vs. Atlantic #3",
            "3": "First Round: East #2 vs. Wildcard #1",
            "4": "First Round: Metropolitan #2 vs. Metropolitan #2",
            "5": "First Round: West #1 vs. Wildcard #2",
            "6": "First Round: Central #2 vs. Central #3",
            "7": "First Round: West #2 vs. Wildcard #1",
            "8": "First Round: Pacific #2 vs. Pacific #3",
        },
        "02": {
            "1": "Eastern Conference Semifinals",
            "2": "Eastern Conference Semifinals",
            "3": "Western Conference Semifinals",
            "4": "Western Conference Semifinals",
        },
        "03": {
            "1": "Eastern Conference Finals",
            "2": "Western Conference Finals",
        },
        "04": {
            "1": "Stanley Cup Final"
        }
    }
    return title[rnd][srs]
