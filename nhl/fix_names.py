def fix_name(team_name: str) -> str:
    """Expand some team names from the values in JSON.

    Some of the names for NHL teams used in the API JSON are incorrect.
    In the sense that they omit certain words of the team name. This function fixes that inconsistency. 

    Args:
        team_name (str): Shortened name of the team

    Returns:
        str: Expanded name of the team (without city)
    """
    if 'wings' in team_name:
        team_name = 'Red Wings'
    elif 'jackets' in team_name:
        team_name = 'Blue Jackets'
    elif 'leafs' in team_name:
        team_name = 'Maple Leafs'
    elif 'knights' in team_name:
        team_name = 'Golden Knights'
    return team_name.title()
