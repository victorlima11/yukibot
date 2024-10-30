import discord
from discord import app_commands
from discord.ext import commands
import random
from anime_api.apis import HmtaiAPI
from anime_api.apis.hmtai.types import ImageCategory



api = HmtaiAPI()

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} Pong!')


async def slash_invite(interaction: discord.Interaction):
    channel_id = interaction.channel.id

    if channel_id in invites:
        await interaction.response.send_message('Um convite já foi criado para este canal.')
        return

    try:
        invite = await interaction.channel.create_invite(max_age=3600, max_uses=1)
        invites[channel_id] = invite.url
        await interaction.response.send_message(f'Aqui está o seu convite: {invite.url}')
    except discord.Forbidden:
        await interaction.response.send_message('Eu não tenho permissão para criar convites neste canal.', ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message('Houve um erro ao tentar criar o convite.')


async def slash_somar(interaction: discord.Interaction, num1: float, num2: float):
    result = num1 + num2
    await interaction.response.send_message(f'{interaction.user.mention} Soma entre: {num1} + {num2} = {result:.2f}')


async def slash_subtrair(interaction: discord.Interaction, num1: float, num2: float):
    result = num1 - num2
    await interaction.response.send_message(f'{interaction.user.mention} Subtração entre: {num1} - {num2} = {result:.2f}')


async def slash_dividir(interaction: discord.Interaction, num1: float, num2: float):
    if num2 == 0:
        await interaction.response.send_message(f"{interaction.user.mention} Divisão por zero não é permitida.")
        return
    result = num1 / num2
    await interaction.response.send_message(f'{interaction.user.mention} Divisão entre: {num1} / {num2} = {result:.2f}')


async def slash_multiplicar(interaction: discord.Interaction, num1: float, num2: float):
    result = num1 * num2
    await interaction.response.send_message(f'{interaction.user.mention} Multiplicação entre: {num1} * {num2} = {result:.2f}')


async def slash_say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)


async def slash_random(interaction: discord.Interaction, min_num: int, max_num: int):
    if min_num > max_num:
        await interaction.response.send_message("O primeiro número deve ser menor ou igual ao segundo número.")
        return
    
    random_num = random.randint(min_num, max_num)
    await interaction.response.send_message(f"Número aleatório entre {min_num} e {max_num}: {random_num}")


async def slash_hug(interaction: discord.Interaction, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.HUG)
    embed = discord.Embed(
        description=f"{interaction.user.mention} deu um abraço em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)
    await interaction.response.send_message(embed=embed)


async def slash_kiss(interaction: discord.Interaction, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.KISS)
    embed = discord.Embed(
        description=f"{interaction.user.mention} deu um beijo em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)
    await interaction.response.send_message(embed=embed)


async def slash_slap(interaction: discord.Interaction, member: discord.Member):
    image = api.get_random_image(ImageCategory.SFW.SLAP)
    embed = discord.Embed(
        description=f"{interaction.user.mention} deu um tapa em {member.mention}!",
        color=discord.Color.blue()
    )
    embed.set_image(url=image.url)
    await interaction.response.send_message(embed=embed)

async def slash_coinflip(interaction: discord.Interaction):
    """Joga uma moeda e retorna 'Cara' ou 'Coroa'."""
    result = random.choice(["Cara", "Coroa"])
    await interaction.response.send_message(f"A moeda caiu em: **{result}**")

