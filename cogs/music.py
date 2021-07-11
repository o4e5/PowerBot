import discord
from discord.ext import commands
import youtube_dl
import os
import sys
from helpers import json_manager
import json

if not os.path.isfile("config.json"):
    sys.exit("'config.json'이 존재하지 않습니다! 추가하고 다시 시도하세요.")
else:
    with open("config.json") as file:
        config = json.load(file)

class music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='🎵-음악')
    await voiceChannel.connect()
    voice = discord.utils.get(commands.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@commands.command()
async def leave(ctx):
    voice = discord.utils.get(commands.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@commands.command()
async def pause(ctx):
    voice = discord.utils.get(commands.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@commands.command()
async def resume(ctx):
    voice = discord.utils.get(commands.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@commands.command()
async def stop(ctx):
    voice = discord.utils.get(commands.voice_clients, guild=ctx.guild)
    voice.stop()

def setup(bot):
    bot.add_cog(music(bot))