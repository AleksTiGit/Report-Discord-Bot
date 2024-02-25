import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
from app import bot
import sqlite3

class Mute(commands.Cog):
  def __init__(self, bot: commands.InteractionBot):
      self.bot = bot

  @commands.slash_command(name='mute', description='Замьютить участника')
  @commands.has_guild_permissions(moderate_members=True)
  async def timeout(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member,  time: int, reason: str, timeformat: str=commands.Param(choices=['minutes', 'hours', 'days'])):
        try:  
          conn = sqlite3.connect('MrPi.db')
          bd = conn.cursor()
          bd.execute('SELECT log_id, invite FROM servers WHERE guild_id = ?', (inter.guild.id,))
          bd_par = bd.fetchone()
          log_channel = bd_par[0]
          invite = bd_par[1]
          conn.close()


          if timeformat == 'minutes':
            time_mute = datetime.now() + timedelta(minutes=time)
            time_word = 'минут'
          if timeformat == 'hours':
            time_mute = datetime.now() + timedelta(hours=time)
            time_word = 'часов'
          if timeformat == 'days':
            time_mute = datetime.now() + timedelta(days=time)
            time_word = 'дней'

          invite = await bot.fetch_invite(invite)

          embed_mute_ls = disnake.Embed(
              title=f'Вас замьютили на сервере {invite.guild.name}',
              description=f'Причина {reason}\nСрок действия наказания: {time} {time_word}',
              color=disnake.Color.from_rgb(255,0,0))
        
          channel = bot.get_channel(int(log_channel))

          embed_mute = disnake.Embed(
              title='Мьют на сервере!!!',
              description=f'Нарушитель: {member.mention}\nПричина: {reason}\nСрок действия наказания: {time} {time_word}',
              color=disnake.Color.from_rgb(255,0,0))

          await inter.send(content=f'_Успешно\nУчастник {member.mention} замьючен_', ephemeral=True)
          await channel.send(embed=embed_mute)
          
          try:
            await member.send(embed=embed_mute_ls)
          except disnake.HTTPException:
            pass

          await member.timeout(reason=reason, until=time_mute)
        except Exception:
            embed_TE = disnake.Embed(
                title='Не удалось(',
                description='Для того, чтобы использовать бота администратор сервера должен его настроить. Если же бот настроен, то значит в его настрйке есть ошибка. Сообщите ему об этом!',
                color=disnake.Color.from_rgb(255,0,0))
            await inter.send(embed=embed_TE, ephemeral=True)

def setup(bot: commands.InteractionBot):
  bot.add_cog(Mute(bot))