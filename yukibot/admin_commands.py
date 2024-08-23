import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def kick(ctx, member: discord.Member, *, reason=None):
    """Expulsar um membro do servidor."""
    if member is None:
        await ctx.send("Você precisa mencionar um membro para expulsá-lo. Exemplo: `!kick @Usuário [motivo]`")
    if ctx.author.guild_permissions.administrator:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} foi expulso do servidor.')
    else:
        await ctx.send(f"{ctx.author.mention} Você não tem permissão para usar este comando.", delete_after=5)

async def ban(ctx, member: discord.Member = None, user_id: int = None, *, reason=None):
    """Banir um membro do servidor por menção ou ID."""
    if member is None:
        await ctx.send("Você precisa mencionar um membro para baní-lo. Exemplo: `!ban @Usuário [motivo]`")
    if ctx.author.guild_permissions.administrator:
        if user_id is not None:
            try:
                user = await bot.fetch_user(user_id)
                member = discord.utils.get(ctx.guild.members, id=user_id)
                if member is None:
                    await ctx.send('Usuário não encontrado no servidor.')
                    return
            except discord.NotFound:
                await ctx.send('Usuário não encontrado.')
                return
            except discord.HTTPException as e:
                await ctx.send(f'Erro ao buscar usuário: {e}')
                return
        
        if member is None:
            await ctx.send('Membro não encontrado.')
            return
        
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} foi banido do servidor.')
    else:
        await ctx.send(f"{ctx.author.mention} Você não tem permissão para usar este comando.", delete_after=5)

async def clear(ctx, amount: int):
    """Limpar mensagens do servidor."""
    if ctx.author.guild_permissions.administrator:
        if amount <= 0:
            await ctx.send("Você deve fornecer um número positivo de mensagens para limpar.")
            return
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} mensagens limpas.', delete_after=5)
    else:
        await ctx.send(f"{ctx.author.mention} Você não tem permissão para usar este comando.", delete_after=5)
    
async def unban(ctx, member:discord.User, *, reason=None):
    if member is None:
        await ctx.send("Você precisa mencionar um membro para desbaní-lo. Exemplo: `!unban id [motivo]`")
    if ctx.author.guild_permissions.administrator:
        if reason == None:
            await ctx.guild.unban(member, reason=reason)
            await ctx.send(f"{member.mention} foi desbanido.", delete_after=5)
        elif reason !=  None:
            await ctx.guild.unban(member, reason=reason)
            await ctx.send(f"{member.mention} foi desbanido.  Motivo: {reason}.", delete_after=5)
        else:
            await ctx.send("Não foi possível desbanir este usuário", delete_after=5)
    else:
        await ctx.send(f"{ctx.author.mention} Você não tem permissão para usar este comando", delete_after=5)

async def mute(ctx, member: discord.Member = None, *, reason: str = None):
    """Muta um membro no servidor."""
    if ctx.author.guild_permissions.administrator:
        if member is None:
            await ctx.send("Você precisa mencionar um membro para silenciar. Exemplo: `!mute @Usuário [motivo]`")
        muted_role = discord.utils.get(ctx.guild.roles, name="Silenciado")
        if muted_role is None:
            muted_role = await ctx.guild.create_role(name="Silenciado")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)

    if muted_role in member.roles:
        await ctx.send(f"{member.mention} já está silenciado.")
        return

    await member.add_roles(muted_role, reason=reason)
    if  reason is None:
        await ctx.send(f"{member.mention} foi silenciado.")
    elif reason !=  None:
        await ctx.send(f"{member.mention} foi silenciado. Motivo: {reason}")

async def unmute(ctx, member: discord.Member = None):
    """Desmuta um membro no servidor."""
    if ctx.author.guild_permissions.administrator:
        if member is None:
            await ctx.send("Você precisa mencionar um membro para desmutar. Exemplo: `!unmute @Usuário`")
            return

        muted_role = discord.utils.get(ctx.guild.roles, name="Silenciado")
        if muted_role is None:
            await ctx.send("O cargo 'Silenciado' não existe. Parece que ninguém foi mutado.")
            return

        if muted_role not in member.roles:
            await ctx.send(f"{member.mention} não está silenciado.")
            return

        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} foi desmutado.")

async def lock(ctx):
    """Bloqueia o canal atual para que apenas administradores possam enviar mensagens."""
    if ctx.author.guild_permissions.administrator:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("Este canal foi bloqueado. Apenas administradores podem enviar mensagens.")
    else:
        await ctx.send("Você não tem permissão para bloquear este canal.")

async def unlock(ctx):
    """Desbloqueia o canal atual, permitindo que todos enviem mensagens novamente."""
    if ctx.author.guild_permissions.administrator:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("Este canal foi desbloqueado. Todos podem enviar mensagens novamente.")
    else:
        await ctx.send("Você não tem permissão para desbloquear este canal.")

async def add_role(ctx, member: discord.Member = None, role: discord.Role = None):
    """Adiciona um cargo ao membro."""
    if member is None or role is None:
        await ctx.send("Você precisa mencionar um usuário e um cargo válido. Exemplo: `!add_role @Usuário @Cargo`")
        return

    if role not in ctx.guild.roles:
        await ctx.send(f"O cargo '{role.name}' não existe no servidor.")
        return

    if member not in ctx.guild.members:
        await ctx.send(f"O membro {member.mention} não foi encontrado no servidor.")
        return

    await member.add_roles(role)
    await ctx.send(f"{member.mention} agora possui o cargo {role.name}.")
    
async def remove_role(ctx, member: discord.Member = None, role: discord.Role = None):
    """Remove um cargo do membro."""
    if member is None or role is None:
        await ctx.send("Você precisa mencionar um usuário e um cargo válido. Exemplo: `!remove_role @Usuário @Cargo`")
        return

    if role not in ctx.guild.roles:
        await ctx.send(f"O cargo '{role.name}' não existe no servidor.")
        return

    if member not in ctx.guild.members:
        await ctx.send(f"O membro {member.mention} não foi encontrado no servidor.")
        return

    await member.remove_roles(role)
    await ctx.send(f"O cargo {role.name} foi removido de {member.mention}.")


async def nick(ctx, member: discord.Member = None, *, nickname: str = None):
    """Muda o apelido de um membro para o valor especificado."""
    if ctx.author.guild_permissions.administrator:
        if member is None or nickname is None:
            await ctx.send("Você precisa mencionar um usuário e fornecer um novo apelido. Exemplo: `!nick @Usuário NovoApelido`")
            return
        
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Você não pode alterar o apelido desse usuário porque ele tem um cargo igual ou superior ao seu.")
            return
        
        try:
            await member.edit(nick=nickname)
            await ctx.send(f"O apelido de {member.mention} foi alterado para `{nickname}`.")
        except discord.Forbidden:
            await ctx.send("Eu não tenho permissão para alterar o apelido desse usuário.")
        except discord.HTTPException as e:
            await ctx.send(f"Ocorreu um erro ao tentar alterar o apelido: {e}")