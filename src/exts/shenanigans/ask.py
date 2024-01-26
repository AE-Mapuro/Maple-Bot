import random
from interactions import *
from typing import Any
from src.exts.shenanigans.shenanigans import ShenaniganCommands as SC


class Ask(Extension):
    BOT_NAME = 'Grendel'
    # Bots are limited to messages 2000 characters or fewer
    BOT_MSG_LEN_LIM = 2000

    @SC.shenanigans.subcommand(sub_cmd_name='ask', sub_cmd_description=f'Ask {BOT_NAME} a question')
    @slash_option(
        name='question',
        description="Question asked by the user (text)",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name='severity',
        description="Severity of question asked (integer)",
        required=False,
        opt_type=OptionType.INTEGER
    )
    async def askCommand(self, ctx: SlashContext, question: str, severity: int = 1):
        responses = ['', 'No', 'Whyyyy', 'Nani', 'Jes', 'Nani Kore', 'Watashi wa Kotowaru', 'Plz', 'Plz No',
                     'No Violins Plox', 'This is too difficult to answer', '\'agrid\'s back!']
        expressions = ['(ㆆ _ ㆆ)', '⊂(◉‿◉)つ', '•`_´•', 'ʕっ•ᴥ•ʔっ', '(•_•) ( •_•)>⌐■-■ (⌐■_■)', '(｡◕‿‿◕｡)', '(︶︹︶)',
                       '┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻', '(ง •̀_•́)ง', '(ノಠ益ಠ)ノ彡┻━┻', R'¯\_(ツ)_/¯']

        # Generate bot response - two messages:
        # reiteration of the question
        # Before appending question marks, remove any question marks from the end of the input string
        question = question.rstrip('?')
        question_full: str = f"{question}{'?' * severity}"
        # response (randomly generated)
        response: str = f"{random.choice(responses)} {random.choice(expressions)}"

        # Message to be sent when input question is too long
        # TODO This variable may be moved outside function scope
        bot_response_too_long = f'The question is too long and/or the severity is too high. {self.BOT_NAME} is limited to responses {self.BOT_MSG_LEN_LIM} characters or fewer.'

        print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')

        messages: list[Any] = []
        if len(question_full) <= self.BOT_MSG_LEN_LIM:
            messages.append(await ctx.send(question_full))
            messages.append(await ctx.send(response))
        else:
            messages.append(await ctx.send(bot_response_too_long))

        # * Use this as a debug point
        return


def setup(bot):
    Ask(bot)
