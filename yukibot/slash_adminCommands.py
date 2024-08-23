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

async def slash_ban(interaction: discord.Interaction, member: discord.Member = None, user_id: int = None, reason: str = None):
    """Banir um membro do servidor por menção ou ID."""
    if interaction.user.guild_permissions.administrator:
        if member is None and user_id is not None:
            try:
                user = await bot.fetch_user(user_id)
                member = discord.utils.get(interaction.guild.members, id=user_id)
                if member is None:
                    await interaction.response.send_message('Usuário não encontrado no servidor.')
                    return
            except discord.NotFound:
                await interaction.response.send_message('Usuário não encontrado.')
                return
            except discord.HTTPException as e:
                await interaction.response.send_message(f'Erro ao buscar usuário: {e}')
                return
        
        if member is None:
            await interaction.response.send_message('Membro não encontrado.')
            return
        
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member.mention} foi banido do servidor.')
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", delete_after=5)

async def slash_clear(interaction: discord.Interaction, amount: int):
    """Limpar mensagens do servidor."""
    if interaction.user.guild_permissions.administrator:
        if amount <= 0:
            await interaction.response.send_message("Você deve fornecer um número positivo de mensagens para limpar.")
            return
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'{amount} mensagens limpas.', delete_after=5)
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando.", delete_after=5)
    
async def slash_unban(interaction: discord.Interaction, user_id: int, reason: str = None):
    """Desbanir um membro do servidor."""
    if interaction.user.guild_permissions.administrator:
        try:
            user = await bot.fetch_user(user_id)
            await interaction.guild.unban(user, reason=reason)
            await interaction.response.send_message(f"{user.mention} foi desbanido. Motivo: {reason if reason else 'Não fornecido.'}", delete_after=5)
        except discord.NotFound:
            await interaction.response.send_message("Usuário não encontrado.", delete_after=5)
    else:
        await interaction.response.send_message(f"{interaction.user.mention} Você não tem permissão para usar este comando", delete_after=5)

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
    
async def slash_remove_role(interaction: discord.Interaction, member: discord.Member = None, role: discord.Role = None):
    """Remove um cargo do membro."""
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