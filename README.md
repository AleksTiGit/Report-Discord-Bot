## REPORT-DISCORD-BOT ##
This is a bot for sending reports. Made in Python using the disnake library.
[ADD](https://discord.com/api/oauth2/authorize?client_id=1186355477295157468&permissions=2064000732230&scope=applications.commands%20bot)

## For users: ##
To send a report, use the ```/report``` command. In the ```link``` parameter you insert a link to the offender’s message.
The bot also has moderation commands:
**/ban**;
**/unban**;
**/mute**
**/unmute**
**/kick**

## For server administrators: ##
To configure the bot you will need to use the command ```/settings```. This command can only be used by the server owner. In the ``role_id`` parameter you specify the role that should be pinged when a report is available; and in the ```channel_id``` parameter you specify the channel to which reporting messages will be sent. In the ```log_channel_id``` parameter you specify the channel for sending logs. In the ```invite``` parameter you specify an invitation link to the server (needed to obtain the server name; must be unlimited)
