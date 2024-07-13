import Database
import Team
import time
import prediction
from datetime import datetime

if __name__ == '__main__':

    # Database information
    host = 'sports.c5m0c71z2qos.us-east-1.rds.amazonaws.com'
    user = 'predictor'
    passwd = 'predictorpassword'

    connection = Database.create_server_connection(host, user, passwd)

    # query the database to get the current week's games
    query = "SELECT * FROM prediction1.fullgametable"

    results = Database.read_all_query(connection, query)
    for row in results:
        if row[1] == 3:
            team1 = Team.NFL_Team(row[2])
            team2 = Team.NFL_Team(row[3])
            team1.get_stats(connection, team1.team_name)
            team2.get_stats(connection, team2.team_name)

            winner = prediction.get_nfl_prediction(team1, team2)

            date = row[4]#.strftime("%m-%d-%Y, %H:%M:%S")
            insert_query = \
                "VALUES (3, '" + team1.team_name + "', '" + team2.team_name + "', '" + winner + "', '" + str(date) + "')"

            Database.insert_query(connection, insert_query)
            print(winner)
        if row[1] == 2:
            team1 = Team.NBA_Team(row[2])
            team2 = Team.NBA_Team(row[3])
            team1.get_stats(connection, team1.team_name)
            team2.get_stats(connection, team2.team_name)
            winner = prediction.get_nba_prediction(team1, team2)
            date = row[4]#.strftime("%m-%d-%Y, %H:%M:%S")
            insert_query = \
                "VALUES (2, '" + team1.team_name + "', '" + team2.team_name + "', '" + winner + "', '" + str(date) + "')"

            Database.insert_query(connection, insert_query)

            print(winner)
            #print(isinstance(row[5], float))





    Database.end_server_connection(connection)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
