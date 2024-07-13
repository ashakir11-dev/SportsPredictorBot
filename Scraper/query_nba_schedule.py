from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import time
import mysql.connector
import re

# find the playing teams for the specified date
def NBA_url(date):
    # formatting and adding the specified date to the base url to get the latest schedule
    base_url = 'https://www.espn.com/nba/schedule/_/date/'
    url = base_url + date.strftime("%Y%m%d")
    NBA_schedule = sports_schedule(url)
    return NBA_schedule

def sports_schedule(url):
    # getting the url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # looking for the correct tags in the html
    # main tag
    schedule_divs = soup.find_all("div", {"class": "ScheduleTables"})
    # current days schedule
    today_schedule = schedule_divs[0]
    schedule_body = today_schedule.find('tbody', {'class': 'Table__TBODY'})
    # each row in the schedule
    rows = schedule_body.find_all('tr', {'class': 'Table__TR'})
    # searching and printing the day.
    search_day = today_schedule.find('div',{'class':'Table__Title'}).text
    print(search_day)
    
    results = []
    # looping through the rows
    for r in rows:
        # parsing through each row
        rst = parse_one_row(r)
        # storing the information into the results list
        results.append(rst)
    return results

# parsing through the rows
def parse_one_row(row):
    # declaring result as dictionary
    result = {}
    # enumerate to iterate the counter and the columns
    for idx, col in enumerate(row.find_all('td')):
        # removing @ and blank spaces
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
    return result

# formating the result print
def print_results(results):
    # enumerate to iterate the counter and the game(results)
    for idx, game in enumerate(results):
        print(f'Game {idx+1}: {game["away_team"]} vs {game["home_team"]}, at {game["time"]}')

if __name__ == '__main__':
    #finding the schedule for the next 6 days.
    mydb = mysql.connector.connect(
        host="sports.c5m0c71z2qos.us-east-1.rds.amazonaws.com",
        user="scraper",
        password="scraperpassword",
        database="prediction1"
    )
    today_date = datetime.today()
    my_date = datetime(today_date.year, today_date.month, (today_date.day))
    for i in range(6):
        # try is to test for errors
        try:
            # passing in a current date to get the schedule. ( +timedelta(i) is to loop to next day)
            results = NBA_url(datetime.now()+timedelta(i)) 
        
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
        print_results(results)
        for game in results:
            #print(game)
            home_team = game["home_team"]
            away_team = game["away_team"]
            
            if home_team == "LA":
                home_team = "Clippers"
            if away_team == "LA":
                away_team = "Clippers"
            #print(home_team)
            #print(f'Game {idx+1}: {game["away_team"]} vs {game["home_team"]}, at {game["time"]}')
            mycursor = mydb.cursor()
            mycursor.execute("SELECT TEAM FROM prediction1.nba_team_stats where Locate(%s, TEAM) !=0 and SEASON = '2020-21'", (str(home_team), ))
            myresult = mycursor.fetchone()
            #mycursor.close()

            if myresult != None:
                team1id = myresult[0]
            else:
                team1id = str(home_team)

            mycursor = mydb.cursor()
            mycursor.execute("SELECT TEAM FROM prediction1.nba_team_stats where Locate(%s, TEAM) !=0 and SEASON = '2020-21'", (str(away_team), ))
            myresult2 = mycursor.fetchone()
            #mycursor.close()

            if myresult2 != None:
                team2id = myresult2[0]
            else:
                team2id = str(away_team)

            print(team1id, team2id)

            splitter = re.split('[:]', game["time"])
            found = game["time"].find(":")
            print(found)
            if splitter[0]!='LIVE' and found != -1: #If live, or already happened, skip
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
                sql = "INSERT INTO fullgametable (sportid, team1id, team2id, datetime) VALUES (2, %s, %s, %s)" #May need to remove duplicates or process duplciates
                val = (team1id, team2id, final_time)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
        my_date+=timedelta(days=1)
            #time.sleep(3)
            #sql = "INSERT INTO gamesschedule (completed, ) VALUES (2, %s, %s, %s)"
            #val = (team1id, team2id, hometeam)
            #mycursor.execute(sql, val)
            #mydb.commit()
