import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Certifique-se de que o bot tem acesso à lista de membros

bot = commands.Bot(command_prefix='!', intents=intents)

async def slash_avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    # Cria o embed com o avatar do usuário
    embed = discord.Embed(
        title=f"Avatar de {member.name}",
        color=0x1E90FF
    )
    embed.set_image(url=member.avatar)  # Corrigido para `user.avatar_url`
    
    await interaction.response.send_message(embed=embed)


async def slash_userinfo(interaction: discord.Interaction, member: discord.Member = None):
    """Mostrar informações sobre um usuário."""
    if member is None:
        member = interaction.user

    tag = str(member)

    try:
        embed = discord.Embed(
            title=f'Informações de {member.display_name}',
            color=0x87CEEB
            )
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Tag', value=tag, inline=False)
        embed.add_field(name='Entrou em', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(embed=embed)


async def slash_info(interaction: discord.Interaction):
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
    await interaction.response.send_message(embed=embed)


async def slash_serverinfo(interaction: discord.Interaction):
    """Informações do servidor."""
    guild = interaction.guild
    owner = guild.owner

    total_channels = len(guild.channels)
    data_entrada = interaction.user.joined_at.strftime('%d/%m/%Y %H:%M:%S')

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

    await interaction.response.send_message(embed=embed)

