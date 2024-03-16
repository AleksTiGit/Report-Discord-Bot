import disnake
from disnake.ext import commands
import sqlite3
from app import bot

class RoleAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='addrole', description='Добавить роль юзеру')
    @commands.has_guild_permissions(manage_roles=True)
    async def addrole(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: disnake.Role):    
        try:
            try:
                conn = sqlite3.connect('MrPi.db')
                bd = conn.cursor()
                bd.execute('SELECT log_id FROM servers WHERE guild_id = ?', (inter.guild.id,))
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

            await member.add_roles(role)
            await inter.response.send_message(f'_Успешно\nУчастнику {member.mention} выдана роль {role.mention}_', ephemeral=True)
            embed = disnake.Embed(
                title='На сервере произошла выдача роли',
                description=f'Участнику {member.mention} была выдана роль {role.mention}',
                color=disnake.Color.from_rgb(255,255,0))
            await logs.send(embed=embed)
        except Exception:
            embed_EXC2 = disnake.Embed(
                title='Не удалось(',
                description='Ваша роль или роль бота ниже роли, которую надо дать участнику (либо у вас ошибка выше 😉)\nТакже вы возможно пытаетесь выдать роль определённого бота, что невозможно',
                color=disnake.Color.from_rgb(255,0,0))
            await inter.send(embed=embed_EXC2, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(RoleAdd(bot))