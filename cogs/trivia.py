from discord.ext import commands
import aiohttp
import random
import re


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def question(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://opentdb.com/api.php?amount=1&type=multiple'
            ) as resp:
                response = await resp.json()
                card = response['results'][0]
                answers = (
                        [
                            "- [x] " + card['correct_answer']
                        ] +
                        [
                            "- [ ] " + _card for _card in card['incorrect_answers']
                        ]
                )
                random.shuffle(answers)
                await ctx.send(
                    re.sub(r"^- \[[x ]\]", "- [?]", "\n".join(answers), flags=re.MULTILINE),
                    title=card['question']
                )


def setup(bot):
    bot.add_cog(Trivia(bot))
