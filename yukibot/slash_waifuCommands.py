import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import requests

async def slash_waifu(ctx):
        # Define a URL da API
    url = 'https://api.waifu.pics/sfw/waifu'
    
    # Envia a requisição GET para a API
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        
        # Obtém a URL da imagem
        image_url = data.get('url')
        
        # Cria um embed com a imagem
        embed = discord.Embed(
            title="Achou uma waifu!",
            description=f"{ctx.author.mention} usou o comando !waifu!",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        
        # Envia o embed como resposta no canal
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Request failed with status code: {response.status_code}")