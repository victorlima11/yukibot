import discord
from discord.ext import commands
import cv2
import numpy as np
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def inverty(ctx):
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
        
        embed = discord.Embed(
            title=f"Aqui está sua imagem invertida!",
            color=discord.Color.blue()
        )
        embed.set_image(url="attachment://imagem_invertida.png")
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        
        # Enviar o embed com a imagem
        await ctx.reply(embed=embed, file=discord.File(fp=image_binary, filename="imagem_invertida.png"))


async def invertx(ctx):
    if not ctx.message.attachments:
        await ctx.send(f"{ctx.author.mention} Por favor envie uma imagem.", delete_after=5)
        return
    
    attachment = ctx.message.attachments[0]

    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send(f"{ctx.author.mention} Por favor, envie um arquivo de imagem válido (png, jpg, jpeg).", delete_after=5)
        return

    image_data = await attachment.read()
    image = Image.open(io.BytesIO(image_data))

    rotate_image = image.transpose(Image.FLIP_LEFT_RIGHT)

    with io.BytesIO() as image_binary:
        rotate_image.save(image_binary, format='PNG')
        image_binary.seek(0)
        
        embed = discord.Embed(
            title="Aqui está sua imagem invertida!",
            color=discord.Color.blue()
        )
        embed.set_image(url="attachment://imagem_invertx.png")
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        
        # Enviar o embed com a imagem
        await ctx.reply(embed=embed, file=discord.File(fp=image_binary, filename="imagem_invertx.png"))
    

async def grayscale(ctx):
    if not ctx.message.attachments:
        await ctx.send(f"{ctx.author.mention} Por favor, envie uma imagem.", delete_after=5)
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send(f"{ctx.author.mention} Por favor, envie um arquivo de imagem válido (png, jpg, jpeg).", delete_after=5)
        return

    image_data = await attachment.read()
    image = Image.open(io.BytesIO(image_data))

    gray_image = image.convert("L")

    with io.BytesIO() as image_binary:
        gray_image.save(image_binary, format='PNG')
        image_binary.seek(0)

        embed = discord.Embed(
            title="Aqui está sua imagem em escala de cinza!",
            color=discord.Color.greyple()
        )
        embed.set_image(url="attachment://imagem_grayscale.png")
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed, file=discord.File(fp=image_binary, filename="imagem_grayscale.png"))


async def text(ctx, *, texto: str = "Texto de Exemplo"):
    if not ctx.message.attachments:
        await ctx.send(f"{ctx.author.mention} Por favor, envie uma imagem.", delete_after=5)
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send(f"{ctx.author.mention} Por favor, envie um arquivo de imagem válido (png, jpg, jpeg).", delete_after=5)
        return

    image_data = await attachment.read()
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    # Propriedades iniciais do texto
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 4  # Tamanho inicial da fonte
    thickness = 2  # Espessura do texto
    font_color = (255, 255, 255)  # Branco

    # Obter as dimensões da imagem
    image_height, image_width, _ = image.shape

    # Ajustar o tamanho da fonte para que o texto caiba na imagem
    while True:
        text_size = cv2.getTextSize(texto, font, font_scale, thickness)[0]
        if text_size[0] < image_width and text_size[1] < image_height * 0.1:  # Ajuste a altura para caber em 10% da imagem
            break
        font_scale -= 0.1  # Reduzir o tamanho da fonte
        if font_scale < 0.5:  # Limite mínimo da fonte
            font_scale = 0.5
            break

    # Calcular a posição do texto para centralizar
    x_position = (image_width - text_size[0]) // 2  # Centralizar no eixo X
    y_position = text_size[1] + 10  # Posicionar no topo da imagem

    # Adicionar o texto à imagem
    cv2.putText(image, texto, (x_position, y_position), font, font_scale, font_color, thickness)

    # Converter a imagem de volta para um formato que o Discord aceita
    _, image_binary = cv2.imencode('.png', image)

    embed = discord.Embed(
        title="Aqui está sua imagem com o texto adicionado!",
        color=discord.Color.blue()
    )
    embed.set_image(url="attachment://imagem_com_texto.png")
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    await ctx.reply(embed=embed, file=discord.File(io.BytesIO(image_binary), filename="imagem_com_texto.png"))

async def blur(ctx, intensity: float = 5.0):  # O valor padrão é 5.0
    if not ctx.message.attachments:
        await ctx.send(f"{ctx.author.mention} Por favor, envie uma imagem.", delete_after=5)
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send(f"{ctx.author.mention} Por favor, envie um arquivo de imagem válido (png, jpg, jpeg).", delete_after=5)
        return

    try:
        # Limitar o valor de intensidade entre 0 e 20
        if intensity < 0:
            intensity = 0
        elif intensity > 20:
            intensity = 20

        image_data = await attachment.read()
        image = Image.open(io.BytesIO(image_data))

        # Aplicar desfoque com a intensidade especificada
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=intensity))

        with io.BytesIO() as image_binary:
            blurred_image.save(image_binary, format='PNG')
            image_binary.seek(0)

            embed = discord.Embed(
                title="Aqui está sua imagem desfocada!",
                color=discord.Color.blue()
            )
            embed.set_image(url="attachment://imagem_blur.png")
            embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            # Enviar o embed com a imagem
            await ctx.reply(embed=embed, file=discord.File(fp=image_binary, filename="imagem_blur.png"))

    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {str(e)}", delete_after=5)