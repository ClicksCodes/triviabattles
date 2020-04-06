import discord
from discord.ext import commands


class NotInGuildError(Exception):
    def __init__(self, *args):
        print(
            "I don't appear to be in my master guild. Constants could not be initialized properly. Proceed with caution"
        )
        for arg in args:
            print(repr(arg))


class Constants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if self.bot.is_ready():
            self.on_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        guild = 684492926528651336
        roles = {
            "Owners": 684493117017161963,
            "Moderators": 686310450618695703,
            "Helpers": 686317204752302091,
            "Translators": 691778934471131136,
            "Namers": 694271523363488176
        }

        self.bot.set(
            "guild",
            self.bot.get_guild(guild)
        )

        if not self.bot.guild:
            raise NotInGuildError(f"Not in guild ID {guild}, have I been kicked or has it been deleted?")

        self.bot.set(
            "staff_roles",
            {}
        )

        for role, role_id in roles.items():
            found_role = self.bot.guild.get_role(role_id)
            if found_role:
                self.bot.staff_roles[role] = found_role
            else:
                print(f"The {role} role (ID {role_id}) was not found. Ignoring...")

        self.bot.set(
            "constants_initialized",
            True
        )

        print("Initialization completed!")


def setup(bot):
    bot.set(
        "constants_initialized",
        False
    )

    bot.set(
        "colors",
        {
            "error": discord.Color(0xf44336),
            "success": discord.Color(0x8bc34a),
            "status": discord.Color(0x3f51b5),
            "info": discord.Color(0x212121),
            "dev": discord.Color(0xFFC107)
        }
    )

    bot.set(
        "emotes",
        {
            "1": "<:purple:696711835176403015>",
            "2": "<:red:696711835662942260>",
            "3": "<:yellow:696711835138654258>",
            "4": "<:green:696711835839102987>"
        }

    bot.add_cog(
        Constants(bot)
    )
