import aiohttp, asyncio, discord, random
from classes.enums import difficulties, categories
from MiniUtils import minidiscord, data, classes


with open('token.txt') as f:
    token = [line.strip() for line in f]

bot = minidiscord.Bot(
    command_prefix='=',
    case_insensitive=True,
    owner_ids=[317731855317336067, 438733159748599813, 261900651230003201, 421698654189912064],
    activity=discord.Activity(
        name="questions get answered.",
        type=discord.ActivityType.watching
    ),  # We create a discord activity to start up with
    status=discord.Status.dnd
)


async def get_cards(
        amount, difficulty: difficulties.Difficulty = difficulties.Difficulty.ALL,
        category: categories.Category = categories.Category.ALL
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://opentdb.com/api.php?amount={amount}{difficulty.value}{category.value}&type=multiple'
        ) as resp:
            if resp.status == 200:
                response = await resp.json()
                if response['response_code'] == 0:
                    # Returned results successfully
                    return response['results']
                elif response['response_code'] == 1:
                    # The API doesn't have enough questions for your query
                    return 1
                elif response['response_code'] == 2:
                    # Invalid Parameter
                    return 2
                elif response['response_code'] == 3:
                    # Token Not Found
                    return 3
                elif response['response_code'] == 4:
                    # Session Token has returned all possible questions for the specified query
                    return 4


@bot.event
async def on_ready():
    print('ready')


async def print_cards():
    for card in await get_cards(50):
        print(card['question'])
        answers = ["- [x] " + card['correct_answer']] + ["- [ ] " + _card for _card in card['incorrect_answers']]
        random.shuffle(answers)
        print("\n".join(answers))


bot.load_extension("cogs.trivia")

with open('token.txt') as tokens:
    bot.tokens = classes.ObfuscatedDict(line.strip().split(":", 1) for line in tokens.readlines())

bot.run(bot.tokens["discord"])
