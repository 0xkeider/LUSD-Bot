import config
import requests
import json
import logging
import discord
from discord.ext import commands, tasks

CURVE_API_URL = 'https://api.curve.fi/api/getPools/ethereum/main'
TOKEN = config.DISCORD_API_KEY

# Logging Config
logging.basicConfig(
    level=logging.INFO,
    format='{asctime} [{levelname:<8}] {message}',
    datefmt="%d %b %Y %H:%M:%S %z",
    style='{',
    filemode='w'
)

def call_pool():
    logging.info('Requesting Curve API...')
    response = requests.get(
        CURVE_API_URL,
        timeout=5
    )
    logging.info('Request Complete')
    return response.json()

def getusdPrice(curve_data, pool_id, token):
    pool_data = curve_data['data']['poolData'][pool_id]
    for coins in pool_data['coins']:
        coin_data = coins
        if coin_data['symbol'] == token:
            usdPrice = coin_data['usdPrice']
            return usdPrice

def main():

    # Broadcast version number
    logging.info('Script Built on 10/9/2022')

    # Connect to Discord
    client = discord.Client()
    @client.event
    async def on_ready():
        if not loop.is_running():
            loop.start()
        logging.info('Logged in as {0.user}'.format(client))

    # Update activity every minute
    @tasks.loop(seconds=60)
    async def loop():
        try:
            json_data = call_pool()
            LUSD_price = getusdPrice(json_data, 33, 'LUSD') * 0.9996 # curve fee of 0.040%

            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='curve.fi'))

            total_guilds = 0
            for guild in client.guilds:
                nickname = f"${round(LUSD_price, 4)}"
                await client.get_guild(guild.id).me.edit(nick=nickname)
                total_guilds += 1
            logging.info(f"Updating activity, watching {total_guilds} guild(s)")
        except:
            logging.error("Error occurred, loop not executed")

    client.run(TOKEN)

if __name__ == "__main__":
    main()
