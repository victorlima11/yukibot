import discord
from discord.ext import commands
import random
from anime_api.apis import HmtaiAPI
from anime_api.apis.hmtai.types import ImageCategory

invites = {}


async def ping(ctx):
    """Ping Pong."""
    await ctx.send(f'{ctx.author.mention} Pong!')

async def invite(ctx):
    channel_id = ctx.channel.id

    if channel_id in invites:
        await ctx.send('Um convite já foi criado para este canal.')
        return

    try:
        invite = await ctx.channel.create_invite(max_age=3600, max_uses=1)
        invites[channel_id] = invite.url
        await ctx.send(f'Aqui está o seu convite: {invite.url}')
    except discord.Forbidden:
        await ctx.send('Eu não tenho permissão para criar convites neste canal.',delete_after=5)
    except discord.HTTPException:
        await ctx.send('Houve um erro ao tentar criar o convite.')

async def somar(ctx,  num1: float=None, num2: float=None):
    """Soma dois números."""
    if num1 is None or num2 is None:
        await ctx.send(f"{ctx.author.mention} Você precisa fornecer dois números para somar. Exemplo: `!somar 5 10`")
    await ctx.send(f'{ctx.author.mention} Soma entre: {num1} + {num2} = {num1 + num2:.2f}')

async def subtrair(ctx,  num1: float=None, num2: float=None):
    """Subtrai dois números."""
    if num1 is None or num2 is None:
        await ctx.send(f"{ctx.author.mention} Você precisa fornecer dois números para subtrair. Exemplo: `!subtrair 12 7`")
    await ctx.send(f'{ctx.author.mention} Subtração entre: {num1} - {num2} = {num1 - num2:.2f}')

async def dividir(ctx,  num1: float=None, num2: float=None):
    """Divide dois números."""
    if num1 is None or num2 is None:
        await ctx.send(f"{ctx.author.mention} Você precisa fornecer dois números para dividir. Exemplo: `!dividir 8 2`")
    await ctx.send(f'{ctx.author.mention} Divisão entre: {num1} / {num2} = {num1 / num2:.2f}')

async def multiplicar(ctx,  num1: float=None, num2: float=None):
    """Multiplica dois números."""
    if num1 is None or num2 is None:
        await ctx.send(f"{ctx.author.mention} Você precisa fornecer dois números para multiplicar. Exemplo: `!multiplicar 3 10`")
    await ctx.send(f'{ctx.author.mention} Multiplicação entre: {num1} * {num2} = {num1 * num2:.2f}')

async def say(ctx, *, text: str):
    """Retorna o texto fornecido pelo usuário."""
    await ctx.send(text)

async def nrandom(ctx, min_num: int = None, max_num: int = None):
    """Gera um número aleatório entre dois números fornecidos. Exemplo de uso: !random 1 100"""
    if min_num is None or max_num is None:
        await ctx.send("Uso correto: `!random <min_num> <max_num>`. Exemplo: `!random 1 100`")
        return

    if min_num > max_num:
        await ctx.send("O primeiro número deve ser menor ou igual ao segundo número.")
        return
    
    random_num = random.randint(min_num, max_num)
    await ctx.send(f"Número aleatório entre {min_num} e {max_num}: {random_num}")

api = HmtaiAPI()

async def hug(ctx, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.HUG)
    embed = discord.Embed(
        description=f"{ctx.author.mention} deu um abraço em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)
    await ctx.send(embed=embed)

async def kiss(ctx, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.KISS)
    embed = discord.Embed(
        description=f"{ctx.author.mention} deu um beijo em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)

    # Envia o embed
    await ctx.send(embed=embed)


async def slap(ctx, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.SLAP)
    embed = discord.Embed(
        description=f"{ctx.author.mention} deu um tapa em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)

    # Envia o embed
    await ctx.send(embed=embed)


async def coinflip(ctx):
    """Joga uma moeda e retorna 'Cara' ou 'Coroa'."""
    result = random.choice(["Cara", "Coroa"])
    await ctx.send(f"A moeda caiu em: **{result}**")
