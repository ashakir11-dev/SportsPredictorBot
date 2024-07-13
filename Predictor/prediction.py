import Team

def get_nba_prediction(Team1, Team2):

    Team1_win_probability = 0
    Team2_win_probability = 0

    # compare win % to give edge to one team or another
    if Team1.win_pct > Team2.win_pct:
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare FG% to give edge to one team or another
    if Team1.fg_pct > Team2.fg_pct:
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare rebounds per game to give edge to one team or another
    if Team1.three_pct > Team2.three_pct:
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare off & def ppg avgs to give edge to one team or another
    if Team1.off_ppg > Team2.off_ppg :
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare rebound avgs to give edge to one team or another
    if Team1.off_ppg > Team2.off_ppg:
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # Give upset boost to underdog (average % of underdogs winning is 32.1%)
    if Team1.win_pct < Team2.win_pct:
        Team1_win_probability = Team1_win_probability * 1.321
    elif Team1.win_pct == Team2.win_pct:
        pass
    else:
        Team2_win_probability = Team2_win_probability * 1.321

    #give home team an advantage (average % of home team wins is 57.6%)
    Team1_win_probability = Team1_win_probability * 1.60

    # Determine winner based off of various factors
    if Team1_win_probability > Team2_win_probability:
        winner = Team1.team_name
    else:
        winner = Team2.team_name

    return winner

def get_nfl_prediction(Team1, Team2):
    Team1_win_probability = 0
    Team2_win_probability = 0

    # compare pass offense vs pass def
    if ((Team1.pass_off + Team2.pass_def) / 2) > ((Team2.pass_off + Team1.pass_def) / 2):
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare run offense vs run def
    if ((Team1.run_off + Team2.run_def) / 2) > ((Team2.run_off + Team1.run_def) / 2):
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # compare average TDs scored
    if Team1.off_tdspg > Team2.off_tdspg:
        Team1_win_probability + 1
    else:
        Team2_win_probability + 1

    # Give upset boost to underdog (average % of underdogs winning is 32.1%)
    if Team1.off_tdspg > Team2.off_tdspg:
        Team1_win_probability = Team1_win_probability * 1.321
    elif Team1.off_tdspg == Team2.off_tdspg:
        pass
    else:
        Team2_win_probability = Team2_win_probability * 1.321

    # give home team an advantage (average % of home team wins is 57.6%)
    Team1_win_probability = Team1_win_probability * 1.576

    # Determine winner based off of various factors
    if Team1_win_probability > Team2_win_probability:
        winner = Team1.team_name
    else:
        winner = Team2.team_name

    return winner