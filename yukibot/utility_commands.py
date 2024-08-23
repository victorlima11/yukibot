import discord
from discord.ext import commands
import aiohttp
from deep_translator import GoogleTranslator
from config import CAT_KEY, PEXELS_KEY
import requests



async def traduzir(ctx, idioma_destino: str = None, *, texto: str = None):
    """Traduzir texto para outro idioma. Ex: !traduzir pt Olá!"""
    if idioma_destino is None or texto is None:
        await ctx.send('Por favor, forneça o idioma de destino e o texto a ser traduzido. Exemplo: `!traduzir pt Olá!`.')
        return

    translator = GoogleTranslator(target=idioma_destino)
    try:
        traducao = translator.translate(texto)
        await ctx.send(f'{ctx.author.mention}\nTexto original: {texto}\n**Texto traduzido**: {traducao}')
    except Exception as e:
        await ctx.send(f'Ocorreu um erro na tradução: {e}')


async def cat(ctx):
    """Enviar uma imagem de gato aleatória em um embed."""
    CAT_API_KEY = CAT_KEY
    url = 'https://api.thecatapi.com/v1/images/search'
    headers = {'x-api-key': CAT_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        image_url = data[0]['url']
                        embed = discord.Embed(
                            title=f'Gerou a imagem de um gato!',
                            color=0x87CEEB
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text='Ultilize o comando !cat para gerar a imagem de um gato.')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send('Desculpe, não consegui encontrar uma imagem de gato no momento.')
                else:
                    await ctx.send(f'Erro ao buscar a imagem: Código de status {resp.status}')
        except aiohttp.ClientError as e:
            await ctx.send(f'Ocorreu um erro ao buscar a imagem de gato: {e}')


translator = GoogleTranslator(source='pt', target='en')

async def img(ctx, *, query: str):
    translated_query = translator.translate(query)

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {
        "Authorization": PEXELS_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data['total_results'] > 0:
        image_url = data['photos'][0]['src']['original']
        embed = discord.Embed( 
            title=f"Imagem buscado com sucesso!",
            description=f"Busca através de PexelsAPI",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Nenhuma imagem encontrada para essa busca.")


