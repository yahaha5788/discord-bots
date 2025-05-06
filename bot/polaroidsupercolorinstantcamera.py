import shlex

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
    usage='p!copycolor (as a reply)',
    description="Copies a user's current color role by replying to their message.",
    brief="Copies a user's current color role."
)
async def copycolor(ctx):
    if not ctx.message.reference:
        await ctx.send("Reply to a user's message to copy their color.")
        return

    try:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        target_user = replied_message.author
    except Exception:
        await ctx.send("Couldn't find the user from the replied message.")
        return

    member = ctx.guild.get_member(target_user.id)
    if not member:
        await ctx.send("That user is not in this server.")
        return

    role = find_supercolor_role(member)
    if not role:
        await ctx.send("That user does not have a color role.")
        return

    hexcode = f"{role.color.value:06X}".upper()

    role = find_supercolor_role(ctx.message.author)
    if role:
        await remove_supercolor(ctx.message.author, role)
    await add_supercolor(ctx, bot, hexcode)

    colorembed = discord.Embed(title='*Click!*', description=f"{get_name(ctx.message.author)} has copied the color #{hexcode} from {get_name(target_user)}", color=int(hexcode, 16))
    set_footer(colorembed)
    await ctx.send(embed=colorembed)


@bot.command(
    aliases=['disable'],
    brief="An admin command that disables a certain color.",
    usage='p!disablecolor <hexcode> <"exempt role name">',
    description='An admin command that disables a certain color. Names of roles can be passed it in the format `"role name"` to define roles that are allowed to use the color.'
)
async def disablecolor(ctx, hexcode: str, *, exempt_roles: str = None):
    hexcode = hexcode.upper()
    if is_valid_hex(hexcode):
        if exempt_roles:
            exempt_roles = shlex.split(exempt_roles)
        else: exempt_roles = []

        try:
            roles = [role for role in ctx.guild.roles if role.name in exempt_roles]
            if len(roles) < len(exempt_roles):
                await ctx.send("One or more specified roles were not found. Would you still like to run the command?")
                proceed = await get_proceed_input(str, ctx, bot)
                if proceed.lower() == 'yes':
                    await disable_color(ctx, hexcode, [role.id for role in roles])
                else:
                    await ctx.send("Stopping the command.")
                    return

            elif len(roles) > len(exempt_roles):
                await ctx.send("Multiple roles have been found from one or more given names. Would you still like to run the command?")
                proceed = await get_proceed_input(str, ctx, bot)
                if proceed.lower() == 'yes':
                    await disable_color(ctx, hexcode, [role.id for role in roles])
                else:
                    await ctx.send("Stopping the command.")
                    return

            else:
                await disable_color(ctx, hexcode, [role.id for role in roles])

            colorembed = discord.Embed(title='*Click!*', description=f"The color role #{hexcode} has been disabled.", color=int(hexcode, 16))
            set_footer(colorembed)
            await ctx.send(embed=colorembed)
        except MissingPermissions:
            await ctx.send("You need admin permissions to disable colors! Ask an admin to run this command.")
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode.')

@bot.command(
    aliases=['enable'],
    brief="An admin command that enables a disabled color.",
    usage='p!enablecolor <hexcode>',
    description='An admin command that enables a previously disabled color.'
)
async def enablecolor(ctx, hexcode: str):
    hexcode = hexcode.upper()
    if is_valid_hex(hexcode):
        try:
            enable = await enable_color(ctx, hexcode)
            if enable:
                colorembed = discord.Embed(title='*Click!*', description=f"The color role #{hexcode} has been enabled.", color=int(hexcode, 16))
                set_footer(colorembed)
                await ctx.send(embed=colorembed)
            else:
                await ctx.send("That color is already enabled!")
        except MissingPermissions:
            await ctx.send("You need admin permissions to disable colors! Ask an admin to run this command.")
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode.')

@bot.command(
    aliases=["roles", "colors"],
    brief="A command to show every supercolor role in the server.",
    usage="p!supercolors",
    description="A command to show every supercolor role in the server."
)
async def supercolors(ctx):
    guild: discord.Guild = ctx.guild
    supercolor_roles: list[discord.Role] = []
    for role in guild.roles:
        if role.name.startswith("sc."):
            supercolor_roles.append(role)
    if supercolor_roles is not None:
        desc = ""
        for role in supercolor_roles:
            role_hex = f"{role.color.value:06X}".upper()
            members = role.members
            users = ""
            for member in members:
                if members.index(member) == len(members) - 1:
                    users += get_name(member)
                else:
                    users += f"{get_name(member)}, "
            desc += f"#{role_hex} - {users}\n"
        rolesembed = discord.Embed(title=f"Supercolor roles in {guild.name}", description=desc, color=EMBED_COLOR)
        await ctx.send(embed=rolesembed)
    else:
        await ctx.send(f"There are no supercolor roles in {guild.name}. Use `p!supercolor <hexcode>` to make one!")

@bot.command(
    aliases=['color'],
    brief="Sends on embed with a color",
    usage="p!showcolor <hexcode>",
    description="Sends an embed with the given color and a copy/paste command"
)
async def showcolor(ctx, hexcode):
    if is_valid_hex(hexcode):
        colorembed = discord.Embed(title=f"#{hexcode}", description=f"`p!supercolor {hexcode}`", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
    else:
        await ctx.send("That is not a valid hexcode!")

@bot.command(
    brief="Converts rgb, hsv, or a hexcode into another form.",
    description="Converts an rgb, hex, or hexcode value into another value of a different type.",
    usage='p!convert <"hex" | "rgb" | "hsv"> <"hex" | "rgb" | "hsv"> <hexcode / r / h> <g / s> <b / v>'
)
async def convert(ctx, start_type, end_type, val_1, val_2, val_3):
    match start_type:
        case "hex":
            if not is_valid_hex(val_1):
                await ctx.send("The given hex is not a valid hexcode.")
                return
        case "rgb":
            if not is_valid_rgb(val_1, val_2, val_3):
                await ctx.send("That is not a valid RGB value.")
                return
        case "hsv":
            if not is_valid_hsv(val_1, val_2, val_3):
                await ctx.send("That is not a valid HSV value.")
                return
    convertembed = discord.Embed(title=f"Convert {start_type} to {end_type}", description=f"Result: {convert_to(start_type, end_type, val_1, val_2, val_3)}", color=int(convert_to(start_type, "hex", val_1, val_2, val_3), 16))
    await ctx.send(embed=convertembed)

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

# @bot.command()
# async def say(ctx, content):
#     await ctx.send(content)
