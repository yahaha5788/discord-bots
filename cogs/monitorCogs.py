import json
import discord
from discord.ext import commands, tasks

from misc.templates import unplayed_event_template, UpcomingEvents, OngoingEvents, Event
from query_stuff import queries

from misc.config import EMBED_COLOR, set_footer, commandattrs, add_app_command


class MonitorCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.FOLLOWED_TEAMS_ONGOING_EVENTS: dict[str, OngoingEventChecker] = {}
        self.FOLLOWED_TEAMS_UPCOMING_EVENTS: dict[str, UpcomingEventChecker] = {}

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.designatechannel)
        add_app_command(self.bot)(self.follow)
        add_app_command(self.bot)(self.unfollow)

    async def startNotificationLoop(self):
        self.setEvents()
        await self.sendNotifications.start()

    def setEvents(self):
        with open('../bot/following.json', 'r') as following:
            followed_teams: dict[str, list[str]] = json.load(following)
            for numbers in followed_teams.values():
                for number in numbers:
                    data, success = queries.ongoing_events(number)
                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number] = OngoingEventChecker(data, data)
                    data, success = queries.upcoming_events(number)
                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number] = UpcomingEventChecker(data, data)

    @commandattrs(
        category='Monitor',
        description="Follows a team. Harold will send notifications every hour if the team's events have changed",
        brief="Follows a team",
        usage=f"/follow <number>",
        param_guide={
            '<number>': 'The number of the team to follow.'
        },
        name='follow'
    )
    async def follow(self, interaction: discord.Interaction, number: int):
        guild_id = str(interaction.guild_id)

        with open('../bot/following.json', 'r+') as following, open('../bot/channel_des.json', 'r') as channel_des:
            followed_teams: dict[str, list[str]] = json.load(following)
            channels: dict[str, int] = json.load(channel_des)

            if guild_id not in channels.keys():
                await interaction.response.send_message(f"You have not designated a channel to send notifications in. Run /designatechannel in a channel to set that channel as the notification channel")

            if guild_id not in followed_teams.keys():
                followed_teams[guild_id] = []

            if number in followed_teams[guild_id]:
                await interaction.response.send_message(f"You are already following Team {number}, {queries.name_from_number(number)}")
                return

            followed_teams[guild_id].append(number)
            following.seek(0)
            json.dump(followed_teams, following, indent=4)
            following.truncate()

        await interaction.response.send_message(f"You are now following Team {number}, {queries.name_from_number(number)}")

    @commandattrs(
        category='Monitor',
        description='Unfollows a team. The guild will stop receiving notifications about the team..',
        brief="Unfollows a team.",
        usage=f"/unfollow <number>",
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='unfollow'
    )
    async def unfollow(self, interaction: discord.Interaction, number: int):
        guild_id = str(interaction.guild_id)

        with open('../bot/following.json', 'r+') as following:
            followed_teams: dict[str, list[str]] = json.load(following)

            if guild_id not in followed_teams.keys():
                await interaction.response.send_message('You are not following any teams')
                return

            if number not in followed_teams[guild_id]:
                await interaction.response.send_message(f"You are not following {number}.")
                return

            followed_teams[guild_id].remove(number)
            following.seek(0)
            json.dump(followed_teams, following, indent=4)
            following.truncate()

        await interaction.response.send_message(f"You are no longer following Team {number}, {queries.name_from_number(number)}")

    @commandattrs(
        category='Monitor',
        description='Designates the channel for hourly notifications to be sent about followed teams.',
        brief="Sets the channel where notifications will be sent.",
        usage=f"/designatechannel",
        name='designatechannel'
    )
    async def designatechannel(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        channel_id = interaction.channel_id

        with open('../bot/channel_des.json', 'r+') as channel_des:
            channels: dict[str, int] = json.load(channel_des)
            channels[guild_id] = channel_id

            channel_des.seek(0)
            json.dump(channels, channel_des, indent=4)
            channel_des.truncate()

        await interaction.response.send_message("Notifications for teams you are following will show up here.")

    @tasks.loop(hours=1)
    async def sendNotifications(self):

        await self.bot.wait_until_ready()

        with open('../bot/channel_des.json', 'r') as channels, open('../bot/following.json', 'r') as following:
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

                    data, success = queries.upcoming_events(number)
                    if not success:
                        continue

                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].last = self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].current
                    self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].current = data

                    if self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].has_changed:
                        events = self.FOLLOWED_TEAMS_UPCOMING_EVENTS[number].changes
                    else:
                        continue

                    title = f"Team {number}, {queries.name_from_number(number)} has a new event!"
                    desc = ""

                    for event in events:
                        desc = desc + unplayed_event_template(event) + "\n"

                    unplayed_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                    set_footer(unplayed_notif_embed)

                    await channel.send(embed=unplayed_notif_embed)


                    data, success = queries.ongoing_events(number)
                    if not success:
                        continue

                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].last = self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].current
                    self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].current = data

                    if self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].has_changed:
                        events = self.FOLLOWED_TEAMS_ONGOING_EVENTS[number].changes
                    else:
                        continue

                    title = f"Team {number}, {queries.name_from_number(number)} is currently playing in an event!"
                    desc = ""

                    for event in events:
                        desc = desc + unplayed_event_template(event) + "\n"

                    ongoing_notif_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
                    set_footer(ongoing_notif_embed)

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