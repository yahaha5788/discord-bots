import json
import discord
from discord.ext import commands, tasks

from misc.templates import UpcomingEventCheck, unplayedEventTemplate, OngoingEventCheck
from query_stuff import queries

from misc.config import COMMAND_PREFIX, EMBED_COLOR, setFooter, checkValidNumber, categorizedCommand


class MonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.FOLLOWED_TEAMS_ONGOING_EVENTS: dict[str, OngoingEventCheck] = {}
        self.FOLLOWED_TEAMS_UPCOMING_EVENTS: dict[str, UpcomingEventCheck] = {}

    @commands.group(invoke_without_command=True)
    async def monitor(self, ctx):
        await ctx.send(f"This is the group of monitor commands. Type `{COMMAND_PREFIX}help monitor` for more info")

    @categorizedCommand(
        category='monitor',
        aliases=['support', 'track', 'follow'],
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}favorite <number>"
    )
    async def favorite(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        guild_id = str(ctx.guild.id)

        with open('../bots/following.json', 'r+') as following:
            followed_teams: dict[str, list[str]] = json.load(following)

            if guild_id not in followed_teams.keys():
                followed_teams[guild_id] = []

            if number in followed_teams[guild_id]:
                await ctx.send(f"You are already following Team {number}, {queries.nameFromNumber(number)}")
                return

            followed_teams[guild_id].append(number)
            following.seek(0)
            json.dump(followed_teams, following, indent=4)
            following.truncate()

        await ctx.send(f"You are now following Team {number}, {queries.nameFromNumber(number)}")

    @categorizedCommand(
        category='monitor',
        aliases=['unfollow'],
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}unfavorite <number>"
    )
    async def unfavorite(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        guild_id = str(ctx.guild.id)

        with open('../bots/following.json', 'r+') as following:
            followed_teams: dict[str, list[str]] = json.load(following)

            if guild_id not in followed_teams.keys():
                await ctx.send('You are not following any teams')
                return

            if number not in followed_teams[guild_id]:
                await ctx.send(f"You are not following {number}.")

            followed_teams[guild_id].remove(number)
            following.seek(0)
            json.dump(followed_teams, following, indent=4)
            following.truncate()

        await ctx.send(f"You are no longer following Team {number}, {queries.nameFromNumber(number)}")

    @categorizedCommand(
        category='monitor',
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}designatechannel"
    )
    async def designatechannel(self, ctx):
        guild_id = str(ctx.guild.id)
        channel_id = ctx.channel.id

        with open('../bots/channel_des.json', 'r+') as channel_des:
            channels: dict[str, int] = json.load(channel_des)
            channels[guild_id] = channel_id

            channel_des.seek(0)
            json.dump(channels, channel_des, indent=4)
            channel_des.truncate()

        await ctx.send("Notifications for teams you are following will show up here.")

    @tasks.loop(hours=1)
    async def sendNotifications(self):
        with open('../bots/channel_des.json', 'r') as channels:
            notif_channels: dict[str, int] = json.load(channels)

            for guild_id, channel_id in notif_channels.items():
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    continue

                with open('../bots/following.json', 'r') as following:
                    followed_teams: dict[str, list[str]] = json.load(following)

                    if guild_id not in followed_teams.keys():
                        continue

                    followed_teams: list[str] = followed_teams[guild_id]

                    for number in followed_teams:
                        # UPCOMING EVENTS
                        data, success = queries.upcomingEvents(number)
                        if not success:
                            continue

                        team_upcoming_events: UpcomingEventCheck = self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number]
                        team_upcoming_events.last_events = team_upcoming_events.current_events
                        team_upcoming_events.current_events = data

                        if team_upcoming_events.last_events != team_upcoming_events.current_events:
                            events = [event for event in team_upcoming_events.current_events.events if event not in team_upcoming_events.last_events.events]  # teehee
                        else:
                            continue

                        title = f"Team {number}, {queries.nameFromNumber(number)} has a new event!"
                        desc = ""

                        for event in events:
                            desc = desc + unplayedEventTemplate(event) + "\n"

                        unplayed_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                        setFooter(unplayed_notif_embed)

                        await channel.send(embed=unplayed_notif_embed)

                    for number in followed_teams:
                        # ONGOING EVENTS
                        data, success = queries.ongoingEvents(number)
                        if not success:
                            continue

                        team_ongoing_events: OngoingEventCheck = self.FOLLOWED_TEAMS_ONGOING_EVENTS[number]
                        team_ongoing_events.last_events = team_ongoing_events.current_events
                        team_ongoing_events.current_events = data

                        if team_ongoing_events.last_events != team_ongoing_events.current_events:
                            events = [event for event in team_ongoing_events.current_events.events if event not in team_ongoing_events.last_events.events]  # teehee
                        else:
                            continue

                        title = f"Team {number}, {queries.nameFromNumber(number)} is currently playing in an event!"
                        desc = ""

                        for event in events:
                            desc = desc + unplayedEventTemplate(event) + "\n"

                        ongoing_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                        setFooter(ongoing_notif_embed)

                        await channel.send(embed=ongoing_notif_embed)
