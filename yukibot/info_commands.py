import discord
from discord.ext import commands

async def userinfo(ctx, member: discord.Member = None):
    """Mostrar informações sobre um usuário."""
    if member is None:
        member = ctx.author

    try:
        embed = discord.Embed(title=f'Informações de {member.display_name}', color=discord.Color.blue())
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Entrou em', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=member.avatar.url) 
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'Ocorreu um erro: {e}')

async def info(ctx):
    """Informações do bot."""
    embed = discord.Embed(
        title="Informações",
        description="Olá, sou o Nyuh Bot!",
        color=0x87CEEB
    )
    embed.add_field(name="Prefixo", value="'!'", inline=False)
    embed.set_image(url="https://i.pinimg.com/originals/c6/8b/e1/c68be1c09c2423ea556cdc4b4c72d30e.jpg")
    embed.add_field(name="Criador", value="Nyuh", inline=False)
    embed.set_footer(text="Obrigado por usar o bot!")
    await ctx.send(embed=embed)

async def serverinfo(ctx):
    guild = ctx.guild
    owner = guild.owner

    embed = discord.Embed(
        title=f"Informações do Servidor: {guild.name}",
        description=f"Detalhes sobre o servidor",
        color=0x1E90FF
    )
    embed.add_field(name="Nome do Servidor", value=guild.name, inline=True)
    embed.add_field(name="ID do Servidor", value=guild.id, inline=True)
    embed.add_field(name="Membros", value=guild.member_count, inline=True)
    embed.add_field(name="Canais", value=len(guild.channels), inline=True)
    embed.add_field(name="Cargos", value=len(guild.roles), inline=True)
    embed.add_field(name="Dono", value=f"{owner.mention}", inline=True)
    embed.add_field(name="Data de Criação", value=guild.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
    embed.add_field(name="Data de Entrada", value=ctx.message.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
    
    embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)
