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