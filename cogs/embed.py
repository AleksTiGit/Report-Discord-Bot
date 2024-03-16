import disnake
from disnake.ext import commands
import aiohttp
from app import bot

embed_webhook = None
url = None

class EmbedFirstModal(disnake.ui.Modal):
    def __init__(self):
        components=[
            disnake.ui.TextInput(
                label='Укажите заголовок',
                custom_id='title',
                style=disnake.TextInputStyle.short,
                placeholder='Заголовок идёт в начале эмбеда жирным шрифтом'),
            disnake.ui.TextInput(
                label='Введите описание',
                custom_id='description',
                style=disnake.TextInputStyle.long,
                placeholder='Описание - основная центральная часть эмбеда'),
            disnake.ui.TextInput(
                label='Введите цвет эмбеда в RGB коде',
                custom_id='color',
                style=disnake.TextInputStyle.short,
                placeholder='Будет отображаться на компьютерах с левой части (вводить через запятую)',
                max_length=10),
            disnake.ui.TextInput(
                label='Укажите ссылку на изображение',
                custom_id='image',
                style=disnake.TextInputStyle.long,
                placeholder='Изображение будет отображаться в самом низу эмбеда',
                required=False),
            disnake.ui.TextInput(
                label='Укажите ссылку на миниатюру',
                custom_id='icon',
                style=disnake.TextInputStyle.long,
                placeholder='Иконка будет отображаться в левом верхнем углу эмбеда',
                required=False)]
        super().__init__(
            title='Создание эмбеда',
            custom_id='embed_create',
            components=components)
    async def callback(self, inter: disnake.ModalInteraction):
        global embed_webhook
        rgb = [int(num) for num in inter.text_values['color'].split(",")]
        embed_webhook=disnake.Embed(
            title=inter.text_values['title'],
            description=inter.text_values['description'],
            color=disnake.Color.from_rgb(r=rgb[0], g=rgb[1], b=rgb[2]))
        if inter.text_values['image'] != '':
            embed_webhook.set_image(inter.text_values['image'])
        if inter.text_values['icon'] != '':
            embed_webhook.set_thumbnail(inter.text_values['icon'])
        await inter.response.send_message(embed=embed_webhook, ephemeral=True, components=[disnake.ui.Button(label='Send', style=disnake.ButtonStyle.primary, custom_id='send')])

class EmbedCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
    
    @commands.slash_command(name='embed', description='Создать эмбед')
    @commands.has_guild_permissions(manage_webhooks=True)
    async def embed(self, inter: disnake.ApplicationCommandInteraction, url_webhook: str):
        await inter.response.send_modal(modal=EmbedFirstModal())
        global url
        url = url_webhook
    
    @bot.listen('on_button_click')
    async def help_listener(inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'send':
            async with aiohttp.ClientSession() as session:
                webhook = disnake.Webhook.from_url(url, session=session)
                await webhook.send(embed=embed_webhook)

def setup(bot: commands.InteractionBot):
    bot.add_cog(EmbedCommand(bot))