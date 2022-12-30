import discord
from discord.ext import commands
from discord.ui import View

from core import settings


class TipsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        custom_id="button_tips",
        label="Подсказки")
    async def button_tips(self, button, interaction):

        embed_tips = discord.Embed(title="Подсказки", description="")
        embed_tips.colour = settings.global_var.embed_color
        embed_tips.add_field(name="Шаги (steps)",
                             value="Показывает сколько шагов обработки нужно ИИ, чтобы получить картинку. "
                                   "Больше шагов обработки - лучше результат (правда... это не всегда так работает)",
                             inline=False)
        embed_tips.add_field(name="Уровень точности (CFG scale)",
                             value="Данный параметр показывает, насколько точно должно соответствовать изображение введенным словам. Чем больше значение, "
                                   "тем более ближе будет к запросу, чем меньше - тем более креативно сделает ИИ (иногда даже что-то получится годное).",
                             inline=False)
        embed_tips.add_field(name="Ключ генерации т.е ключ-семечко (seed)",
                             value="Данный ключ содержит в себе информацию о созданном изображении. "
                                   "С его помощью можно сделать такое же изображение, либо его вариации",
                             inline=False)
        embed_tips.add_field(name="Порядок слов",
                             value="Порядок слов влияет на изображение. Если будет 'кошка, собака', то ИИ будет предпочитать делать изображение ближе к кошке, чем к собаке.\n"
                                   "При долгом создании, ИИ начинает игнорировать слова, которые ближе к концу введенного списка (и понятно зачем он так делает).",
                             inline=False)
        embed_tips.add_field(name="Предпочтения",
                             value="Данный параметр помогает ИИ понять ваши желание касательно картинки\n"
                                    "`(слово)`- каждые `()` увеличивают вниманиее ИИ к `слово` в 1.1 раз\n`[слово]`- каждые `[]` понижают "
                                   "внимание к `слово` в 1.1 раз\n`(слово:1.5)`-увеличивает внимание к `слово` в 1.5 раза\n`("
                                   "слово:0.25)`- понижает внимание к `слово` в 4 раза\n Если в слове (без параметров увеличивающих вниманиее ИИ к слову) есть скобки, то выделять их нужно с помощью \" \ \" - `\(word\)`",
                             inline=False)
        embed_tips.add_field(name="Комбинирование",
                             value="`[слово1|слово2]`\nПри создании изображения, ИИ будет брать что-то общее между введеными словами на кажждом шаге "
                                   "Последовательность слов влияет на результат.",
                             inline=True)
        embed_tips.set_footer(text='Используя ❌ можно удалить картинку, если вам не понравилось (либо вышел ужас)')

        await interaction.response.edit_message(embed=embed_tips)

#    @discord.ui.button(
#        custom_id="button_styles",
#        label="Список стилей")
#    async def button_style(self, button, interaction):
#
#        style_list = ''
#        for key, value in settings.global_var.style_names.items():
#            if value == '':
#                value = ' '
#            style_list = style_list + f'\n{key} - ``{value}``'
#        embed_styles = discord.Embed(title="Список досупных стилей", description=style_list)
#        embed_styles.colour = settings.global_var.embed_color
#
#        await interaction.response.edit_message(embed=embed_styles)

    @discord.ui.button(
        custom_id="button_model",
        label="Список моделей")
    async def button_model(self, button, interaction):

        model_list = ''
        for key, value in settings.global_var.model_names.items():
            if value == '':
                value = ' '
            # strip any folders from model full name
            value = value.split('/', 1)[-1].split('\\', 1)[-1]

            model_list = model_list + f'\n{key}'
        embed_model = discord.Embed(title="Список досупных моделей", description=model_list)
        embed_model.colour = settings.global_var.embed_color

        await interaction.response.edit_message(embed=embed_model)

    @discord.ui.button(
        custom_id="button_about",
        label="Обо мне")
    async def button_about(self, button, interaction):

        embed_about = discord.Embed(title="Это я!",
                                    description=f"Приветик. Я CucumberSeller, то есть бот на платформе Discord\n"
                                                f"Больше я о себе и не могу рассказать....\n"
                                                f"Текущая версия бота - 1.0.1\n"
                                                f"Не судите нас строго, все ошибки будут исправлены в будущем. \":3\n"
                                                f"За вопросами и помощью смело обращайтесь к ZyaBlik#7695 (パン из ＨＯＮＫＡＩ) или-же к Nuck Noggers#0333\n")
        embed_about.colour = settings.global_var.embed_color

        embed_about.set_footer(text='Короче, крутого дня вам! \":3')

        await interaction.response.edit_message(embed=embed_about)

class TipsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TipsView())

    @commands.slash_command(name="tips", description="Подсказки")
    async def tips(self, ctx):
        first_embed = discord.Embed(title='Выбери кнопку нужную тебе кнопку :3')
        first_embed.colour = settings.global_var.embed_color

        await ctx.respond(embed=first_embed, view=TipsView(), ephemeral=True)


def setup(bot):
    bot.add_cog(TipsCog(bot))
