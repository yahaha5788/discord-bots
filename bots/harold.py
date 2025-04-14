import discord
from discord.ext import commands

from cogs import basicCogs, competitonCogs, eventCogs, monitorCogs, recordCogs, statsCogs, helpCogs

from misc.config import ACTIVITY, VALID_GUILDS, STARTING

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='h$', intents=intents, activity=STARTING)

@bot.event
async def on_ready():
    await bot.add_cog(basicCogs.FunCog(bot))

    # await bot.add_cog(competitonCogs.CompetitionCog(bot)) TODO: FINISH THIS

    await bot.add_cog(eventCogs.EventCog(bot))
    await bot.add_cog(eventCogs.QualificationCog(bot))

    await bot.add_cog(monitorCogs.MonitorCog(bot))

    await bot.add_cog(recordCogs.RecordCog(bot))

    await bot.add_cog(statsCogs.StatsCog(bot))
    await bot.add_cog(statsCogs.InfoCog(bot))

    await bot.add_cog(helpCogs.HelpCog(bot))

    for guild in VALID_GUILDS:
        await bot.tree.sync(guild=guild)

    await bot.change_presence(activity=ACTIVITY)
    print('Bot is ready')