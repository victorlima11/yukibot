import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def avatar(ctx, user: discord.User = None):
    """Mostra o avatar de um usuário específico."""
    if user is None:
        # Se nenhum usuário for especificado, usa o autor da mensagem
        user = ctx.author
    
    # Cria o embed com o avatar do usuário
    embed = discord.Embed(
        title=f"Avatar de {user.name}",
        color=0x1E90FF
    )
    embed.set_image(url=user.avatar.url)
    
    await ctx.send(embed=embed)

async def userinfo(ctx, member: discord.Member = None):
    """Mostrar informações sobre um usuário."""
    tag = str(ctx.author)
    if member is None:
        member = ctx.author

    try:
        embed = discord.Embed(title=f'Informações de {member.display_name}', color=discord.Color.blue())
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Tag', value=tag, inline=False)
        embed.add_field(name='Entrou em', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=member.avatar.url) 
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'Ocorreu um erro: {e}')

async def info(ctx):
    """Informações do bot."""
    embed = discord.Embed(
        title="Informações",
        description="Saudações, sou a Yuki bot. Vou lhe ajudar como puder!",
        color=0x87CEEB
    )
    embed.add_field(name="Fui desenvolvida para facilitar algumas funções.", value="Use !help para conhecer os comandos", inline=False)
    embed.set_image(url="https://i.pinimg.com/originals/c1/fe/ff/c1feff7a3960d75cb225160587b45ca6.gif")
    embed.add_field(name="Criado por:", value="[Nyuh999](https://github.com/desire777)", inline=False)
    embed.add_field(name="Site:", value="[YukiBot](https://yukibot.squareweb.app/#inicio)", inline=False)
    embed.set_footer(text="Obrigado por usar o bot!")
    await ctx.send(embed=embed)

async def serverinfo(ctx):
    guild = ctx.guild
    owner = guild.owner
    total_channels = len(guild.channels)
    data_entrada = ctx.author.joined_at.strftime('%d/%m/%Y %H:%M:%S')

    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)

    embed = discord.Embed(
        title=f"Informações do Servidor: {guild.name}",
        description=f"Detalhes sobre o servidor",
        color=0x1E90FF
    )
    embed.add_field(name="Nome do Servidor", value=guild.name, inline=True)
    embed.add_field(name="ID do Servidor", value=guild.id, inline=True)
    embed.add_field(name="Membros", value=guild.member_count, inline=True)
    embed.add_field(name=f"Canais ({total_channels})", value=f"Texto: {text_channels}\nVoz: {voice_channels}", inline=True)
    embed.add_field(name="Cargos", value=len(guild.roles), inline=True)
    embed.add_field(name="Dono", value=f"{owner.mention}", inline=True)
    embed.add_field(name="Data de Criação", value=guild.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
    embed.add_field(name="Data de Entrada", value=data_entrada, inline=True)
    
    embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)

