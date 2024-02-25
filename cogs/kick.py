import disnake
from disnake.ext import commands
from app import bot
import sqlite3

class Kick(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
    
    @commands.slash_command(name='kick', description='Выгнать участника')
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        try:  
          conn = sqlite3.connect('MrPi.db')
          bd = conn.cursor()
          bd.execute('SELECT log_id, invite FROM servers WHERE guild_id = ?', (inter.guild.id,))
          bd_par = bd.fetchone()
          log_channel = bd_par[0]
          invite = bd_par[1]
          conn.close()
        
          invite = await bot.fetch_invite(invite)

          embed_kick=disnake.Embed(
            title='На сервере произошёл кик',
            description=f'Нарушитель: {member.mention}\nПричина: {reason}',
            color=disnake.Color.from_rgb(255,0,0))
     
          embed_kick_ls = disnake.Embed(
            title=f'Вас кикнули с сервера {invite.guild.name}',
            description=f'Причина: {reason}',
            color=disnake.Color.from_rgb(255,0,0))
        
          channel = bot.get_channel(int(log_channel))

          await inter.send(content=f'_Успешно\nУчастник {member.mention} был выгнан с сервера_', ephemeral=True)
          await channel.send(embed=embed_kick)
          
          try:
            await member.send(embed=embed_kick_ls)
          except disnake.HTTPException:
             pass
          
          await member.kick(reason=reason) 
        except Exception:
          embed_TE = disnake.Embed(
            title='Не удалось(',
            description='Для того, чтобы использовать бота администратор сервера должен его настроить. Если же бот настроен, то значит в его настрйке есть ошибка. Сообщите ему об этом!',
            color=disnake.Color.from_rgb(255,0,0))
          await inter.send(embed=embed_TE, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Kick(bot))