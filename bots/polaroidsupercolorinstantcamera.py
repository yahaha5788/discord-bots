from discord.ext import commands
import discord.utils
from typing import Any, Optional
from misc.polaroidutils import *

command_prefix = "p!"
activity = discord.Game(name="with colors")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity)


@bot.command(aliases=['sc'],
             usage="p!supercolor <hexcode>",
             description="Uses user input of a 6-character hex code to create a role with that color and add it to the user.",
             brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode=None):
    if isValidHex(hexcode):

        for c in disabled_colors:
            if in_hue_range(c.hex, hexcode) and not (set([role for role in c.allowed_roles]) & set([role.id for role in ctx.author.roles])):
                await ctx.send("This color is disabled, and you do not have the permissions to access it!")
                return
            elif in_hue_range(c.hex, hexcode) and (set([role for role in c.allowed_roles]) & set([role.id for role in ctx.author.roles])):
                await ctx.send("This color is disabled, but you have permissions to use it.")

        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)

        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        setFooter(colorembed)
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "p!help supercolor" for info on the command syntax')
        
@bot.command(aliases=['cc'],
             usage="p!clearcolor",
             description="Removes a user's color role, and deletes it if there are no other users with that role.",
             brief="Clears a user's color role")
async def clearcolor(ctx):
    had_role = await removeSupercolor(ctx)
    if had_role:
        clearembed = discord.Embed(title='*Click!*', description='Your color role has been removed')
        setFooter(clearembed)
        await ctx.send(embed=clearembed)
    else: 
        ctx.send("You do not have a color role")
    
@bot.command(
    aliases=['current'],
    usage='p!currentcolor',
    desription="Gets and sends the user's current color role.",
    brief='Shows your current color role.'
)
async def currentcolor(ctx):
    user = ctx.message.author
    role = findSupercolorRole(user)
    
    if not role:
        ctx.send("You do not have a color role")
        return
        
    hexcode = f"{role.color.value:06X}"
    
    currentembed = discord.Embed(description=f"{getName(user)}'s current color is #{hexcode}.")
    currentembed.add_field(name='Command:', value=f"`p!supercolor {hexcode}`")
    setFooter(currentembed)
    await ctx.send(embed=currentembed)
            
@bot.command(
    aliases=['copy'],
    usage='p!copycolor <user>'
)
async def copycolor(ctx, user):
    user = ctx.guild.get_member(user.id)

    if user:
        hexcode = f"{findSupercolorRole(user).color.value:06X}"
        if not hexcode:
            await ctx.send("That user does not have a color role.")
            return

        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        setFooter(colorembed)
        await ctx.send(embed=colorembed)
    else:
        await ctx.send("That user does not exist!")

@bot.command(
    aliases=['whitelist', 'disable'],
    brief="An admin command that disables a certain color.",
    description='An admin command that disables a certain color as well as ones around it to preserve the meaning of certain colors.'
)
async def disablecolor(ctx, hexcode: str, *exempt_roles: discord.Role):
    if isValidHex(hexcode):
        try:
            await disableColor(ctx, hexcode, [role.id for role in exempt_roles])

            colorembed = discord.Embed(title='*Click!*', description=f"The color role #{hexcode} has been disabled.", color=int(hexcode, 16))
            setFooter(colorembed)
            await ctx.send(embed=colorembed)
        except MissingPermissions:
            await ctx.send("You need admin permissions to disable colors! Ask an admin to run this command.")
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode.')

@bot.command(
    brief='',
    description="",
)
async def help(ctx, keyword: Optional[str] = None):
    desc = "Type `p!help <command>` for help on a specific command." if not keyword else ""
    helpembed = discord.Embed(title="Help Menu", description=desc)
    for cmd in bot.commands:
        header = cmd.usage