import discord
from discord import commands
from discord import app_commands
import os # default module
from dotenv import load_dotenv
import randoms

load_dotenv() # load all the variables from the env file

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents= discord.Intents.default())
        self.synced= False
    
    async def on_ready(self):
        if not self.synced:
            await tree.sync()
            self.sycned= True
        print(f'Logged in as {self.user}.')

client= aclient()
tree= app_commands.CommandTree(client)

@tree.command(name= "1line")
async def one_line(interaction: discord.Interaction):
    await interaction.response.send_message(randoms.one_line())

@tree.command(name= "4liase")
async def four_liase(interaction: discord.Interaction):
    await interaction.response.send_message(randoms.aliase())

@tree.command(name="thirst", description="You are thirsty boi")
async def thirst(interaction: discord.Interaction, thirsty: int=1):
    thirmst= ":droplet:"
    for i in range (thirsty-1):
        thirmst= thirmst+ " :droplet:"
    await interaction.response.send_message(thirmst)

@tree.command(name="hunger", description="You are hungry boi")
async def hunger(interaction: discord.Interaction, hungry: int= 1):
    hung= ":hamburger:"
    for i in range (hungry-1):
        hung= hung+ " :hamburger:"
    await interaction.response.send_message(hung)


client.run(os.getenv('TOKEN')) # run the bot with the token
