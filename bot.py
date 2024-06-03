import datetime
from dotenv import load_dotenv
import os
import discord
import json
from peewee import Model, SqliteDatabase, CharField, IntegerField, DateTimeField

db = SqliteDatabase('chessguessr.db')
class GameResult(Model):
    index = IntegerField()
    attempt_count = IntegerField()
    attempt_limit = IntegerField()
    win = IntegerField()
    user = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()
db.create_tables([GameResult])

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
green_square = '🟩'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Chessguessr'):
        parsed = parse_message(message)
        game_result = GameResult(
            index=parsed['index'],
            attempt_count=parsed['attempt_count'],
            attempt_limit=parsed['attempt_limit'],
            win=parsed['win'],
            user=parsed['user']
        )
        game_result.save()
        user_results = GameResult.select().where(GameResult.user == parsed['user'])
        games_played = user_results.count()
        win_percent = user_results.where(GameResult.win == 1).count() / games_played
        await message.channel.send(json.dumps({
            'user': parsed['user'],
            'games_played': games_played,
            'win_percent': win_percent
        }))

    if message.content.startswith("$leaderboard"):
        user_results = GameResult.select().where(GameResult.win == 1)
        leaderboard = {}
        for result in user_results:
            if result.user in leaderboard:
                leaderboard[result.user] += 1
            else:
                leaderboard[result.user] = 1
        sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
        await message.channel.send(json.dumps(sorted_leaderboard))

def parse_message(message):
    # Chessguessr #713 1/5
    # 
    # :green_square::green_square::green_square::green_square::green_square:
    content = message.content

    # Parse the first line
    first_line = content.split('\n\n')[0]
    first_line_split = first_line.split(' ')
    index = first_line_split[1].replace('#', '')
    attempt_count = first_line_split[2].split('/')[0]
    attempt_limit = first_line_split[2].split('/')[1]

    # Parse the board
    win = False
    board = content.split('\n\n')[1]
    for line in board.split('\n'):
        print(line)
        if line == green_square * 5:
            win = True

    return {
        'index': index,
        'attempt_count': attempt_count,
        'attempt_limit': attempt_limit,
        'win': win,
        'user': message.author.name,
    }


client.run(os.getenv('DISCORD_TOKEN'))
