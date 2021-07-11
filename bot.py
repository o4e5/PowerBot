import json
import os
import platform
import random
import sys
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json'이 존재하지 않습니다! 추가하고 다시 시도하세요.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)

# 이 코드는 봇이 준비되었을 때 실행됩니다. 
@bot.event
async def on_ready():
    print(f"다음으로 로그인했습니다. ' {bot.user.name} '")
    print(f"Discord.py 버전 : {discord.__version__}")
    print(f"파이썬 버전 : {platform.python_version()}")
    print(f"실행 위치 : {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

# 봇의 상태 메시지 설정
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [f"{config['bot_prefix']}도움"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

# 사용자 정의 도움말 명령을 생성할 수 있도록 discord.py의 기본 도움말 명령을 제거합니다. 
bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"확장 로드됨 : {extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"확장 로드에 실패함 {extension}\n{exception}")

# 이 이벤트의 코드는 접두어가 있든 없든 누군가 메시지를 보낼 때마다 실행됩니다.
@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    with open("blacklist.json") as file:
        blacklist = json.load(file)
    if message.author.id in blacklist["ids"]:
        return
    await bot.process_commands(message)

# 이 이벤트의 코드는 명령이 *성공적으로* 실행될 때마다 실행됩니다.
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"{ctx.guild.name}에서 {executedCommand} 실행됨 ({ctx.message.guild.id} {ctx.message.author} {ctx.message.author.id}")

# 이 이벤트의 코드는 유효한 명령이 오류를 잡을 때마다 실행됩니다.
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="천천히 보내주세요. 시끄러워요..;;",
            description=f"다음에서 이 명령을 다시 사용할 수 있습니다. {f'{round(hours)}시간' if round(hours) > 0 else ''} {f'{round(minutes)}분' if round(minutes) > 0 else ''} {f'{round(seconds)}초' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="오류!",
            description="권한이 없어요.ㅠㅠ `" + ", ".join(
                error.missing_perms) + "` 역할이 있어야 명령어를 실행할 수 있어요!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="오류!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

bot.run(config["token"])