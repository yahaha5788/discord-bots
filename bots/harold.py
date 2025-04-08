import discord
from discord.ext import commands

from misc.config import COMMAND_PREFIX, ACTIVITY, STARTING
from cogs import basicCogs, statsCogs, helpCogs, monitorCogs, eventCogs, recordCogs

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, activity=STARTING)

@bot.event
async def on_ready():
    await bot.add_cog(basicCogs.FunCog(bot))

    await bot.add_cog(eventCogs.EventCog(bot))
    await bot.add_cog(eventCogs.QualificationCog(bot))

    await bot.add_cog(recordCogs.RecordCog(bot))

    await bot.add_cog(statsCogs.StatsCog(bot))
    await bot.add_cog(statsCogs.InfoCog(bot))

    await bot.add_cog(monitorCogs.MonitorCog(bot))

    bot.help_command = helpCogs.HelpCMD()

    await bot.change_presence(activity=ACTIVITY)

    await monitorCogs.MonitorCog(bot).startNotificationLoop()