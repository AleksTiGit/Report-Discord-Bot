import disnake
from disnake.ext import commands
from app import bot

name_vote = None

class VoteModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label='Имя',
                custom_id='name',
                style=disnake.TextInputStyle.short,
                max_length=100),
            disnake.ui.TextInput(
                label='Первый вариант',
                custom_id = 'first',
                style=disnake.TextInputStyle.short,
                max_length=100),
            disnake.ui.TextInput(
                label='Второй вариант',
                custom_id = 'second',
                style=disnake.TextInputStyle.short,
                max_length=100,),
            disnake.ui.TextInput(
                label='Третий вариант',
                custom_id='third',
                style=disnake.TextInputStyle.short,
                max_length=100,
                required=False),
            disnake.ui.TextInput(
                label='Четвёртый вариант',
                custom_id='fourth',
                style=disnake.TextInputStyle.short,
                max_length=100,
                required=False)]
        super().__init__(
            title='Создание голосования',
            custom_id='vote',
            components=components)
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title=inter.text_values['name'],
            color=disnake.Color.blue())
        embed.add_field(name='Первый вариант [1️⃣]', value=inter.text_values['first'], inline=False)
        embed.add_field(name='Второй вариант [2️⃣]', value=inter.text_values['second'], inline=False)
        if inter.text_values['third'] != '':
            embed.add_field(name='Третий вариант [3️⃣]', value=inter.text_values['third'], inline=False)
        if inter.text_values['fourth'] != '' and inter.text_values['third'] != '':
            embed.add_field(name='Четвёртый вариант [4️⃣]', value=inter.text_values['fourth'], inline=False)
        await inter.send(embed=embed)

        

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='vote', description='Провести голосование')
    async def vote(inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_modal(modal=VoteModal())

def setup(bot: commands.InteractionBot):
    bot.add_cog(Vote(bot))
