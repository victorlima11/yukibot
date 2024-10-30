import discord
from discord import app_commands
from discord.ext import commands

# Criação do bot separado para registrar comandos de slash
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

async def slash_kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    """Expulsar um membro do servidor."""
    if interaction.user.guild_permissions.administrator:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.mention} foi expulso do servidor.')
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", delete_after=5)


async def slash_ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    """Banir um membro do servidor por menção."""
    if interaction.user.guild_permissions.administrator:
        if member is None:
            await interaction.response.send_message('Membro não encontrado.', ephemeral=True)
            return
        
        # Verifica se o cargo do autor é superior ao do membro
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(f"Você não pode banir {member.mention}, pois eles têm um cargo igual ou superior ao seu.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'{member.mention} foi banido do servidor.', ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f'Erro ao banir o usuário: {e}', ephemeral=True)
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, você não tem permissão para usar este comando.", ephemeral=True)


async def slash_clear(interaction: discord.Interaction, amount: int):
    """Limpar mensagens do servidor."""
    if interaction.user.guild_permissions.administrator:
        if amount <= 0:
            await interaction.response.send_message("Você deve fornecer um número positivo de mensagens para limpar.", ephemeral=True)
            return
        
        # Enviar uma resposta inicial informando que o comando foi recebido
        await interaction.response.send_message(f'Quantidade de mensagens limpas: {amount}', ephemeral=True)
        
        # Limpar mensagens
        await interaction.channel.purge(limit=amount)
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", ephemeral=True)




async def slash_mute(interaction: discord.Interaction, member: discord.Member = None, reason: str = None):
    """Muta um membro no servidor."""
    if interaction.user.guild_permissions.administrator:
        if member is None:
            await interaction.response.send_message("Você precisa mencionar um membro para silenciar. Exemplo: `/mute @Usuário [motivo]`")
            return
        
        muted_role = discord.utils.get(interaction.guild.roles, name="Silenciado")
        if muted_role is None:
            muted_role = await interaction.guild.create_role(name="Silenciado")
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)
        
        if muted_role in member.roles:
            await interaction.response.send_message(f"{member.mention} já está silenciado.")
            return
        
        await member.add_roles(muted_role, reason=reason)
        await interaction.response.send_message(f"{member.mention} foi silenciado. Motivo: {reason if reason else 'Não fornecido.'}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", delete_after=5)

async def slash_unmute(interaction: discord.Interaction, member: discord.Member = None):
    """Desmuta um membro no servidor."""
    if interaction.user.guild_permissions.administrator:
        if member is None:
            await interaction.response.send_message("Você precisa mencionar um membro para desmutar. Exemplo: `/unmute @Usuário`")
            return
        
        muted_role = discord.utils.get(interaction.guild.roles, name="Silenciado")
        if muted_role is None:
            await interaction.response.send_message("O cargo 'Silenciado' não existe. Parece que ninguém foi mutado.")
            return
        
        if muted_role not in member.roles:
            await interaction.response.send_message(f"{member.mention} não está silenciado.")
            return
        
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f"{member.mention} foi desmutado.")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", delete_after=5)

async def slash_lock(interaction: discord.Interaction):
    """Bloqueia o canal atual para que apenas administradores possam enviar mensagens."""
    if interaction.user.guild_permissions.administrator:
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Este canal foi bloqueado. Apenas administradores podem enviar mensagens.")
    else:
        await interaction.response.send_message("Você não tem permissão para bloquear este canal.")

async def slash_unlock(interaction: discord.Interaction):
    """Desbloqueia o canal atual, permitindo que todos enviem mensagens novamente."""
    if interaction.user.guild_permissions.administrator:
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Este canal foi desbloqueado. Todos podem enviar mensagens novamente.")
    else:
        await interaction.response.send_message("Você não tem permissão para desbloquear este canal.")

async def slash_add_role(interaction: discord.Interaction, member: discord.Member = None, role: discord.Role = None):
    """Adiciona um cargo ao membro."""
    if interaction.user.guild_permissions.administrator:
      if member is None or role is None:
          await interaction.response.send_message("Você precisa mencionar um usuário e um cargo válido. Exemplo: `/add_role @Usuário @Cargo`")
          return
  
      if role not in interaction.guild.roles:
          await interaction.response.send_message(f"O cargo '{role.name}' não existe no servidor.")
          return
  
      if member not in interaction.guild.members:
          await interaction.response.send_message(f"O membro {member.mention} não foi encontrado no servidor.")
          return

      await member.add_roles(role)
      await interaction.response.send_message(f"{member.mention} agora possui o cargo {role.name}.")
    else:
      await interaction.response.send_message("Você não tem permissão para adicionar roles.")
    
    
async def slash_remove_role(interaction: discord.Interaction, member: discord.Member = None, role: discord.Role = None):
    """Remove um cargo do membro."""
    if interaction.user.guild_permissions.administrator:
      if member is None or role is None:
          await interaction.response.send_message("Você precisa mencionar um usuário e um cargo válido. Exemplo: `/remove_role @Usuário @Cargo`")
          return
  
      if role not in interaction.guild.roles:
          await interaction.response.send_message(f"O cargo '{role.name}' não existe no servidor.")
          return
  
      if member not in interaction.guild.members:
          await interaction.response.send_message(f"O membro {member.mention} não foi encontrado no servidor.")
          return

      await member.remove_roles(role)
      await interaction.response.send_message(f"O cargo {role.name} foi removido de {member.mention}.")
    else:
      await interaction.response.send_message("Você não tem permissão para remover roles.")

async def slash_banner(interaction: discord.Interaction, member: discord.Member = None):
    """Pega o banner de um usuário do Discord."""
    if member is None:
        member = interaction.user

    user_id = member.id
    try:
        # Pega o banner do usuário
        user = await bot.fetch_user(user_id)
        banner_url = user.banner.url if user.banner else None
        if banner_url:
            await interaction.response.send_message(f'O banner de {member.mention} é: {banner_url}')
        else:
            await interaction.response.send_message(f'{member.mention} não tem um banner.')
    except discord.NotFound:
        await interaction.response.send_message('Usuário não encontrado.')
    except discord.HTTPException as e:
        await interaction.response.send_message(f'Erro ao buscar banner: {e}')