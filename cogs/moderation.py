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


class moderation(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='추방', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason="사유를 명시하지 않음"):
        """
        서버에서 유저를 추방해요.
        """
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="오류!",
                description="어드민 역할이 있어야 해요.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="유저가 추방되었어요!",
                    description=f"**{context.message.author}**님이 **{member}**님을 추방시켰어요 !",
                    color=0x42F56C
                )
                embed.add_field(
                    name="사유 :",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"당신은 **{context.message.author}**님에게 추방당했어요!\n사유 : {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="오류!",
                    description="사용자를 추방하는 동안 오류가 발생했어요. 내 역할이 추방하려는 사용자의 역할 위에 있는지 확인하세요!",
                    color=0xE02B2B
                )
                await context.message.channel.send(embed=embed)

    @commands.command(name="닉네임")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, nickname=None):
        """
        서버 별명을 변경해요.
        """
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="별명을 성공적으로 바꿨어요!",
                description=f"이제 **{member}**님의 별명은 '**{nickname}**' 입니다!",
                color=0x42F56C
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="오류!",
                description="사용자를 추방하는 동안 오류가 발생했어요. 내 역할이 추방하려는 사용자의 역할 위에 있는지 확인하세요!",
                color=0xE02B2B
            )
            await context.message.channel.send(embed=embed)

    @commands.command(name="벤")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason="명시되지 않았어요."):
        """
        이 서버에서 해당 유저를 벤해요.
        [ 중요 ] 아직 벤 된 유저를 다시 되돌릴 능력이 없어요.
        신중하게 생각해 주세요!
        """
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="오류!",
                    description="사용자에게 관리자 권한이 있어요.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="성공적으로 벤되었어요!",
                    description=f"**{member}**님은 **{context.message.author}**님에게 벤을 당했어요!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="사유 :",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"**{context.message.author}님에게 서버에서 벤 처리 되었어요. **!\n사유 : {reason}")
        except:
            embed = discord.Embed(
            )
            await context.send(embed=embed)

    @commands.command(name="경고")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, context, member: discord.Member, *, reason="명시되지 않았어요."):
        """
        개인 메시지로 사용자를 경고해요.
        """
        embed = discord.Embed(
            title="성공적으로 유저가 경고되었어요!",
            description=f"**{member}**님은 **{context.message.author}**님에게 경고되었어요!",
            color=0x42F56C
        )
        embed.add_field(
            name="사유 :",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"**{context.message.author}**님이 해당 서버에서 경고했어요.!\n사유 : {reason}")
        except:
            pass

    @commands.command(name="삭제")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def purge(self, context, amount):
        """
        해당 채널에서 지정된 수 만큼 메시지를 삭제해요.
        """
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="오류!",
                description=f"`{amount}`는 올바른 값이 아니에요.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="오류!",
                description=f"`{amount}`는 올바른 값이 아니에요.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        purged_messages = await context.message.channel.purge(limit=amount)
        embed = discord.Embed(
            title="채팅이 삭제되었어요!",
            description=f"**{context.message.author}**님이 **{len(purged_messages)}**만큼의 채팅을 청소했어요!",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(moderation(bot))
