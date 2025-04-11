import discord
from discord.ext import commands, tasks

from misc.config import COMMAND_PREFIX, ACTIVITY, STARTING
from cogs import basicCogs, statsCogs, helpCogs, monitorCogs, eventCogs, recordCogs, competitonCogs, updatesLoop

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, activity=STARTING)

@bot.event
async def on_ready():
    fun_cog = basicCogs.FunCog(bot)
    await bot.add_cog(fun_cog)

    event_cog = eventCogs.EventCog(bot)
    quals_cog = eventCogs.QualificationCog(bot)
    await bot.add_cog(event_cog)
    await bot.add_cog(quals_cog)

    record_cog = recordCogs.RecordCog(bot)
    await bot.add_cog(record_cog)

    stats_cog = statsCogs.StatsCog(bot)
    info_cog = statsCogs.InfoCog(bot)
    await bot.add_cog(stats_cog)
    await bot.add_cog(info_cog)

    monitor_cog = monitorCogs.MonitorCog(bot)
    await bot.add_cog(monitor_cog)

    comp_cog = competitonCogs.CompetitionCog(bot)
    await bot.add_cog(comp_cog)

    updates_loop = updatesLoop.Updates(bot)
    await bot.add_cog(updates_loop)

    bot.help_command = helpCogs.HelpCMD()
    updates_loop.retrieveCogs()

    await bot.change_presence(activity=ACTIVITY)