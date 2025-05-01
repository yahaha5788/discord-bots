from discord.ext import commands
import discord.utils
from typing import Any
from misc.polaroidutils import *

command_prefix = "p!"
activity = discord.Game(name="with colors")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity)


@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command(pass_context=True, aliases=['sc'], help="Command format: polaroid supercolor <hexcode>", description="Uses user input of a 6-character hex code to create a role with that color and add it to the user. The color role includes the user's username to avoid name conflicts", brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode=None):
    if isValidHex(hexcode):

        for c in disabled_colors:
            if in_hue_range(c.hex, hexcode) and not (set([role for role in c.allowed_roles]) & set([role.id for role in ctx.author.roles])):
                await ctx.send("This color is disabled, and you do not have the permissions to access it!")


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
            
@bot.command(aliases=['copy'])
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
        for num, user in users_dict.items():
            color_role = findSupercolorRole(user)
            hexcode = f"{color_role.color.value:06X}"
            
            embed = discord.Embed(title=f"{num}: {user.display_name}", color=int(hexcode, 16))
            await ctx.send(embed=embed)

        while not found_user:
            requested_user: int = await getInputOfType(int, ctx, bot)
            if requested_user in users_dict:
                found_user = users_dict[requested_user]
            else:
                await ctx.send("Please enter a valid number.")


    if found_user:
        hexcode = f"{findSupercolorRole(found_user).color.value:06X}"
        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)

@bot.command(aliases=['whitelist', 'disable'])
async def disablecolor(ctx, hexcode: str, *exempt_roles: discord.Role):
    if isValidHex(hexcode):
        await disableColor(ctx, hexcode, [role.id for role in exempt_roles])

        colorembed = discord.Embed(title='*Click!*', description=f"The color role #{hexcode} has been disabled.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
        await ctx.send(disabled_colors)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode.')