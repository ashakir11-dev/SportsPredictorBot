from abc import ABC, abstractmethod
import time
import Database

class Team:

    pass_off = None
    pass_def = None
    run_off = None
    run_def = None
    off_tdspg = None
    win_pct = None
    fg_pct = None
    three_pct = None
    off_ppg = None
    rpg = None
    ft_pct = None
    fta = None

    @abstractmethod
    def get_stats(self):
        pass


class NFL_Team(Team):

    def __init__(self, team_name):
        self.team_name = team_name



    def get_stats(self, connection, team_name):
        # get passing offense stats
        query = "Select * FROM prediction1.2021_team_offense_passing WHERE Team='" + team_name +"'"
        results = Database.read_single_query(connection, query)
        NFL_Team.pass_off = (results[5])/17
        # get rushing offense stats
        NFL_Team.run_off = (results[2])/17
        # get offensive TDs per game
        NFL_Team.off_tdspg = (results[3])/17
        # get passing defense stats
        NFL_Team.pass_def = (results[3])/17
        # get rushing defense stats
        NFL_Team.run_def = (results[2])/17

        return Team


class NBA_Team(Team):

    def __init__(self, team_name):
        self.team_name = team_name

    def get_stats(self, connection, team_name):
        query = "Select * FROM prediction1.nba_team_stats WHERE Team='" + team_name + "' AND Season='2020-21'"
        results = Database.read_single_query(connection, query)
        NBA_Team.win_pct = results[5]
        NBA_Team.fg_pct = results[10]
        NBA_Team.three_pct = results[13]
        NBA_Team.off_ppg = results[7]
        NBA_Team.rpg = results[19]
        NBA_Team.ft_pct = results[16]
        NBA_Team.fta = results[15]

        return Team