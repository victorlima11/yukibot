import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import logging

logging.basicConfig(level=logging.INFO)

music_queue = [] 

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'geo_bypass': True,
        }

        if stream:
            ydl_opts['format'] = 'bestaudio/best'

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]

        return cls(discord.FFmpegPCMAudio(info['url']), data=info)

async def play_next(ctx):
    if music_queue:
        next_song = music_queue.pop(0)
        ctx.voice_client.play(next_song, after=lambda e: ctx.bot.loop.create_task(play_next(ctx)))
        embed = discord.Embed(title="Tocando Agora", description=next_song.title, color=discord.Color.blue())
        embed.set_thumbnail(url=next_song.thumbnail)
        await ctx.send(embed=embed)
        logging.info(f"Playing next song: {next_song.title}")
    else:
        if not ctx.voice_client.is_playing():
            await ctx.voice_client.disconnect()
            logging.info("Queue is empty and not playing, disconnecting.")

async def play(ctx, *, url):
    if ctx.voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=ctx.bot.loop, stream=False)
        if ctx.voice_client.is_playing():
            music_queue.append(player)
            embed = discord.Embed(title="Adicionado à fila:", description=player.title, color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            ctx.voice_client.play(player, after=lambda e: ctx.bot.loop.create_task(play_next(ctx)))
            embed = discord.Embed(title="Tocando Agora", description=player.title, color=discord.Color.blue())
            embed.set_thumbnail(url=player.thumbnail)
            await ctx.send(embed=embed)
            logging.info(f"Playing: {player.title}")

async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        music_queue.clear()  # Limpa a fila ao parar a música
        embed = discord.Embed(title="Música Parada", description="A música foi parada e a fila foi limpa.", color=discord.Color.red())
        await ctx.send(embed=embed)
        logging.info("Music stopped and queue cleared.")

async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        if music_queue:
            await play_next(ctx)
        else:
            embed = discord.Embed(title="Música Pulada", description="Não há músicas na fila para tocar.", color=discord.Color.yellow())
            await ctx.send(embed=embed)
            logging.info("Skipped song but no songs left in queue.")

async def queue(ctx):
    if not music_queue:
        embed = discord.Embed(title="Fila de Músicas", description="A fila está vazia.", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        queue_list = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(music_queue)])
        embed = discord.Embed(title="Fila de Músicas", description=queue_list, color=discord.Color.blue())
        await ctx.send(embed=embed)

async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        music_queue.clear()  # Limpa a fila ao desconectar
        embed = discord.Embed(title="Desconectado", description="O bot foi desconectado do canal de voz e a fila foi limpa.", color=discord.Color.red())
        await ctx.send(embed=embed)
        logging.info("Bot disconnected and queue cleared.")
