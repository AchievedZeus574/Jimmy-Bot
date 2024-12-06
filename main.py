import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import random
import praw
from datetime import datetime, time as dtime

# Load environment variables
load_dotenv()

# Reddit Configuration
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Discord Configuration
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))  # Channel ID from .env
TARGET_GUILD_ID = int(os.getenv("TARGET_GUILD_ID"))      # Server ID from .env
POST_TIME = dtime(
    hour=int(os.getenv("POST_HOUR", 12)), 
    minute=int(os.getenv("POST_MINUTE", 0))
)  # Scheduled post time (default 12:00 PM)

# Subreddit List - Using environment variable for flexibility
SUBREDDIT_LIST = os.getenv("SUBREDDIT_LIST", "EarthPorn,Art,Memes").split(",")  # Comma-separated list from .env

# Log File
LOG_FILE = "post_log.txt"

# Helper function to log the post with subreddit, post id, and date
def log_post(post_id, date_posted, subreddit_name):
    with open(LOG_FILE, "a") as log:
        log.write(f"Post ID: {post_id}, Subreddit: {subreddit_name}, Date: {date_posted}\n")

# Function to update the starting day number in the .env file
def update_day_number(day_number):
    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for line in lines:
            if line.startswith("START_DAY_NUMBER"):
                file.write(f"START_DAY_NUMBER={day_number}\n")
            else:
                file.write(line)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild=discord.Object(id=TARGET_GUILD_ID))
            self.synced = True
        print(f'Logged in as {self.user}')
        self.schedule_post.start()  # Start the scheduled posting loop

    async def fetch_random_image(self, subreddit_name):
        try:
            subreddit = reddit.subreddit(subreddit_name)
            posts = subreddit.hot(limit=100)
            image_posts = [post for post in posts if post.url.endswith(('.jpg', '.png', '.jpeg'))]

            if image_posts:
                random_post = random.choice(image_posts)
                title = random_post.title
                post_id = random_post.id
                return title, post_id, random_post.url
            else:
                return None, None, f"No image posts found in r/{subreddit_name}."
        except Exception as e:
            return None, None, f"An error occurred: {str(e)}"

    @tasks.loop(minutes=1)
    async def schedule_post(self):
        """Check the time every minute and post at the scheduled time."""
        now = datetime.now().time()
        if now.hour == POST_TIME.hour and now.minute == POST_TIME.minute:
            channel = self.get_channel(TARGET_CHANNEL_ID)
            if channel:
                # Get the starting day number from the .env file
                start_day_number = int(os.getenv("START_DAY_NUMBER", "367"))

                # Select a random subreddit from the list
                subreddit_name = random.choice(SUBREDDIT_LIST)
                title, post_id, image_url = await self.fetch_random_image(subreddit_name)
                if title:
                    post_number = start_day_number  # Use the current starting day number
                    message = f"Cat of the Day {post_number}: {title}\n{image_url}"
                    await channel.send(message)

                    # Log the post ID, subreddit, and date
                    log_post(post_id, datetime.now().strftime("%Y-%m-%d"), subreddit_name)

                    # Update the starting day number for the next post
                    update_day_number(post_number + 1)
                else:
                    await channel.send(image_url)

client = aclient()
tree = discord.app_commands.CommandTree(client)

# Discord Commands
@tree.command(name= "1line")
async def one_line(interaction: discord.Interaction):
    await interaction.response.send_message(randoms.one_line())

@tree.command(name= "4liase")
async def four_liase(interaction: discord.Interaction):
    await interaction.response.send_message(randoms.aliase())

@tree.command(name="thirst", description="You are thirsty boi")
async def thirst(interaction: discord.Interaction, thirsty: int=1):
    await interaction.response.send_message(randoms.thirst(thirsty))

@tree.command(name="hunger", description="You are hungry boi")
async def hunger(interaction: discord.Interaction, hungry: int= 1):
    if (hungry>166):
        await interaction.response.send_message("Max hunger is 166 fatty", ephemeral= True, delete_after=120)
    else:
        await interaction.response.send_message(randoms.hunger(hungry))

@tree.command(name="randomimage", description="Fetch a random image from a subreddit")
async def random_image(interaction: discord.Interaction, subreddit_name: str):
    title, post_id, image_url = await client.fetch_random_image(subreddit_name)
    if title:
        await interaction.response.send_message(f"Cat of the Day: {title}\n{image_url}")
    else:
        await interaction.response.send_message(image_url)

@tree.command(name="triggerpost", description="Manually post a random image to the target channel")
async def trigger_post(interaction: discord.Interaction):
    """Manually trigger a post to the target channel."""
    allowed_users = [608813834492313603]

    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)  # Defer the response
    
    subreddit_name = random.choice(SUBREDDIT_LIST)
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel:
        title, post_id, image_url = await client.fetch_random_image(subreddit_name)
        if title:
            start_day_number = int(os.getenv("START_DAY_NUMBER", "1"))
            post_number = start_day_number
            message = f"Cat of the Day {post_number}: {title}\n{image_url}"
            await channel.send(message)

            log_post(post_id, datetime.now().strftime("%Y-%m-%d"), subreddit_name)
            update_day_number(post_number + 1)

            await interaction.followup.send(f"Successfully posted an image from r/{subreddit_name} to the target channel!", ephemeral=True)
        else:
            await interaction.followup.send(image_url, ephemeral=True)
    else:
        await interaction.followup.send("Target channel not found. Please check the configuration.", ephemeral=True)

# Run the bot
client.run(os.getenv('TOKEN'))
