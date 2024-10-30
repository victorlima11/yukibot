import discord
from discord.ext import commands
import aiohttp
from deep_translator import GoogleTranslator
from config import CAT_KEY, PEXELS_KEY
import requests


async def slash_traduzir(interaction: discord.Interaction, idioma_destino: str, texto: str):
    """Traduzir texto para outro idioma."""
    if not idioma_destino or not texto:
        await interaction.response.send_message('Por favor, forneça o idioma de destino e o texto a ser traduzido. Exemplo: `/traduzir pt Olá!`.', ephemeral=True)
        return

    translator = GoogleTranslator(target=idioma_destino)
    try:
        traducao = translator.translate(texto)
        await interaction.response.send_message(f'{interaction.user.mention}\nTexto original: {texto}\n**Texto traduzido**: {traducao}')
    except Exception as e:
        await interaction.response.send_message(f'Ocorreu um erro na tradução: {e}', ephemeral=True)


async def slash_cat(interaction: discord.Interaction):
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
                            title='Gerou a imagem de um gato!',
                            color=0x87CEEB
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text='Utilize o comando /cat para gerar a imagem de um gato.')
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message('Desculpe, não consegui encontrar uma imagem de gato no momento.', ephemeral=True)
                else:
                    await interaction.response.send_message(f'Erro ao buscar a imagem: Código de status {resp.status}', ephemeral=True)
        except aiohttp.ClientError as e:
            await interaction.response.send_message(f'Ocorreu um erro ao buscar a imagem de gato: {e}', ephemeral=True)


async def slash_img(interaction: discord.Interaction, query: str):
    """Buscar uma imagem usando a Pexels API."""
    translator = GoogleTranslator(source='pt', target='en')
    translated_query = translator.translate(query)

    url = f"https://api.pexels.com/v1/search?query={translated_query}&per_page=1"
    headers = {
        "Authorization": PEXELS_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Verificar se encontramos uma imagem
    if data['total_results'] > 0:
        image_url = data['photos'][0]['src']['original']
        embed = discord.Embed(
            title="Imagem buscada com sucesso!",
            description="Busca através de Pexels API",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Nenhuma imagem encontrada para essa busca.", ephemeral=True)
