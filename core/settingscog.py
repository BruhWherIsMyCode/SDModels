import discord
from discord import option
from discord.ext import commands
from typing import Optional

from core import settings


class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # pulls from model_names list and makes some sort of dynamic list to bypass Discord 25 choices limit
    def model_autocomplete(self: discord.AutocompleteContext):
        return [
            model for model in settings.global_var.model_names
        ]

    @commands.slash_command(name='settings', description='Проверить и изменить мои настройки для этого сервера')
    @option(
        'current_settings',
        bool,
        description='Показать текущие настройки.',
        required=False,
    )
    @option(
        'display_nprompt',
        bool,
        description='Показать исключающие тэги',
        required=False,
    )
    @option(
        'n_prompt',
        str,
        description='Установить исключающие тэги (negative prompt) для этого сервера',
        required=False,
    )
    @option(
        'model',
        str,
        description='Set default data model for image generation',
        required=False,
        autocomplete=discord.utils.basic_autocomplete(model_autocomplete),
    )
    @option(
        'steps',
        int,
        description='Set default amount of steps for the server',
        min_value=1,
        required=False,
    )
    @option(
        'max_steps',
        int,
        description='Установить максимум шагов для ИИ',
        min_value=1,
        required=False,
    )
    @option(
        'width',
        int,
        description='Установить стандартную ширину картинки для этого сервера',
        required=False,
        choices=[x for x in range(192, 1088, 64)]
    )
    @option(
        'height',
        int,
        description='Установить стандартную высоту картинки для этого сервера',
        required=False,
        choices=[x for x in range(192, 1088, 64)]
    )
    @option(
        'sampler',
        str,
        description='Установить стандартную пробоотборник для этого сервера',
        required=False,
        choices=settings.global_var.sampler_names,
    )
    @option(
        'count',
        int,
        description='Установить стандартное количество картинок за раз для этого сервера',
        min_value=1,
        required=False,
    )
    @option(
        'max_count',
        int,
        description='Установить максимальное количество картинок за раз для этого сервера',
        min_value=1,
        required=False,
    )
    
    @option(
        'clip_skip',
        int,
        description='Установить стандартное значение CLIP Skip для этого сервера (не акутально)',
        required=False,
        choices=[x for x in range(1, 13, 1)]
    )
    async def settings_handler(self, ctx,
                               current_settings: Optional[bool] = True,
                               n_prompt: Optional[str] = 'unset',
                               model: Optional[str] = None,
                               steps: Optional[int] = 1,
                               max_steps: Optional[int] = 1,
                               width: Optional[int] = 1,
                               height: Optional[int] = 1,
                               sampler: Optional[str] = 'unset',
                               count: Optional[int] = None,
                               max_count: Optional[int] = None,
                               clip_skip: Optional[int] = 0,
                               display_nprompt: Optional[bool] = True):
        guild = '% s' % ctx.guild_id
        reviewer = settings.read(guild)
        # create the embed for the reply
        embed = discord.Embed(title="Текущие настройки", description="")
        embed.colour = settings.global_var.embed_color
        current = ''
        new = ''
        set_new = False

        if current_settings:
            cur_set = settings.read(guild)
            for key, value in cur_set.items():
                if value == '':
                    value = ' '
                current = current + f'\n{key} - ``{value}``'
            embed.add_field(name=f'Настройки которые дейстивиельны для этого сервера:', value=current, inline=False)

        # run through each command and update the defaults user selects
        if n_prompt != 'unset':
            settings.update(guild, 'negative_prompt', n_prompt)
            new = new + f'\nNegative prompts: ``"{n_prompt}"``'
            set_new = True

        if model is not None:
            settings.update(guild, 'data_model', model)
            new = new + f'\nData model: ``"{model}"``'
            set_new = True

        if max_steps != 1:
            settings.update(guild, 'max_steps', max_steps)
            new = new + f'\nMax steps: ``{max_steps}``'
            # automatically lower default steps if max steps goes below it
            if max_steps < reviewer['default_steps']:
                settings.update(guild, 'default_steps', max_steps)
                new = new + f'\nDefault steps is too high! Lowering to ``{max_steps}``.'
            set_new = True

        if width != 1:
            settings.update(guild, 'default_width', width)
            new = new + f'\nWidth: ``"{width}"``'
            set_new = True

        if height != 1:
            settings.update(guild, 'default_height', height)
            new = new + f'\nHeight: ``"{height}"``'
            set_new = True

        if sampler != 'unset':
            settings.update(guild, 'sampler', sampler)
            new = new + f'\nSampler: ``"{sampler}"``'
            set_new = True

        if max_count is not None:
            settings.update(guild, 'max_count', max_count)
            new = new + f'\nMax count: ``{max_count}``'
            # automatically lower default count if max count goes below it
            if max_count < reviewer['default_count']:
                settings.update(guild, 'default_count', max_count)
                new = new + f'\nЭэээ, не, слишком много картинок хочешь, понижаю до - ``{max_count}``.'
            set_new = True

        if clip_skip != 0:
            settings.update(guild, 'clip_skip', clip_skip)
            new = new + f'\nCLIP skip: ``{clip_skip}``'
            set_new = True

        # review settings again in case user is trying to set steps/counts and max steps/counts simultaneously
        reviewer = settings.read(guild)
        if steps != 1:
            if steps > reviewer['max_steps']:
                new = new + f"\nМаксимально количество шагов ``{reviewer['max_steps']}``! Ты не можешь поставить число больше этого!"
            else:
                settings.update(guild, 'default_steps', steps)
                new = new + f'\nSteps: ``{steps}``'
            set_new = True

        if count is not None:
            if count > reviewer['max_count']:
                new = new + f"\nМаксимально количество одновременных картинок ``{reviewer['max_count']}``! Ты не можешь поставить число больше этого!"
            else:
                settings.update(guild, 'default_count', count)
                new = new + f'\nCount: ``{count}``'
            set_new = True

        if display_nprompt is not None:
            settings.update(guild, 'display_nprompt', display_nprompt)
            new = new + f'\nDisplay negative prompt: ``"{display_nprompt}"``'
            set_new = True

        if set_new:
            embed.add_field(name=f'New defaults', value=new, inline=False)

        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(SettingsCog(bot))
