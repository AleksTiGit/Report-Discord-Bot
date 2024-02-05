from disnake.ext import commands
import disnake
from disnake import Guild
import sqlite3

def create():
    conn = sqlite3.connect('MrPi.db')
    bd = conn.cursor()
    bd.execute('''CREATE TABLE IF NOT EXISTS servers
               (guild_id INTEGER PRIMARY KEY, ping_id TEXT, channel_id TEXT, owner_id TEXT)''')
    conn.commit()
    conn.close()

intents = disnake.Intents.default()
intents.typing = False
intents.presences= False
intents.messages = True
intents.guilds = True

bot = commands.InteractionBot(intents=intents, activity=disnake.Game(name='Кого забанить?)'))

@bot.slash_command(name='settings', description='Настройка бота')
async def set(inter: disnake.ApplicationCommandInteraction, ping_id: str, channel_id: str):
    guild = await bot.fetch_guild(inter.guild.id)
    owner  = guild.owner_id
    conn = sqlite3.connect('MrPi.db')
    bd = conn.cursor()
    bd.execute('INSERT OR REPLACE INTO servers (guild_id,  owner_id) VALUES (?,?)', (inter.guild.id, owner))
    conn.commit()
    conn.close()

    if inter.author.id == owner:
        conn = sqlite3.connect('MrPi.db')
        db = conn.cursor()
        db.execute('INSERT OR REPLACE INTO servers (guild_id,  ping_id, channel_id) VALUES (?,?,?)', (inter.guild.id, ping_id, channel_id))
        conn.commit()
        conn.close()
      
        embed_own = disnake.Embed(
            title='Значения успешно добавлены',
            description='Теперь на сервере можно пользоваться слеш-командой **report**',
            color=disnake.Color.from_rgb(255,255,255))
        await inter.response.send_message(embed=embed_own, ephemeral=True)
    else:
        embed_not = disnake.Embed(
            title='Вы не можете использовать эту команду',
            description='Причина: вы не владелец (овнер) сервера',
            color=disnake.Color.from_rgb(255,0,0))
        await inter.response.send_message(embed=embed_not, ephemeral=True)

@bot.slash_command(name='report', description='Подать жалобу')
async def report(inter: disnake.ApplicationCommandInteraction, link: str):
    try:    
        conn = sqlite3.connect('MrPi.db')
        bd = conn.cursor()
        bd.execute('SELECT ping_id, channel_id FROM servers WHERE guild_id = ?', (inter.guild.id,))
        bd_par = bd.fetchone()
        role_id = bd_par[0]
        rep_channel = bd_par[1]
        conn.close()
    except TypeError:
        embed_TE = disnake.Embed(
            title='Не удалось(',
            description='Для того, чтобы использовать бота владелец сервера должен его настроить. Сообщите ему об этом!',
            color=disnake.Color.from_rgb(255,0,0))
        await inter.send(embed=embed_TE, ephemeral=True)


    try:
        embed_chat = disnake.Embed(
            title='Репорт отправлен',
            description='Стафф ближайшем времени накажет нарушителя',
            color=disnake.Color.from_rgb(0, 77, 255))
        

        embed_report = disnake.Embed(title = 'Репорт',
                          description =f'[Ссылка на сообщение нарушителя]({link})\n<@&{int(role_id)}> примите меры',
                          color=disnake.Color.from_rgb(255,0,0))
    
        await inter.send(embed=embed_chat, ephemeral=True)
        channel = bot.get_channel(int(rep_channel))
        await channel.send(embed=embed_report)
    except AttributeError or UnboundLocalError:
        embed_AE = disnake.Embed(
            title='Не удалось(',
            description='Владелец сервера не настроил бота или указал неправильные данные. Сообщите ему об этом!',
            color=disnake.Color.from_rgb(255,0,0))
        await inter.response.send_message(embed=embed_AE)

@bot.slash_command(name='help', description='Помощь с отправкой репорта')
async def help(inter: disnake.ApplicationCommandInteraction):
    embed_help = disnake.Embed(title='Помощь с отправкой репорта',
                          description='**Для пользователей:**\nДля отправки репорта, вам следует использовать команду```/report```\nВ параметре ```link``` вы вставляете ссылку на сообщение нарушителя.\n**Для администраторов сервера:**\nДля настройки бота вам понадобится использовать команду```/settings```. Эту команду может исользовать только овнер (владелец) сервера. В параметре ```ping_id``` вы указываете роль, которую надо пинговать при наличии репорта; а в параметре ```channel_id``` вы указываете канал, в который будут отправляться сообщения о репорте.\n\n[_Сервер поддержки_](https://discord.com/invite/nHD8bpdvR4)',
                          color=disnake.Color.from_rgb(255,255,255)) 
    await inter.response.send_message(embed=embed_help, ephemeral=True)

@bot.slash_command(name='info', description='Информация о боте')
async def infobot(inter: disnake.ApplicationCommandInteraction):
    embed_info = disnake.Embed(
        title='Info Mr.Pi bot',
        description='**V.1.0.0**\nХозяин и создатель: Алекс Титан\nКод бота на GitHub: [тык](https://github.com/AleksTiGit/Report-Discord-Bot)\nСервер поддержки: [тык](https://discord.com/invite/nHD8bpdvR4)\nТелеграмм канал: [тык](https://t.me/kotiki_developeri)\nGitHub: [тык](https://github.com/AleksTiGit)\nYouTube: [тык](https://youtube.com/@KAT_Developers)',
        color=disnake.Color.from_rgb(255,255,255))
    await inter.response.send_message(embed=embed_info)

@bot.event
async def on_ready():
    print(f'Bot is online: {bot.user}')

@bot.event
async def on_guild_remove(guild: Guild):
    conn = sqlite3.connect('MrPi.db')
    bd = conn.cursor()
    bd.execute('DELETE FROM servers WHERE guild_id = ?', (guild.id,))
    conn.commit()
    conn.close()

create()
bot.run(TOKEN)
