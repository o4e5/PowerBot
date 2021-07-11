import asyncio
import json
import os
import random
import sys

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType

if not os.path.isfile("config.json"):
    sys.exit("'config.json'이 존재하지 않습니다! 추가하고 다시 시도하세요.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Fun(commands.Cog, name="게임"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="팁")
    @commands.cooldown(1, 86400, BucketType.user)
    async def dailyfact(self, context):
        """
        팁을 가져와요. 영어만 지원합니다.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="오류!",
                        description="API에 문제가 있어요. 나중에 다시 시도해 주세요.",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    self.dailyfact.reset_cooldown(context)

    @commands.command(name="가위바위보")
    async def rock_paper_scissors(self, context):
        """
        이모지를 이용해 가위바위보를 할 수 있어요.
        """
        choices = {
            0: "바위",
            1: "보",
            2: "가위"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="가위바위보!", color=0xF59E42)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**비겼어요!**\n{context.message.author}님이 {user_choice_emote}, 저는 {bot_choice_emote}를 냈어요!"
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**{context.message.author}님이 이겼네요!**\nYou've chosen {user_choice_emote} 저는 {bot_choice_emote}를 냈어요!"
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**{context.message.author}님이 이겼네요!**\nYou've chosen {user_choice_emote} 저는 {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**{context.message.author}님이 이겼네요!**\nYou've chosen {user_choice_emote} 저는 {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="저기... 가위바위보 안해요? ㅠㅠ", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)


def setup(bot):
    bot.add_cog(Fun(bot))