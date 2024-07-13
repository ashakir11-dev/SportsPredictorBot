from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import time
import mysql.connector
import re

#Could be a map, but python is dumb
#Handle 2 Los Angeles/NY Teams
teams_loc = ["Arizona", "Atlanta", "Carolina", "Chicago", "Dallas", "Detroit", "Greenbay", "Los Angeles", "Minnesota", "New Orleans", "New York", "Philadelphia", "San Francisco", "Seattle", "Tampa Bay", "Washington", "Baltimore", "Buffalo", "Cincinnati", "Cleveland", "Denver", "Houston", "Indianapolis", "Jacksonville", "Kansas City", "Las Vegas", "Los Angeles", "Miami", "New England", "New York", "Pittsburgh", "Tennessee"]
teams_name = ["Cardinals", "Falcons", "Panthers", "Bears", "Cowboys", "Lions", "Packers", "Rams", "Vikings", "Saints", "Giants", "Eagles", "49ers", "Seahawks", "Buccaneers", "FootballTeam", "Ravens", "Bills", "Bengals", "Browns", "Broncos", "Texans", "Colts", "Jaguars", "Chiefs", "Raiders", "Chargers", "Dolphins", "Patriots", "Jets", "Steelers", "Titans"]
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def week_url(current_date):
    if int(current_date) in range(20221123,20221130,1):
        url_week = 12
    elif int(current_date) in range(20221130,20221207,1):
        url_week = 13
    elif int(current_date) in range(20221207,20221214,1):
        url_week = 14
    elif int(current_date) in range(20221214,20221221,1):
        url_week = 15
    elif int(current_date) in range(20221221,20221228,1):
        url_week = 16
    elif int(current_date) in range(20221218,20231204,1):
        url_week = 17
    return url_week

def sports_schedule(date):
    # getting the url
    # determining the week number based on the date
    week_num = week_url(date.strftime("%Y%m%d"))
    url = (f"https://www.espn.com/nfl/schedule/_/week/{week_num}/year/2022/seasontype/2/date/{date}")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # looking for the correct tags in the html
    # main tag
    schedule_divs = soup.find_all("div", {"class": "ScheduleTables"})
    # current days schedule
    results = []
    for item in schedule_divs:
        schedule_body = item.find('tbody', {'class': 'Table__TBODY'})
    # each row in the schedule
        rows = schedule_body.find_all('tr', {'class': 'Table__TR'})
        for r in rows:
        # parsing through each row
            rst = parse_one_row(r)
                # storing the information into the results list
            if rst["home_team"] == "New York" or rst["home_team"] == "Los Angeles" or rst["away_team"] == "New York" or rst["away_team"] == "Los Angeles":
                print("skipping")
            else:
                # searching and printing the day.
                search_day = item.find('div',{'class':'Table__Title'}).text
                print(search_day)
                splitter = re.split('[,]', search_day)
                print(splitter)
                rst['date'] = splitter[1]
                results.append(rst)
    
    return results
# parsing through the rows
def parse_one_row(row):
    # declaring result as dictionary
    result = {}
    # enumerate to iterate the counter and the columns
    for idx, col in enumerate(row.find_all('td')):
        # removing @ and blank spaces
        #found = col.find("saints")
        text = col.text.replace('@', '').strip()
        # setting first column as away team
        if idx == 0:
            result['away_team'] = text
            # setting first column as home team
        elif idx == 1:
            result['home_team'] = text
        # setting first column as game time
        elif idx == 2:
            result['time'] = text
        
        result['date'] = "N/A"

    print(result)
    return result

# formating the result print
# def print_results(results):
#     # enumerate to iterate the counter and the game(results)
#     for idx, game in enumerate(results):
#         print(f'Game {idx+1}: {game["away_team"]} vs {game["home_team"]}, at {game["time"]}')

if __name__ == '__main__':
    #finding the schedule for the next 6 days.
        mydb = mysql.connector.connect(
        host="sports.c5m0c71z2qos.us-east-1.rds.amazonaws.com",
        user="scraper",
        password="scraperpassword",
        database="prediction1"
    )
        # try is to test for errors
        try:
            # passing in a current date to get the schedule. ( +timedelta(i) is to loop to next day)
            results = sports_schedule(datetime.now()+timedelta())
        
        # directly below (commented out) is to query a specific date: 
        # query_sports_schedule(datetime(2022, 9, 5))

        # except is for handling the errors
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print('request time out')
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print('too many redirect')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print('request unknown error')
        # printing the results
        # print_results(results)
        
        my_date = timedelta()
        print(my_date)
        for game in results:
            #print(game)
            home_team = game["home_team"]
            away_team = game["away_team"]

            date_splitter = re.split('[ ]', game["date"])
            game_day = date_splitter[2]
            game_month = date_splitter[1] 
            #print(game_day, game_month)
            for i in range(0, len(month_list)):
                if game_month == month_list[i]:
                    game_month = (i+1)
            #print(game_month)

            for i in range(0, len(teams_loc)):
                if home_team == str(teams_loc[i]):
                    home_team = teams_name[i]
                if away_team == str(teams_loc[i]):
                    away_team = teams_name[i]
            #print(home_team)
            #print(f'Game {idx+1}: {game["away_team"]} vs {game["home_team"]}, at {game["time"]}')
            mycursor = mydb.cursor()
            mycursor.execute("SELECT TEAM FROM prediction1.2021_team_defense_downs where Locate(%s, TEAM) !=0", (str(home_team), ))
            myresult = mycursor.fetchone()
            #mycursor.close()

            if myresult != None:
                team1id = myresult[0]
            else:
                team1id = str(home_team)

            mycursor = mydb.cursor()
            mycursor.execute("SELECT TEAM FROM prediction1.2021_team_defense_downs where Locate(%s, TEAM) !=0", (str(away_team), ))
            myresult2 = mycursor.fetchone()
            #mycursor.close()

            if myresult2 != None:
                team2id = myresult2[0]
            else:
                team2id = str(away_team)

            print(team1id, team2id)

            my_date = datetime(year=2022, month=int(game_month), day=int(game_day))
            print(my_date)
            found = game["time"].find(":")
            splitter = re.split('[:]', game["time"])
            if splitter[0] != 'LIVE' and found != -1: #If live, or already happened, skip
                #skip
                splitter2 = re.split('[ ]',splitter[1])
                print(splitter[0], splitter[1], splitter2[0])
                if "PM" in game["time"]:
                    #print(splitter[0])
                    final_time = my_date + timedelta(hours=12+int(splitter[0]), minutes = int(splitter2[0]))
                else:
                    #print(splitter[1])
                    final_time = my_date + timedelta(hours=int(splitter[0]), minutes = int(splitter2[0]))
                #print(today_date)
                print(final_time)
                sql = "INSERT INTO fullgametable (sportid, team1id, team2id, datetime) VALUES (3, %s, %s, %s)" #May need to remove duplicates or process duplciates
                val = (team1id, team2id, final_time)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
            else:
                print("Skipping game")
            #time.sleep(3)
            #sql = "INSERT INTO gamesschedule (completed, ) VALUES (2, %s, %s, %s)"
            #val = (team1id, team2id, hometeam)
            #mycursor.execute(sql, val)
            #mydb.commit()
