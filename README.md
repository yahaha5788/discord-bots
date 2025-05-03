# PolaroidSupercolorInstantCamera
### A bot for infinitely customizable color roles!

The Polaroid is a discord bot made for color roles. It allows for any user to have their own custom username color through a role (ex. sc.00FFFF)

## How it works
### Role creation
The bot creates roles at the default position (bottom) as discord.py does not allow for creating a role at a position. The bot then edits the roles position. If the role if being created but not edited, it is possible that the bot is experiencing laterncy or does not have apt permissions.\
The bot uses "sc." to identify supercolor roles. This may be changed in the future. 

### `p!supercolor <hexcode>` 
This is the command for getting a custom color. It will create a role for the hexcode, or it will add the role to the user if it already exists.
Abbreviated by p!sc

### `p!clearcolor`
Clears the custom color from a user. It removes the role, and deletes it if nobody else has the role.

### `p!currentcolor`
Sends the user's current supercolor role, with a command to copy for the role.

### `p!copycolor` 
