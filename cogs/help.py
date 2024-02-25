import disnake
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name='help', description='Помощь с отправкой репорта и настройкой бота')
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        embed_help = disnake.Embed(title='Помощь с отправкой репорта & настройкой бота',
                          description='**Для пользователей:**\nДля отправки репорта, вам следует использовать команду```/report```\nВ параметре ```link``` вы вставляете ссылку на сообщение нарушителя.\n**Для администраторов сервера:**\nДля настройки бота вам понадобится использовать команду```/settings``` Эту команду может исользовать только администрторы сервера. В параметре ```role_id``` вы указываете роль, которую надо пинговать при наличии репорта; а в параметре ```channel_id``` вы указываете канал, в который будут отправляться сообщения о репорте. В параметре ```log_channel_id``` вы указываете id канала, в который будут отправляться логию В параметре ```invite``` вы указываете ссылку-приглашение на ваш сервер (нужна для получения имени сервера)\nВ боте есть команды для модерациии такие как: ban, mute, unmute, unban\n# Бот в будущем может смениться на другой. Уведомление об этом обязательно будет на нашем ДС сервере.\nТакже мы постараемся уведомить об этом всех через нашего бота\n\n[_Сервер поддержки_](https://discord.com/invite/nHD8bpdvR4)',
                          color=disnake.Color.from_rgb(255,255,255)) 
        await inter.response.send_message(embed=embed_help, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Help(bot))