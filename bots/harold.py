import discord
import query_stuff.queries as queries
from discord.ext import commands
import discord.utils
from random import randint


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

gold = 'BBA53D'
embed_color = int(gold, 16)

@bot.event
async def on_ready():
    print("Encoders have been reset")


@bot.command(pass_context=True, aliases=['topTeam', 'bt'], help='Command format: $bestTeam <region>. If <region> is left blank, the default region is All.', description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region', brief="Gets the best team from ftcscout.org")
async def bestTeam(ctx, region='All'):
    data, success = queries.getBestTeam(region)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
        ctx.send(embed=embed)
        return
    team_info, team_qstats, team_events = data

    

@bot.command(pass_context=True, aliases=['qstats'])
async def quickstats(ctx, number):
    ...
@bot.command(pass_context=True, aliases=['stats'])
async def teamstats(ctx, number):
    ...
@bot.command(pass_context=True, aliases=['events'])
async def teamevents(ctx, number):
    ...
@bot.command(pass_cntext=True, aliases=['info'])
async def teaminfo(ctx, number):
    ...
@bot.command(pass_context=True, aliases=['8'])
async def eightball(ctx):
    ...
@bot.command(pass_context=True)
async def dice(ctx, sides=6):
    roll = randint(0, sides) #i don't remeber how discord emoticons work so fix this later
    diceembed=discord.Embed(title=":game_die:", description=f"You rolled a **{roll}**")
    ctx.send(embed=diceembed)
 

