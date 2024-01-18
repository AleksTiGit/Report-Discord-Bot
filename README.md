## REPORT-DISCORD-BOT ##
This is a bot for sending reports. When sending the ```/report``` command, you must provide a link to the offender's message.
Made in Python with the disnake library
## FOR DEVELOPERS: ##
Instead of ```GAME``` you insert an activity (what the bot will play; this is indicated in the bot’s profile);

Instead of ```ROLE_ID``` you insert the Id of the role that needs to be pinged when you sent the report;

Instead of ```CHANNEL_ID``` you insert the ID of the channel to which information about reports will be sent;

Instead of ```TOKEN``` you insert your bot token;

If you want to change the colors in embed messages, then replace the RGB code in ```disnake.Color.from_rgb(rgb code)```.
