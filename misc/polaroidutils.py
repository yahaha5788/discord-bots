import math
from typing import NamedTuple
import matplotlib.pyplot as plt
import numpy as np
import colorsys
import discord
from discord.ext.commands import MissingPermissions, Bot
import re

class DisabledColor(NamedTuple):
    hex: str
    allowed_roles: list[int]  # list of role ids

disabled_colors: list[DisabledColor] = []

# --------------------------- DEF ------------------------------#


def _current_role_name(hexcode: str) -> str:
    """
    Gives the current role name schema so it doesn't have to be changed everywhere.
    :param hexcode: The hexcode to use in the role name
    :return: The formatted name of the role
    """
    return f"sc.{hexcode}"  # never underestimate my laziness


def is_valid_hex(hexcode: str) -> bool:
    """
    Checks if a given string is a valid 6-character hexcode.
    :param hexcode: The hexcode to check
    :return: If the hexcode is a valid hexcode
    """

    return bool(re.fullmatch(r"[0-9A-Fa-f]{6}", hexcode))

def get_name(user) -> str:
    """
    Gets the display or nickname for a user (used only in currentcolor).
    :param user: The user to get the name of
    :return: The nick or display name of the user
    """
    return user.nick if user.nick else user.display_name

def find_supercolor_role(user):
    """
    Gets a supercolor role from a user if they have one.
    :param user: The user to check
    :return: The role, or None if no role was found
    """
    for role in user.roles:
        if role.name.startswith("sc."):
            return role

    return None

def _check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel  # if message sent is the same channel & author as the original message

def set_footer(embed: discord.Embed) -> None:
    """
    Adds a field to the embed with the GitHub repository link and link to report an issue.
    :param embed: The embed to add the links to
    """
    embed.add_field(name="Links", value="[Report a problem](https://github.com/yahaha5788/discord-bots/issues/new) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)

def _hex_to_hsv(hexcode) -> tuple[float, float, float]:
    """
    Converts a hexcode into RGB values, and uses colorsys to convert those RGB values into HSV values.
    :param hexcode: The hexcode to be converted
    :return: the hue, saturation, and value
    """
    r, g, b = tuple(int(hexcode[i:i+2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)

def _hsv_to_hex(h, s, v) -> str:
    """
    Uses colorsys to convert the hue, saturation, and value of a color into RGB values,
    then formats the values into parts of a hexcode which are then put together in a string.
    :param h: The hue of the color
    :param s: The saturation of the color
    :param v: The value of the color
    :return: The hexcode of the color
    """
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

def plot_color_range(center_hex, offset=3) -> None:
    """
    Uses matplotlib to plot a polar graph from the "center" hexcode and an offset (defaults to 3)
    showing the color's placement on an HSV spectrum and the range of what colors will be disabled.
    May be used in the future for disable color or a command to show all disables colors.
    :param center_hex: The hexcode the use as a reference
    :param offset: The offset (in degrees) in each direction for disabled colors
    """
    center_h, s, v = _hex_to_hsv(center_hex)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.set_yticklabels([])

    for h in range(360): #spin wheeeeee
        rgb = colorsys.hsv_to_rgb(h / 360, s, v)
        ax.bar(np.radians(h), 1, width=np.radians(1), color=rgb, edgecolor=rgb)

    for h in range(int((center_h * 360) - offset), int((center_h * 360) + offset)):
        hue = h % 360  # wrap around circle
        rgb = colorsys.hsv_to_rgb(hue / 360, s, v)
        ax.bar(
            np.radians(hue),
            1.1,
            width=np.radians(1),
            color=rgb,
            edgecolor='black',
            linewidth=0.5,
            alpha=0.25
        )

    ax.plot(np.radians(center_h * 360), 1, 'o', color='white', markersize=10, markeredgecolor='black')

    plt.title(f"Disabled color: {center_hex.upper()}")
    plt.show()


# --------------------------- ASYNC DEF ------------------------------#

async def get_input_of_type(msg_type, ctx, bot):
    """
    Was used for selecting a user for copycolor. Might be used later for supercolor in saving roles by finding similar colors
    and using a second input.
    :param msg_type: The type of input
    :param ctx: The context, passed in from the command
    :param bot: The bot, obviously
    :return: The message, if it is the correct type
    """
    while True:
        try:
            msg = await bot.wait_for('message', check=_check(ctx))
            return msg_type(msg.content)
        except ValueError:
            ctx.send(f"Please enter a {msg_type}") # this might say something like builtins.str but idk
            continue                               # i'll fix it if it comes up but for now it's fine

async def remove_supercolor(user, role) -> None:
    """
    Removes a supercolor role from the user, and deletes it if nobody else has that role.
    :param user: The user to remove the role from
    :param role: The role to remove
    """
    await user.remove_roles(role)

    if len(role.members) == 0:
        await role.delete()

async def add_supercolor(ctx, bot: Bot, hexcode) -> None:
    """
    Adds a supercolor role to user, and creates one if it does not exist already.
    :param ctx: The context, passed in from the command
    :param bot: The bot
    :param hexcode: The hexcode to be used in the role name and color
    """
    name = _current_role_name(hexcode)
    user = ctx.message.author

    role = discord.utils.get(ctx.guild.roles, name=name)

    if role is None:
        role = await ctx.guild.create_role(name=name, color=discord.Color(int(hexcode, 16)), hoist=False, mentionable=False)
        bot_user: discord.Member = ctx.guild.get_member(bot.user.id)
        highest_role = ctx.guild.roles.index(bot_user.top_role)
        await role.edit(position=highest_role - 1)

    await user.add_roles(role)

async def disable_color(ctx, hexcode: str, allowed_roles: list[int]) -> None:
    """
    Disables a given color from a hexcode, as well as a range of similar colors around it.
    :param ctx: The context, passed in from the command
    :param hexcode: The hexcode to disable
    :param allowed_roles: Any roles taken as *exempt_roles. These roles are exemple from the effect and can still use the color normally
    :raise MissingPermissions: If the command user is not an administrator.
    """
    if ctx.message.author.guild_permissions.administrator:
        disabled_colors.append(DisabledColor(hexcode, allowed_roles))
        role = await discord.utils.get(ctx.guild.roles, name=_current_role_name(hexcode))
        if role:
            await role.delete()
    else:
        raise MissingPermissions(["Administrator"])

def _get_color_at_angle(base_hex, offset_deg) -> str:
    """
    Gets a hexcode at an offset from a given base hex.
    :param base_hex: The hexcode to use as reference
    :param offset_deg: The amount to offset by
    :return: The offset hexcode.
    """
    h, s, v = _hex_to_hsv(base_hex)
    base_deg = h * 360

    new_deg = (base_deg + offset_deg) % 360
    h = new_deg / 360

    return f"#{_hsv_to_hex(h, s, v)}"

def _fix_radians(rad: float) -> float:
    """
    Fixes a radian value to make sure that values across the circle (at positions like 358° if a hexcode at 0° is disabled) still get disabled
    :param rad: The radian value to fix
    :return: The fixed radian value
    """
    while rad > math.pi:
        rad -= 2 * math.pi

    while rad < -math.pi:
        rad += 2 * math.pi

    return rad

def in_hue_range(base, ref, offset=3) -> bool:
    """
    Checks if a given hexcode is within a certain distance on the HSV spectrum from a base hexcode
    :param base: The base disabled hexcode
    :param ref: The hexcode to check
    :param offset: The degree offset from the base hexcode where hexcodes can be used again. Defaults to three.
    :return: If the given hexcode is within the offset from the base hexcode.
    """
    base_h, _, _ = _hex_to_hsv(base)
    ref_h, _, _ = _hex_to_hsv(ref)

    base_rad = math.radians(base_h * 360)
    ref_rad = math.radians(ref_h * 360)

    return abs(_fix_radians(base_rad - ref_rad)) < math.radians(offset)



# 00FFFF as test
# 00FFFA is in range, 00FAAA is not
