import discord
from discord.ext import commands
import io
from PIL import Image


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def invert(ctx):
    if not ctx.message.attachments:
        await ctx.send(f"{ctx.author.mention} Por favor envie uma imagem.", delete_after=5)
        return
    
    attachment = ctx.message.attachments[0]

    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send(f"{ctx.author.mention} Por favor, envie um arquivo de imagem válido (png, jpg, jpeg).", delete_after=5)
        return

    image_data = await attachment.read()
    image = Image.open(io.BytesIO(image_data))

    inverted_image = image.transpose(Image.FLIP_TOP_BOTTOM)

    with io.BytesIO() as image_binary:
        inverted_image.save(image_binary, format='PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename="imagem_invertida.png"))