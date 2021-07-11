import json
import os
import sys
import discord

from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json'이 존재하지 않습니다! 추가하고 다시 시도하세요.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Template(commands.Cog, name="확장"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="테스트")
    async def testcommand(self, context):
        """
        봇이 잘 작동하는지 알아내요.
        """
        embed = discord.Embed(
            title="문제 없음",
            description=f"이것은 제가 고장나지 않았는지 알아내는 것이에요!",
            color=0x42F56C
        )
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Template(bot))
