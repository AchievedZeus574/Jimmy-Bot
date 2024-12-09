import discord
import os
from dotenv import load_dotenv
import logging
import asyncpraw
import randoms #used for other functions 
from random import choice
import asyncio
import configparser

#load .env variables
load_dotenv()

#load config file
config= configparser.ConfigParser()
config.read('config.ini')

#enable logging at INFO level
logger= logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler= logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

#grab information for async praw
reddit= asyncpraw.Reddit(
    client_id= os.getenv('REDDIT_CLIENT_ID'),
    client_secret= os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent= os.getenv('REDDIT_USER_AGENT')
)

#grab random image from reddit specified by command
async def post_grab(sub):
    try:
        subreddit= await reddit.subreddit(sub)
        posts= [
            post async for post in subreddit.hot(limit=25)
            if post.url.endswith(('.jpg', '.png', '.jpeg'))
        ]
        if posts:
            random_post= choice(posts)
            return random_post.url
        else:
            return f"No image posts found in r/{sub}."
    except Exception as e:
        return f"An error occured {str(e)}"


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

@bot.slash_command(name="1line", description="Spit out a random one liner")
async def one_liner(ctx: discord.ApplicationContext):
    await ctx.respond(randoms.one_line())

@bot.slash_command(name="4liase", description="Give a random aliase")
async def four_liase(ctx: discord.ApplicationContext):
    await ctx.respond(randoms.aliase())
@bot.slash_command(name="random", description="Grab random image from best of a SubReddit of your choosing")
async def random(ctx, subreddit: discord.Option(discord.SlashCommandOptionType.string)):
    url= await post_grab(subreddit)
    await ctx.respond(url)

@bot.slash_command(name="triggerpost", description="Trigger posting of CotD")
async def CotDM(ctx):
    await ctx.defer()
    post= await post_grab()
    await ctx.respond(f'Post failed')

#run the bot
bot.run(os.getenv('TOKEN'))