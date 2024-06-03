A Discord bot which records chessguessr results to chessguessr.db.

```
Chessguessr #713 3/5

🟩⬜⬜⬜⬜
🟩🟩⬜⬜🇺🇦
🟩🟩🟩🟩🟩

https://chessguessr.com/

# Will output
> {"user": "user1", "games_played": 1, "win_percent": 1.0}
```

# Install

Read the "Getting started" section to learn how to make your own Discord bot: https://discordpy.readthedocs.io/en/stable/#getting-started

Create a .env with the DISCORD_TOKEN var.

```
DISCORD_TOKEN=your_token
```

Run bot.py to start the bot.

# Commands

`$leaderboard`: prints a leaderboard. e.g.

```
{"user1": 1, "user2": 1}
```