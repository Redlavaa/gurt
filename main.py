import discord
from discord.ext import commands
from gamelist import list
from getonline import getonline
from getplayer import get
from getid import getuserid
from getlatestplayer import getlatest
from getguild import getguild

TOKEN = "MTQ2Nzk5OTA1ODkzMjI3MzE2NA.GZWU91.-Hmj9EJ7cs6GpmfgnJW2RNE_Rcw-5c7Hebs0uY"
GUILD_ID = 1468373912931926142

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="gamelist", description="Replies with gamelist")
async def gamelist(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        name, id, execution_time, embed = await list()

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="profile", description="Replies with profile info")
async def profile(interaction: discord.Interaction, id: str):

    await interaction.response.defer()

    try:
        name, networth, icon, execution_time, embed= await get(id)

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
        name, id, icon, execution_time, embed = await getlatest()

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="playercount", description="Replies with total online players")
async def playercount(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        embed, execution_time = await getonline()

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {type(e).__name__} - {e}")

@bot.tree.command(name="guild", description="Gives Guild Information")
async def profile(interaction: discord.Interaction, id: str):

    await interaction.response.defer()

    try:
        embed = await getguild(id)

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
