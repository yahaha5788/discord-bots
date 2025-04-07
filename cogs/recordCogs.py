import discord
from discord.ext import commands
from query_stuff import queries
from misc.templates import *
from misc.config import setFooter, EMBED_COLOR, categorizedCommand, COMMAND_PREFIX


class RecordCog(commands.Cog):

    @commands.group(invoke_without_command=True)
    async def records(self, ctx):
        await ctx.send(f"This is the group of record commands. Type `{COMMAND_PREFIX}help records` for more info.")

    @categorizedCommand(
        category="records",
        aliases=['topteam', 'bt'],
        description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region',
        brief="Gets the best team from ftcscout.org",
        usage=f"{COMMAND_PREFIX}bestteam <region>",
        parameters={
            "<region>": "An optional argument for the region to search in. Defaults to All."
        }
    )
    async def bestteam(self, ctx, region='All'):
        data, success = queries.bestTeam(region)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return
        team_info, team_qstats, team_events = data
        auto, tele, endgame, np = team_qstats
        location = team_info.loc.cityStateCountry
        title = f"Team {team_info.number}, {team_info.name}"
        desc = f"Located in {location}"

        embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)

        name, val = qStatsTemplate(auto, tele, endgame, np)
        embed.add_field(name=name, value=val, inline=False)

        for event in team_events:
            if event.started:
                name, val = eventTemplate(event)

                embed.add_field(name=name, value=val, inline=False)

        setFooter(embed)

        await ctx.send(embed=embed)

    @categorizedCommand(
        category='records',
        aliases=['wr', 'worldrecord', 'bm'],
        description='Queries the best match from ftcscout.org with an optional region modifier to search within a given region',
        brief="Gets the best match from ftcscout.org.",
        usage=f"{COMMAND_PREFIX}bestmatch <region>",
        parameters={
            "<region>": "An optional argument for the region to search in. Defaults to All."
        }
    )
    async def bestmatch(self, ctx, region='All'):
        data, success = queries.bestMatch(region)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

        event, match = data


        title = f"Best match was played at {event.name} on {event.start}\n{event.location.cityStateCountry} ({event.event_type})"
        scores_embed = discord.Embed(title=title, description="═══════════════════════════════", color=EMBED_COLOR)

        addMatchScores(match, scores_embed)

        setFooter(scores_embed)

        await ctx.send(embed=scores_embed)

