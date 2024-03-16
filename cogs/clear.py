import disnake
from disnake.ext import commands
import sqlite3
from app import bot

class ClearMes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='clear', description='Очистить сообщения')
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(inter: disnake.ApplicationCommandInteraction, limit: int):
            try:
                conn = sqlite3.connect('MrPi.db')
                bd = conn.cursor()
                bd.execute('SELECT log_id, invite FROM servers WHERE guild_id = ?', (inter.guild.id,))
                bd_par = bd.fetchone()
                log_channel = bd_par[0]
                conn.close()
                logs = bot.get_channel(int(log_channel))
            except Exception:
                embed_EXC1 = disnake.Embed(
                    title='Не удалось(',
                    description='Для того, чтобы использовать бота администратор сервера должен его настроить.\nЕсли же бот настроен, то значит в его настройке есть ошибка.\nЕсли же бот настроен правильно, то это может быть связано с тем, что бот не имеет доступа к каналу логов, либо роль бота ниже роли участника, которого надо забанить\nТакже проверьте разоешения бота: с версии 1.1.2 для бота требуется разрешение "администратор"\nСообщите администратору об этом!',
                    color=disnake.Color.from_rgb(255,0,0))
                await inter.send(embed=embed_EXC1, ephemeral=True)

            await inter.channel.purge(limit=limit)

            await inter.send(f'_Успешно\nБыло очищено {limit} сообщений_', ephemeral=True)
            embed = disnake.Embed(
                title='На сервере произошла очистка чата',
                description=f'Было очищено {limit} сообщений в канале {inter.channel.mention}\nСообщения двух-недельной давности были пропущены',
                color=disnake.Color.from_rgb(255,255,0))           
            await logs.send(embed=embed)

def setup(bot: commands.InteractionBot): 
     bot.add_cog(ClearMes(bot))