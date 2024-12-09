import discord
import os
from dotenv import load_dotenv
import logging
import asyncpraw
import randoms

#load .env variables
load_dotenv()

#enable logging at INFO level
logger= logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler= logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

#create bot and get it ready on startup
bot= discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} ready')
    await bot.sync_commands()

#commands for bot
@bot.slash_command(name="hello", description="say hi to Jeff")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey, "+ randoms.aliase()+ "!")

#run the bot
bot.run(os.getenv('TOKEN'))