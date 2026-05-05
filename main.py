import os

import discord
import wavelink
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

LAVALINK_HOST = os.getenv("LAVALINK_HOST", "127.0.0.1")
LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", "2333"))
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")
LAVALINK_SECURE = os.getenv("LAVALINK_SECURE", "false").lower() == "true"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="0.0", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    scheme = "https" if LAVALINK_SECURE else "http"
    uri = f"{scheme}://{LAVALINK_HOST}:{LAVALINK_PORT}"

    node = wavelink.Node(
        uri=uri,
        password=LAVALINK_PASSWORD,
    )

    await wavelink.Pool.connect(
        nodes=[node],
        client=bot,
    )

    print(f"Connected to Lavalink: {uri}")


@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("你要先進語音頻道。")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(cls=wavelink.Player)

    await ctx.send(f"已加入：{channel.name}")


@bot.command()
async def play(ctx, *, query: str):
    if not ctx.author.voice:
        await ctx.send("你要先進語音頻道。")
        return

    player: wavelink.Player | None = ctx.voice_client

    if player is None:
        player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

    tracks = await wavelink.Playable.search(query)

    if not tracks:
        await ctx.send("找不到歌曲。")
        return

    track = tracks[0]
    await player.play(track)
    await ctx.send(f"正在播放：{track.title}")


@bot.command()
async def pause(ctx):
    player: wavelink.Player | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.pause(True)
    await ctx.send("已暫停。")


@bot.command()
async def resume(ctx):
    player: wavelink.Player | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.pause(False)
    await ctx.send("繼續播放。")


@bot.command()
async def stop(ctx):
    player: wavelink.Player | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.stop()
    await ctx.send("已停止播放。")


@bot.command()
async def leave(ctx):
    player: wavelink.Player | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.disconnect()
    await ctx.send("已離開語音頻道。")


bot.run(TOKEN)