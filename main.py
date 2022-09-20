import requests
import json
import logging

import discord
from discord.ext import commands, tasks
from millify import millify

import config

CURVE_API_URL     = 'https://api.curve.fi/api/getPools/ethereum/main'
DEFILLAMA_API_URL = 'https://stablecoins.llama.fi/stablecoins?includePrices=true'
TOKEN             = config.DISCORD_API_KEY

# Logging Config
logging.basicConfig(
    level=logging.INFO,
    format='{asctime} [{levelname:<8}] {message}',
    datefmt="%d %b %Y %H:%M:%S %z",
    style='{',
    filemode='w'
)

def call_API(api_name, API_URL):
    logging.info(f"Requesting {api_name} API...")
    response = requests.get(
        API_URL,
        timeout=5
    )
    logging.info('Request Complete')
    return response.json()

def get_usd_price(curve_data, pool_id, token):
    pool_data = curve_data['data']['poolData'][pool_id]
    for coins in pool_data['coins']:
        coin_data = coins
        if coin_data['symbol'] == token:
            usdPrice = coin_data['usdPrice']
            return usdPrice

def get_circulating(json_data, stablecoin_id, token):
    stablecoin_data = json_data['peggedAssets'][stablecoin_id]
    if stablecoin_data['symbol'] == token:
        circulating_supply = stablecoin_data['circulating']['peggedUSD']
        return circulating_supply

def main():

    # Broadcast version number
    logging.info('Script Built on 20/9/2022')

    # Connect to Discord
    client = discord.Client(intents=discord.Intents.default())
    @client.event
    async def on_ready():
        if not loop.is_running():
            loop.start()
        logging.info('Logged in as {0.user}'.format(client))

    # Update activity every minute
    @tasks.loop(seconds=60)
    async def loop():
        try:
            curve_json = call_API('Curve', CURVE_API_URL)
            defillama_json = call_API('DefiLlama', DEFILLAMA_API_URL)
            LUSD_price = get_usd_price(curve_json, 33, 'LUSD')
            LUSD_circulating = get_circulating(defillama_json, 7, 'LUSD')

            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{millify(LUSD_circulating)} circulating"))

            # Update nickname in every connected guild
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
