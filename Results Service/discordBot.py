# bot.py
import os
import random
import pymysql
import discord
from dotenv import load_dotenv
from discord.ext import commands

db = pymysql.connect(host = 'sports.c5m0c71z2qos.us-east-1.rds.amazonaws.com' , port = 3306, user = 'robot', password= 'robotpassword')
cursor = db.cursor()

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()

#client = discord.Client(intents=intents)

# 2
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='test')
async def testing(ctx):
    test_quote = "I'm active!"

    response = test_quote
    await ctx.send(response)

@bot.command(name='info')
async def helper(ctx):

    response = "Here are some commands you can use! \n!test - This will test the bot to ensure it is responding and active. \n!predictions - See the predicted winner of your team's next game \n!NBAstats - See the stats of any NBA team and season \n!NFLstats - See stats from an NFL team of your choice \n!accuracy - See the accuracy of the prediction algorithm"
    await ctx.send(response)

@bot.command(name='predictions')
async def prediction(ctx):
    await ctx.send(f"What team's predictions would you like to see?")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)

    query = '''USE prediction1'''
    cursor.execute(query)
    query = """SELECT team1id,team2id,predicted_winner,game_date FROM predictions WHERE team1id = """ + """'""" + msg.content + """';"""
    cursor.execute(query)
    #predictions = cursor.fetchall()[0]
    #response = predictions[0] + ' vs. ' + predictions[1] + ' --- Winner: ' + predictions[2] + ' (Game Date: ' + str(predictions[3]) + ')'

    predictions = cursor.fetchall()
    response = ''

    for game in predictions:
        response = response + '\n' + game[0] + ' vs. ' + game[1] + ' --- Winner: ' + game[2] + ' (Game Date: ' + str(game[3]) + ')'

    print(predictions)

    try: 
        test = predictions[0]
        pass
    except:
        response = 'Sorry, no predictions have been made for the ' + msg.content


    await ctx.send(response)

@bot.command(name="NBAstats")
async def command(ctx):
    await ctx.send(f"Type the full name of the NBA team to see their stats i.e. Boston Celtics")

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)

    #print(msg.content)
    query = '''USE prediction1;'''
    cursor.execute(query)
    
    await ctx.send(f"What season would you like to see? i.e 'YYYY-YY'")
    msg2 = await bot.wait_for("message", check=check)

    query = """SELECT TEAM,GP,W,L,PTS,SEASON FROM nba_team_stats WHERE TEAM = """ + """'""" + msg.content + """' and SEASON = '""" + msg2.content + """';"""

    cursor.execute(query)
    response = cursor.fetchall()[0]
    print(response)
    respond = '' + response[0] + ' Stats (' + response[5] + ')\nGames Played: ' + str(response[1]) + '\nWins: ' + str(response[2]) + '\nLosses: ' + str(response[3]) + '\nAvg Points: ' + str(response[4]) 

    await ctx.send(respond)

@bot.command(name="accuracy")
async def command(ctx):

    query = '''USE prediction1;'''
    cursor.execute(query)
    query = '''SELECT * FROM accuracy;'''
    cursor.execute(query)
    response = cursor.fetchall()[0]

    respond = 'Games Analyzed: ' + str(response[1]) + '\nAccuracy: ' + str(response[0]) + '%'

    await ctx.send(respond)

@bot.command(name="NFLstats")
async def command(ctx):

    await ctx.send(f"What NFL team's stats would you like to see? i.e. Chiefs")

    query = '''USE prediction1;'''
    cursor.execute(query)
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    team = msg.content

    #await ctx.send(f"Would you like to see stats for Offense or Defense?")
    #msg2 = await bot.wait_for("message", check=check)
    #msg2 = msg2.content

    #await ctx.send(f"Which stats would you like to see? \nPassing \nReceiving \nRushing")
    #stat = await bot.wait_for("message", check=check)
    #stat = stat.content

    #if msg2.lower() == "offense":
    #    if stat.lower() == "passing":
    #        query = """SELECT Att,Cmp,TD,Rate FROM 2021_team_offense_passing WHERE Team = '""" + team + """';"""
    #        #query = """SELECT Att,Cmp,Pass Yds,TD,INT,Rate FROM 2021_team_offense_passing WHERE Team == '""" + team + """';"""

    #        cursor.execute(query)

    #    elif stat.lower() == "receiving":
    #        query = """SELECT Rec,Yds,TD FROM 2021_team_offense_receiving WHERE Team = '""" + team + """';"""
    #        cursor.execute(query)

    #    elif stat.lower() == "rushing":
    #        query = """SELECT Att,YPC,TD FROM 2021_team_offense_rushing WHERE Team = '""" + team + """';"""
    #        cursor.execute(query)
            
    #    num_fields = len(cursor.description)
    #    field_names = [i[0] for i in cursor.description]     

    #    respond = "Team: " + team
    #    x = 0
    #    response = cursor.fetchall()[0]
    #    print(response)
    #    for i in response:
    #        respond = respond + "\n" + field_names[x] + ": " + str(i)
    #        x+=1

    respond = team + ' 2021 Offense Stats'         
    query = """SELECT Att,CMP,TD,Rate FROM 2021_team_offense_passing WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]
    
    respond = respond + '\nPass Attempts: ' + str(data[0]) + '\nCompletions: ' + str(data[1]) + '\nPassing Touchdowns: ' + str(data[2]) + '\nRate: ' + str(data[3])

    query = """SELECT Rec,Yds,TD FROM 2021_team_offense_receiving WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]

    respond = respond + '\nReceiving Yards: ' + str(data[1])

    query = """SELECT Att,YPC,TD FROM 2021_team_offense_rushing WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]

    respond = respond + '\nRushing Attempts: ' + str(data[0]) + '\nYards per Carry: ' + str(data[1]) + '\nRushing TDs: ' + str(data[2])

    #DEFENSE
    respond = respond + '\n\n' + team + ' 2021 Defense Stats'         
    query = """SELECT Att,CMP,TD,Rate FROM 2021_team_defense_passing WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]
    
    respond = respond + '\nPass Attempts: ' + str(data[0]) + '\nCompletions Allowed: ' + str(data[1]) + '\nPassing Touchdowns Allowed: ' + str(data[2]) + '\nRate: ' + str(data[3])

    query = """SELECT Rec,Yds,TD FROM 2021_team_defense_receiving WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]

    respond = respond + '\nReceiving Yards Allowed: ' + str(data[1])

    query = """SELECT Att,YPC,TD FROM 2021_team_defense_rushing WHERE Team = '""" + team + """';"""
    cursor.execute(query)
    data = cursor.fetchall()[0]

    respond = respond + '\nRushing Attempts: ' + str(data[0]) + '\nYards per Carry Allowed: ' + str(data[1]) + '\nRushing TDs Allowed: ' + str(data[2])
    #if msg2.lower() == "defense":
    #    if stat.lower() == "passing":
    #        query = """SELECT Att,Cmp,TD,Rate FROM 2021_team_defense_passing WHERE Team = '""" + team + """';"""
            #query = """SELECT Att,Cmp,Pass Yds,TD,INT,Rate FROM 2021_team_offense_passing WHERE Team == '""" + team + """';"""

    #        cursor.execute(query)

    #    elif stat.lower() == "receiving":
    #        query = """SELECT Rec,Yds,TD FROM 2021_team_defense_receiving WHERE Team = '""" + team + """';"""
    #        cursor.execute(query)

    #    elif stat.lower() == "rushing":
    #        query = """SELECT Att,Rush Yds,YPC,TD FROM 2021_team_defense_rushing WHERE Team = '""" + team + """';"""
    #        cursor.execute(query)
            
    #    num_fields = len(cursor.description)
    #    field_names = [i[0] for i in cursor.description]     

    #    respond = "Team: " + team
    #    x = 0
    #    response = cursor.fetchall()[0]
    #    print(response)
    #    for i in response:
    #        respond = respond + "\n" + field_names[x] + ": " + str(i)
    #        x+=1  


    await ctx.send(respond)

        

bot.run(TOKEN)