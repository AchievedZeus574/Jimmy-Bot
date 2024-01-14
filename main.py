import discord
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
    await interaction.response.send_message(randoms.thirst(thirsty))

@tree.command(name="hunger", description="You are hungry boi")
async def hunger(interaction: discord.Interaction, hungry: int= 1):
    if (hungry>166):
        await interaction.response.send_message("Max hunger is 166 fatty", ephemeral= True, delete_after=120)
    else:
        await interaction.response.send_message(randoms.hunger(hungry))


client.run(os.getenv('TOKEN')) # run the bot with the token
