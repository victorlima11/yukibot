import discord
from discord.ext import commands
import aiohttp
from deep_translator import GoogleTranslator
from config import WEATHER_KEY



async def clima(ctx, *, city: str = None):
    """Mostrar informações do clima de uma cidade."""
    if city is None:
        await ctx.send('Por favor, forneça o nome da cidade. Exemplo: `!clima São Paulo`.')
        return

    api_key = WEATHER_KEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                data = await resp.json()
                if data['cod'] == 200:
                    weather_desc = data['weather'][0]['description'].capitalize()
                    translated_desc = GoogleTranslator(source='auto', target='pt').translate(weather_desc)
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    embed = discord.Embed(
                        title=f'Clima em {city.capitalize()}',
                        color=0x87CEEB
                    )
                    embed.add_field(name='Descrição', value=translated_desc, inline=False)
                    embed.add_field(name='Temperatura', value=f'{temp}°C', inline=True)
                    embed.add_field(name='Sensação Térmica', value=f'{feels_like}°C', inline=True)
                    embed.add_field(name='Umidade', value=f'{humidity}%', inline=True)
                    embed.add_field(name='Velocidade do Vento', value=f'{wind_speed} m/s', inline=True)
                    embed.set_footer(text='Dados fornecido por OpenWeather API ☁️')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'Não consegui encontrar informações sobre o clima para {city}.')
        except aiohttp.ClientError as e:
            await ctx.send(f'Ocorreu um erro ao consultar o clima: {e}')