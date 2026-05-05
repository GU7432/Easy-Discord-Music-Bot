import os
from collections import deque

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

intents = discord.Intents.default()  # 建立一組預設權限。
intents.message_content = True

bot = commands.Bot(command_prefix="0.0", intents=intents)


# 自定義 Player 類，支援隊列
class MusicPlayer(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.track_queue = deque()


@bot.event
async def on_wavelink_track_end(payload: wavelink.TrackEndEventPayload):
    """歌曲播放結束時自動播放隊列中的下一首"""
    player = payload.player

    if not isinstance(player, MusicPlayer) or payload.reason == "replaced":
        return

    if not player.track_queue:
        return

    next_track = player.track_queue.popleft()
    await player.play(next_track)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    if wavelink.Pool.nodes:
        return

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
        if isinstance(ctx.voice_client, MusicPlayer):
            ctx.voice_client.text_channel = ctx.channel
    else:
        player: MusicPlayer = await channel.connect(cls=MusicPlayer)
        player.text_channel = ctx.channel

    await ctx.send(f"已加入：{channel.name}")


@bot.command()
async def play(ctx, *, query: str):
    if not ctx.author.voice:
        await ctx.send("你要先進語音頻道。")
        return

    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        player = await ctx.author.voice.channel.connect(cls=MusicPlayer)

    tracks = await wavelink.Playable.search(query)

    if not tracks:
        await ctx.send("找不到歌曲。")
        return

    track = tracks[0]

    # 如果當前沒有播放歌曲，直接播放；否則加入隊列
    if player.playing:
        player.track_queue.append(track)
        await ctx.send(f"已加入隊列：{track.title} (隊列中有 {len(player.track_queue)} 首歌曲)")
    else:
        await player.play(track)
        await ctx.send(f"正在播放：{track.title}")


@bot.command()
async def pause(ctx):
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.pause(True)
    await ctx.send("已暫停。")


@bot.command()
async def resume(ctx):
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    await player.pause(False)
    await ctx.send("繼續播放。")


@bot.command()
async def stop(ctx):
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    player.track_queue.clear()  # 清空隊列
    await player.stop()
    await ctx.send("已停止播放。")


@bot.command()
async def leave(ctx):
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    player.track_queue.clear()
    await player.disconnect()
    await ctx.send("已離開語音頻道。")


@bot.command()
async def queue(ctx):
    """顯示目前的播放隊列"""
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    if not player.track_queue:
        await ctx.send("隊列是空的。")
        return

    queue_list = "\n".join(
        [f"{i + 1}. {track.title}" for i, track in enumerate(list(player.track_queue)[:10])]
    )
    remaining = len(player.track_queue) - 10
    if remaining > 0:
        queue_list += f"\n... 還有 {remaining} 首歌曲"

    embed = discord.Embed(
        title="播放隊列",
        description=queue_list,
        color=discord.Color.blue()
    )
    if player.playing:
        embed.add_field(name="目前播放", value=player.current.title if player.current else "無", inline=False)
    embed.set_footer(text=f"隊列中共有 {len(player.track_queue)} 首歌曲")
    await ctx.send(embed=embed)


@bot.command()
async def skip(ctx):
    """跳過目前的歌曲"""
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    if not player.playing:
        await ctx.send("目前沒有正在播放的歌曲。")
        return

    await player.stop()
    await ctx.send("已跳過目前的歌曲。")


@bot.command()
async def clear_queue(ctx):
    """清空隊列"""
    player: MusicPlayer | None = ctx.voice_client

    if player is None:
        await ctx.send("我現在不在語音頻道。")
        return

    if not player.track_queue:
        await ctx.send("隊列已經是空的。")
        return

    player.track_queue.clear()
    await ctx.send("已清空播放隊列。")


def main():
    if not TOKEN:
        raise RuntimeError("缺少 DISCORD_TOKEN，請在 .env 設定 Discord Bot Token。")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
