import json
import discord
from discord.ext import commands, tasks

from misc.templates import unplayedEventTemplate, UpcomingEvents, OngoingEvents, Event
from query_stuff import queries

from misc.config import COMMAND_PREFIX, EMBED_COLOR, setFooter, checkValidNumber, categorizedCommand


class MonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot
        self.FOLLOWED_TEAMS_ONGOING_EVENTS: dict[str, OngoingEventChecker] = {}
        self.FOLLOWED_TEAMS_UPCOMING_EVENTS: dict[str, UpcomingEventChecker] = {}

    async def startNotificationLoop(self):
        self.setEvents()
        await self.sendNotifications.start()

    def setEvents(self):
        with open('../bots/following.json', 'r') as following:
            followed_teams: dict[str, list[str]] = json.load(following)
            for numbers in followed_teams.values():
                for number in numbers:
                    data, success = queries.ongoingEvents(number)
                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number] = OngoingEventChecker(data, data)
                    data, success = queries.upcomingEvents(number)
                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number] = UpcomingEventChecker(data, data)

    @commands.group(invoke_without_command=True)
    async def monitor(self, ctx):
        await ctx.send(f"This is the group of monitor commands. Type `{COMMAND_PREFIX}help monitor` for more info")

    @categorizedCommand(
        category='monitor',
        aliases=['support', 'track', 'follow'],
        description='Follows a team. If a channel if designated, the bot will send notifications if the team if currently participating in an event, or if they have a new upcoming event.',
        brief="Follows a team",
        usage=f"{COMMAND_PREFIX}favorite <number>",
        parameters={
            '<number>': 'The number of the team to follow.'
        }
    )
    async def favorite(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        guild_id = str(ctx.guild.id)

        with open('../bots/following.json', 'r+') as following, open('../bots/channel_des.json', 'r') as channel_des:
            followed_teams: dict[str, list[str]] = json.load(following)
            channels: dict[str, int] = json.load(channel_des)

            if guild_id not in channels.keys():
                await ctx.send(f"You have not designated a channel to send notifications in. Run {COMMAND_PREFIX}designatechannel in a channel to set that channel as the notification channel")

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
        description='Unfollows a team. If the guild was previously receiving notifications about this team, they will no longer.',
        brief="Unfollows a team.",
        usage=f"{COMMAND_PREFIX}unfavorite <number>",
        parameters={
            '<number>': 'The number of the team to query for.'
        }
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
                return

            followed_teams[guild_id].remove(number)
            following.seek(0)
            json.dump(followed_teams, following, indent=4)
            following.truncate()

        await ctx.send(f"You are no longer following Team {number}, {queries.nameFromNumber(number)}")

    @categorizedCommand(
        category='monitor',
        description='Designates the channel for notifications. This is where hourly notifications will be sent about followed teams.',
        brief="Sets the channel where notifications will be sent.",
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

        await self.bot.wait_until_ready()

        with open('../bots/channel_des.json', 'r') as channels, open('../bots/following.json', 'r') as following:
            notif_channels: dict[str, int] = json.load(channels)
            followed_teams: dict[str, list[str]] = json.load(following)

            for guild_id, channel_id in notif_channels.items():
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    continue

                if guild_id not in followed_teams.keys():
                    continue

                followed_teams: list[str] = followed_teams[guild_id]

                for number in followed_teams:

                    data, success = queries.upcomingEvents(number)
                    if not success:
                        continue

                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].last = self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].current
                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].current = data

                    if self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].has_changed:
                        events = self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].changes
                    else:
                        continue

                    title = f"Team {number}, {queries.nameFromNumber(number)} has a new event!"
                    desc = ""

                    for event in events:
                        desc = desc + unplayedEventTemplate(event) + "\n"

                    unplayed_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                    setFooter(unplayed_notif_embed)

                    await channel.send(embed=unplayed_notif_embed)


                    data, success = queries.ongoingEvents(number)
                    if not success:
                        continue

                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].last = self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].current
                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].current = data

                    if self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].has_changed:
                        events = self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].changes
                    else:
                        continue

                    title = f"Team {number}, {queries.nameFromNumber(number)} is currently playing in an event!"
                    desc = ""

                    for event in events:
                        desc = desc + unplayedEventTemplate(event) + "\n"

                    ongoing_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                    setFooter(ongoing_notif_embed)

                    await channel.send(embed=ongoing_notif_embed)

class UpcomingEventChecker: #please help me i'm going insane
    def __init__(self, current: UpcomingEvents, last: UpcomingEvents):
        self.current_event = current
        self.last_event = last

    @property
    def current(self) -> UpcomingEvents:
        return self.current_event

    @property
    def last(self) -> UpcomingEvents:
        return self.last_event

    @last.setter
    def last(self, value):
        self.last_event = value

    @current.setter
    def current(self, value):
        self.current_event = value

    @property
    def has_changed(self) -> bool:
        return self.current != self.last

    @property
    def changes(self) -> list[Event]:
        return [event for event in self.current.events if event not in self.last.events]

class OngoingEventChecker:
    def __init__(self, current: OngoingEvents, last: OngoingEvents):
        self.current_event = current
        self.last_event = last

    @property
    def current(self) -> OngoingEvents:
        return self.current_event

    @property
    def last(self) -> OngoingEvents:
        return self.last_event

    @last.setter
    def last(self, value):
        self.last_event = value

    @current.setter
    def current(self, value):
        self.current_event = value

    @property
    def has_changed(self) -> bool:
        return self.current != self.last

    @property
    def changes(self) -> list[Event]:
        return [event for event in self.current.events if event not in self.last.events]