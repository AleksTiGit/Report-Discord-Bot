from disnake.ext import commands
import disnake

intents = disnake.Intents.default()
intents.typing = False
intents.presences= False
intents.messages = True

bot = commands.Bot(command_prefix='/',intents=intents, activity=disnake.Game(name='GAME'))

@bot.slash_command(name='report', description='Подать жалобу.')
async def report(ctx, link: str):
    embed_chat = disnake.Embed(
        title='Репорт отправлен',
        description='Стафф ближайшем времени накажет нарушителя',
        color=disnake.Color.from_rgb(0, 77, 255))
    embed_report = disnake.Embed(title = 'Репорт',
                          description =f"[Ссылка на сообщение нарушителя]({link})\n<@&ROLE_ID> примите меры",
                          color=disnake.Color.from_rgb(255,0,0))
    
    channel = bot.get_channel(CHANNEL_ID)

    await ctx.send(embed=embed_chat, ephemeral=True)
    await channel.send(embed=embed_report)

@bot.slash_command(name='help', description='Помощь с отправкой репорта.')
async def help(ctx):
    embed = disnake.Embed(title='Помощь с отправкой репорта',
                          description='Для отправки репорта, вам следует использовать команду```/report```\nВ параметре ```link``` вы вставляете ссылку на сообщение нарушителя.',
                          color=disnake.Color.from_rgb(255,255,255)) 
    await ctx.send(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot is online: {bot.user}')

bot.run('TOKEN')