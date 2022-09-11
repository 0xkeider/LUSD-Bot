# LUSD Price Bot

## Initial Setup

1. Requires a Discord Bot Token to run. Head over to the [Discord Developer Portal](https://discord.com/developers/applications/), and click on New Application to generate a token.

2. Create a file named `config.py` and paste this line with your token.
```
DISCORD_API_KEY = "INSERT TOKEN HERE"
```

## Run

Run `main.py`.

## Configuration

The bot updates the price every 60 seconds by default. To change this, modify the interval
```
@tasks.loop(seconds=60)
```
You can use the properties `seconds`, `minutes` and `hours`.