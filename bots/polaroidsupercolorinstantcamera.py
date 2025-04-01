import discord
from discord.ext import commands
import discord.utils
from typing import Any
import re

command_prefix = "polaroid "
activity = discord.Game(name="with colors")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity)
        
def currentRoleName(hexcode: str) -> str:
    return f"sc.{hexcode}" #never underestimate my laziness      
        
def isValidHex(hexcode) -> bool:
    if not isinstance(hexcode, str):  
        return False
        
    return bool(re.fullmatch(r"[0-9A-Fa-f]{6}", hexcode))

def getName(user) -> str:
    return user.nick if user.nick else user.display_name

def getUsers(guild, name: str) -> list:
    matches = [member for member in guild.members if member.display_name == name]
    return matches

def findSupercolorRole(user):
    for role in user.roles:
        if role.name.startswith("sc."):
            return role
            
    return None
            
def filterUsers(users: list) -> list:
    filtered_users = []
    
    for user in users:
        if findSupercolorRole(user):
            filtered_users.append(user)
            
    return filtered_users

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel #if message sent is the same channel & author as the original message


async def getInputOfType(func, ctx):
    while True:
        try:
            msg = await bot.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            ctx.send("Enter a number.")
            continue

async def removeSupercolor(ctx):
    user = ctx.message.author
    role = findSupercolorRole(user)
    if role is None:
        return False

    await user.remove_roles(role)

    if len(role.members) == 0:
        await role.delete()

    return True

                
async def addSupercolor(ctx, hexcode):
    name = currentRoleName(hexcode)
    user = ctx.message.author
        
    role = discord.utils.get(ctx.guild.roles, name=name)
    
    if role is None:
        role = await ctx.guild.create_role(name=name, color=discord.Color(int(hexcode, 16)))
        await role.edit(position=len(ctx.guild.roles) - 2)
        
    await user.add_roles(role)


@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command(pass_context=True, aliases=['sc'], help="Command format: polaroid supercolor <hexcode>", description="Uses user input of a 6-character hex code to create a role with that color and add it to the user. The color role includes the user's username to avoid name conflicts", brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode=None):
    if isValidHex(hexcode):
        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)

        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "polaroid help sc" for info on the command syntax')
        
@bot.command(pass_context=True, aliases=['cc'], help="Command format: polaroid clearcolor", description="Clears a user's color role", brief="Clears a user's color role")
async def clearcolor(ctx):
    had_role = await removeSupercolor(ctx)
    if had_role:
        embed = discord.Embed(title='*Click!*', description='Your color role has been removed')
        await ctx.send(embed=embed)
    else: 
        ctx.send("You do not have a color role")
    
@bot.command(pass_context=True)
async def currentcolor(ctx):
    user = ctx.message.author
    role = findSupercolorRole(user)
    
    if not role:
        ctx.send("You do not have a color role")
        return
        
    hexcode = f"{role.color.value:06X}"
    
    embed = discord.Embed(description=f"{getName(user)}'s current color is #{hexcode}.")
    embed.set_footer(text=f"Command: polaroid supercolor {hexcode}")
    await ctx.send(embed=embed)
            
@bot.command(pass_context=True)
async def copycolor(ctx, username):
    users: list = getUsers(ctx.guild, username)
    
    filtered_users = filterUsers(users)

    if not filtered_users:
        await ctx.send("User not found, or the user entered does not have a valid color role")
        return
        
    if len(filtered_users) == 1:
        found_user = filtered_users[0]
        
    else:
        found_user = None
        users_dict: dict[int, Any] = {}
        for user in filtered_users:
            users_dict[filtered_users.index(user)] = user

        await ctx.send("Multiple users found. Select one by typing the corresponding number:")
        for num, user in users_dict:
            color_role = findSupercolorRole(user)
            hexcode = f"{color_role.color.value:06X}"
            
            embed = discord.Embed(title=f"{num}: {user.display_name}", color=int(hexcode, 16))
            await ctx.send(embed=embed)

        while not found_user:
            requested_user: int = await getInputOfType(int, ctx)
            if requested_user in users_dict:
                found_user = users_dict[requested_user]


    if found_user:
        hexcode = f"{findSupercolorRole(found_user).color.value:06X}"
        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
        