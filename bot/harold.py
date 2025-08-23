import discord
from discord.ext import commands

from cogs import basicCogs, competitonCogs, eventCogs, monitorCogs, recordCogs, statsCogs, helpCogs

from misc.config import ACTIVITY, STARTING

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='h$', intents=intents, activity=STARTING)



@bot.event
async def on_ready():
    for cog in bot.cogs: # eat some leftovers
        await bot.remove_cog(cog)

    await bot.add_cog(basicCogs.FunCog(bot))

    # await bot.add_cog(competitonCogs.CompetitionCog(bot)) NOT FUNCTIONAL

    await bot.add_cog(eventCogs.EventCog(bot))
    await bot.add_cog(eventCogs.QualificationCog(bot))

    await bot.add_cog(monitorCogs.MonitorCog(bot))
    #
    await bot.add_cog(recordCogs.RecordCog(bot))
    #
    await bot.add_cog(statsCogs.StatsCog(bot))
    await bot.add_cog(statsCogs.InfoCog(bot))

    help_cog = helpCogs.HelpCog(bot)

    await bot.add_cog(help_cog)

    # Sync to each guild
    for guild in bot.guilds:
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild: {guild.name} ({guild.id})")
        except Exception as e:
            print(f"Failed to sync commands to guild {guild.name} ({guild.id}): {e}")

    help_cog.wrap_all_commands(bot.guilds[0])

    await bot.change_presence(activity=ACTIVITY)
    print('Bot is ready')