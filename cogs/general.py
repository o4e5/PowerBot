import json
import os
import platform
import random
import sys

import aiohttp
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json'이 존재하지 않습니다! 추가하고 다시 시도하세요.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="일반"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="정보", aliases=["봇 정보"])
    async def info(self, context):
        """
        이 봇에 대한 정보를 불러와요.
        """
        embed = discord.Embed(
            description="이 봇은 디스코드의 깃허브 템플릿을 참고했어요!",
            color=0x42F56C
        )
        embed.set_author(
            name="봇 정보"
        )
        embed.add_field(
            name="개발자 :",
            value="04e5#1731",
            inline=True
        )
        embed.add_field(
            name="파이썬 버전 :",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="접두사 :",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.set_footer(
            text=f"이 메시지는 '{context.message.author}'' 님으로부터 요청되었어요."
        )
        await context.send(embed=embed)

    @commands.command(name="서버정보")
    async def serverinfo(self, context):
        """
        이 서버에 대한 정보를 불러와요.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**서버 이름 :**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="멤버 수 :",
            value=server.member_count
        )
        embed.add_field(
            name=f"역할 : ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"만들어진 시간 : {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="핑")
    async def ping(self, context):
        """
        봇이 살아 있는지 확인해요.
        """
        embed = discord.Embed(
            title="데이터 처리 속도 :",
            description=f"봇 지연 시간은 {round(self.bot.latency * 1000)}ms입니다!",
            color=0x42F56C
        )
        await context.send(embed=embed)

    @commands.command(name="초대")
    async def invite(self, context):
        """
        디스코드 서버에 초대할 수 있어요.
        """
        embed = discord.Embed(
            description=f"저를 초대하려면 [여기](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263)에서 초대할 수 있어요.",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("메시지를 보냈어요!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(name="투표")
    async def poll(self, context, *, title):
        """
        투표할 수 있는 설문조사를 만들어요. 명령어 뒤에 투표 주제를 쓰세요!
        """
        embed = discord.Embed(
            title="새로운 투표가 만들어졌어요!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"이 투표는 {context.message.author}로부터 만들어졌어요."
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="대화")
    async def eight_ball(self, context, *, question):
        """
        저와 아무말 대화를 할 수 있어요!
        """
        answers = ['심심해', '헤헿']
        embed = discord.Embed(
            title="**대답 :**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"질문 : {question}"
        )
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))
