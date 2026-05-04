import discord
import os
from dotenv import load_dotenv
from typing import Literal
from discord.ext import commands
from discord import app_commands
from src.api.store.getitem import getitem
from src.api.game.gamelist import list
from src.api.user.getonline import getonline
from src.api.user.getplayer import get
from src.api.user.getid import getuserid
from src.api.user.getlatestplayer import getlatest
from src.api.guild.getguild import getguild
from src.api.rankings.getleaderboard import getrankings
from src.api.misc.download import downloadasset
from src.api.game.getgame import getgame

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="gamelist", description="Replies with gamelist")
async def gamelist(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        embed = await list()

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="profile", description="Replies with profile info")
async def profile(interaction: discord.Interaction, id: str):

    await interaction.response.defer()

    try:
        embed, execution_time = await get(id)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="fetchid", description="Replies with your user id")
async def fetchid(interaction: discord.Interaction, username: str):

    await interaction.response.defer()

    try:
        id, execution_time = await getuserid(username)

        await interaction.followup.send(f"ID: {id}, Execution Time: {execution_time}ms")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="latestplayer", description="Replies with the latest player")
async def latestplayer(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        embed, execution_time = await getlatest()

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="playercount", description="Replies with total online players")
async def playercount(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        await interaction.followup.send("Currently Broken Cause I dont wanna rewrite this, I will fix it later")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="guild", description="Gives Guild Information")
async def guild(interaction: discord.Interaction, id: str):

    await interaction.response.defer()

    try:
        embed = await getguild(id)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="item", description="Gives Item Information")
async def item(interaction: discord.Interaction, id: str):

    await interaction.response.defer()

    try:
        embed = await getitem(id)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="leaderboard", description="Replies with the leaderboard")
async def leaderboard(interaction: discord.Interaction, category: Literal["networth", "visits", "sales", "xp", "forumposts", "profileviews"], page: int): # ok if im gonna be honest I have no idea how the whole Literal thing works it just works dont question it

    await interaction.response.defer()

    try:
        embed = await getrankings(category, page)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="download", description="Downloads an asset")
async def download(interaction: discord.Interaction, id: int):

    await interaction.response.defer()

    try:
        embed = await downloadasset(id)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="game", description="Gives Game Information")
async def game(interaction: discord.Interaction, id: int):

    await interaction.response.defer()

    try:
        embed, execution_time = await getgame(id)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        await bot.tree.sync()
        print("Slash commands synced")
        await bot.change_presence(activity=discord.Game(name="waiting for a command"))
    except Exception as e:
        print("Sync failed:", type(e).__name__, e)

bot.run(TOKEN)
