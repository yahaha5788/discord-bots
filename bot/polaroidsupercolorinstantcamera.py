from discord.ext import commands
import discord.utils
from typing import Optional
from bot.polaroidutils import *

command_prefix = "p!"
activity = discord.Game(name="with colors")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity, help_command=None)


@bot.command(aliases=['sc'],
             usage="p!supercolor <hexcode>",
             description="Uses user input of a 6-character hex code to create a role with that color and add it to the user.",
             brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode: str = None):
    hexcode = hexcode.upper()
    if is_valid_hex(hexcode):
        for c in disabled_colors:
            if in_hue_range(c.hex, hexcode) and not (set([role for role in c.allowed_roles]) & set([role.id for role in ctx.message.author.roles])):
                await ctx.send("This color is disabled, and you do not have the permissions to access it!")
                return
            elif in_hue_range(c.hex, hexcode) and (set([role for role in c.allowed_roles]) & set([role.id for role in ctx.message.author.roles])):
                await ctx.send("This color is disabled, but you have permissions to use it.")

        role = find_supercolor_role(ctx.message.author)
        if role:
            await remove_supercolor(ctx.message.author, role)
            
        await add_supercolor(ctx, bot, hexcode)

        colorembed = discord.Embed(title='*Click!*', description=f"{get_name(ctx.message.author)} has been given the color #{hexcode}.", color=int(hexcode, 16))
        set_footer(colorembed)
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "p!help supercolor" for info on the command syntax')
        
@bot.command(aliases=['cc'],
             usage="p!clearcolor",
             description="Removes a user's color role, and deletes it if there are no other users with that role.",
             brief="Clears a user's color role")
async def clearcolor(ctx):
    role = find_supercolor_role(ctx.message.author)
    if role:
        await remove_supercolor(ctx.message.author, role)
        clearembed = discord.Embed(title='*Click!*', description=f"{get_name(ctx.message.author)}'s color role has been removed.")
        set_footer(clearembed)
        await ctx.send(embed=clearembed)
    else: 
        await ctx.send("You do not have a color role")
    
@bot.command(
    aliases=['current'],
    usage='p!currentcolor',
    desription="Gets and sends the user's current color role.",
    brief='Shows your current color role.'
)
async def currentcolor(ctx):
    user = ctx.message.author
    role = find_supercolor_role(user)
    
    if not role:
        await ctx.send("You do not have a color role.")
        return
        
    hexcode = f"{role.color.value:06X}"
    hexcode = hexcode.upper()
    
    currentembed = discord.Embed(description=f"{get_name(user)}'s current color is #{hexcode}.", color=int(hexcode, 16))
    currentembed.add_field(name='Command:', value=f"`p!supercolor {hexcode}`")
    set_footer(currentembed)
    await ctx.send(embed=currentembed)
            
@bot.command(
    aliases=['copy'],
    usage='p!copycolor <user>',
    description="Copies a user's current color role.",
    brief="Copies a user's current color role."
)
async def copycolor(ctx, user: discord.User):
    user = ctx.guild.get_member(user.id)

    if user:
        role = find_supercolor_role(user)
        if not role:
            await ctx.send("That user does not have a color role.")
            return

        hexcode = f"{role.color.value:06X}"
        hexcode = hexcode.upper()

        await remove_supercolor(user, role)
        await add_supercolor(ctx, bot, hexcode)
        colorembed = discord.Embed(title='*Click!*', description=f"{get_name(ctx.message.author)} has copied the color #{hexcode} from {get_name(user)}", color=int(hexcode, 16))
        set_footer(colorembed)
        await ctx.send(embed=colorembed)

    else:
        await ctx.send("That user does not exist!")

@bot.command(
    aliases=['whitelist', 'disable'],
    brief="An admin command that disables a certain color.",
    usage='p!disablecolor <hexcode>',
    description='An admin command that disables a certain color as well as ones around it to preserve the meaning of certain colors.'
)
async def disablecolor(ctx, hexcode: str, *exempt_roles: discord.Role):
    hexcode = hexcode.upper()
    if is_valid_hex(hexcode):
        try:
            await disable_color(ctx, hexcode, [role.id for role in exempt_roles])

            colorembed = discord.Embed(title='*Click!*', description=f"The color role #{hexcode} has been disabled.", color=int(hexcode, 16))
            set_footer(colorembed)
            await ctx.send(embed=colorembed)
        except MissingPermissions:
            await ctx.send("You need admin permissions to disable colors! Ask an admin to run this command.")
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode.')

@bot.command(
    usage='p!help <command>',
    brief='Shows this menu.',
    description="Shows this menu.",
)
async def help(ctx, command: Optional[str] = None):
    cmd = [cmd for cmd in bot.commands if cmd.name == command]
    if not cmd and not command:
        helpembed = discord.Embed(title="Help Menu", description="Type `p!help <command>` for help on a specific command.", color=EMBED_COLOR)
        for bot_command in bot.commands:
            header = bot_command.usage
            value = bot_command.brief
            helpembed.add_field(name=header, value=value, inline=False)
    elif cmd and command:
        cmd = cmd[0]
        helpembed = discord.Embed(title=cmd.usage, description=cmd.description, color=EMBED_COLOR)
    else:
        helpembed = discord.Embed(title='Help Error', description="That is not a valid command name. Type `p!help` to see all commands.", color=EMBED_COLOR)

    set_footer(helpembed)
    await ctx.send(embed=helpembed)
