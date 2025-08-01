Harold is a Discord bot for tracking and getting the statistics of First Tech Challenge teams.
##### This is very much a WIP. Although most commands work, there are still many to be made and polished.

## Planned

Event creation for worlds and states events\
Event creation for upcoming events of followed teams\
Automatic updating of followed teams (`updatesLoop.py`)\
`/recentmatches` - get the team's last or most recent match\
`/customstat` - query for specific stats of a team in a specific time period\
`/compareteams` - compare two teams\
`/setstates` - event creation and updating for a state event\
`/trivia` - trivia about FIRST idk

Wrap all commands on start (associate name, usage, and other variables that are given via `@commandattrs` and aren't in normal app commands) instead of every time `/help` is run for optimization

Work on condesing the /worlds command to allow for showing matches without sending the ***ONE EMBED TO RULE THEM ALL***, possibly
splitting into `/worlds <division> <data>` in which `<data>` is "matches" or "teams"