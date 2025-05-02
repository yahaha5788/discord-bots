import math
import tkinter as tk
from typing import NamedTuple
import matplotlib.pyplot as plt
import numpy as np
import colorsys
import discord
from discord.ext.commands import MissingPermissions
import re

class DisabledColor(NamedTuple):
    hex: str
    allowed_roles: list[int]  # list of role ids

disabled_colors: list[DisabledColor] = []

# --------------------------- DEF ------------------------------#


def currentRoleName(hexcode: str) -> str:
    return f"sc.{hexcode}"  # never underestimate my laziness


def isValidHex(hexcode) -> bool:
    if not isinstance(hexcode, str):
        return False

    return bool(re.fullmatch(r"[0-9A-Fa-f]{6}", hexcode))

def findRole(hexcode: str, guild: discord.Guild) -> discord.Role:
    role = discord.utils.get(guild.roles, name=currentRoleName(hexcode))
    return role

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

def check(ctx):
    return lambda \
        m: m.author == ctx.author and m.channel == ctx.channel  # if message sent is the same channel & author as the original message

def setFooter(embed: discord.Embed) -> None:
    embed.add_field(name="Links", value="[Report a problem](https://github.com/yahaha5788/discord-bots/issues/new) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)

def hex_to_hsv(hex_color):
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_hex(h, s, v) -> str:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255)) # whyyy

def plot_color_range(center_hex, offset=3):
    center_h, s, v = hex_to_hsv(center_hex)

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

async def getInputOfType(func, ctx, bot):
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
        role = await ctx.guild.create_role(name=name, color=discord.Color(int(hexcode, 16)), hoist=False, mentionable=False)
        await role.edit(position=len(ctx.guild.roles) - 2)

    await user.add_roles(role)

async def disableColor(ctx, hexcode: str, allowed_roles: list[int]):
    if ctx.author.guild_permissions.administrator:
        disabled_colors.append(DisabledColor(hexcode, allowed_roles))
        role = findRole(hexcode, ctx.guild)
        if role:
            await role.delete()
    else:
        raise MissingPermissions(["Administrator"])

def get_color_at_angle(base_hex, offset_deg) -> str:
    h, s, v = hex_to_hsv(base_hex)
    base_deg = h * 360

    new_deg = (base_deg + offset_deg) % 360
    h = new_deg / 360

    return f"#{hsv_to_hex(h, s, v)}"

def fix_radians(rad):
    while rad > math.pi:
        rad -= 2 * math.pi

    while rad < -math.pi:
        rad += 2 * math.pi

    return rad

def in_hue_range(base, ref, offset=3):
    base_h, _, _ = hex_to_hsv(base)
    ref_h, _, _ = hex_to_hsv(ref)

    base_rad = math.radians(base_h * 360)
    ref_rad = math.radians(ref_h * 360)

    return abs(fix_radians(base_rad - ref_rad)) < math.radians(offset)



# 00FFFF as test
# 00FFFA is in range, 00FAAA is not
