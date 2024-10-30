import discord
from discord.ext import commands
from config import TOKEN
import json
import os
from typed.admin_commands import kick, ban, clear, unban, mute, unmute, lock, unlock, add_role, remove_role, nick
from typed.user_commands import ping, invite, somar, dividir, subtrair, multiplicar, say, nrandom, hug, slap, kiss, coinflip
from typed.utility_commands import traduzir, cat, img
from typed.info_commands import info, userinfo, serverinfo, avatar
from typed.weather_commands import clima
from typed.waifu_commands import waifu
from typed.genshin_commands import playergi, char, chars
from typed.img_commands import invertx, inverty, grayscale, text
from slash.slash_infoCommands import *
from slash.slash_userCommands import *
from slash.slash_adminCommands import *
from slash.slash_waifuCommands import *
from slash.slash_utilityCommands import *
from slash.slash_watherCommands import*

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True









bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command('help')

@bot.command(name='help', description='Mostra ajuda sobre os comandos do bot')
async def help(ctx):
    embed = discord.Embed(
        title='Ajuda do Bot',
        description='Para ver a lista completa de comandos do bot, por favor visite o seguinte site:',
        color=0x00ff00
    )
    embed.add_field(
        name='Lista de Comandos',
        value='[Clique aqui para ver os comandos](https://yukibot.squareweb.app/#comandos)',
        inline=False
    )

    await ctx.send(embed=embed)


def load_autoroles():
    if os.path.exists("autoroles.json"):
        with open("autoroles.json", "r") as file:
            return json.load(file)
    return {}

def save_autoroles(autoroles):
    with open("autoroles.json", "w") as file:
        json.dump(autoroles, file, indent=4)


autoroles = load_autoroles()

@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in autoroles:
        roles = autoroles[guild_id]
        for role_id in roles:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role)
                    print(f"Role {role.name} added to {member.name}")
                except discord.Forbidden:
                    print(f"Missing permissions to add role {role.name} to {member.name}")
                except Exception as e:
                    print(f"Failed to add role {role.name} to {member.name}: {e}")

@bot.command(name="autorole_add")
@commands.has_permissions(administrator=True)
async def autorole_add(ctx, role: discord.Role):
    guild_id = str(ctx.guild.id)
    if guild_id not in autoroles:
        autoroles[guild_id] = []
    if str(role.id) not in autoroles[guild_id]:
        autoroles[guild_id].append(str(role.id))
        save_autoroles(autoroles)
        await ctx.send(f"O cargo: {role.name} foi adicionado ao autorole.")
    else:
        await ctx.send(f"O cargo: {role.name} já está no autorole.")


@bot.command(name="autorole_remove")
@commands.has_permissions(administrator=True)
async def autorole_remove(ctx, role: discord.Role):
    guild_id = str(ctx.guild.id)
    if guild_id in autoroles and str(role.id) in autoroles[guild_id]:
        autoroles[guild_id].remove(str(role.id))
        if not autoroles[guild_id]:
            del autoroles[guild_id]
        save_autoroles(autoroles)
        await ctx.send(f"O cargo: {role.name} foi removido do autorole.")
    else:
        await ctx.send(f"O cargo {role.name} não está no autorole.")


@bot.command(name="autorole_list")
async def autorole_list(ctx):
    guild_id = str(ctx.guild.id)
    if guild_id in autoroles and autoroles[guild_id]:
        role_names = [ctx.guild.get_role(int(role_id)).name for role_id in autoroles[guild_id]]
        await ctx.send(f"Lista de autoroles do servidor: {', '.join(role_names)}")
    else:
        await ctx.send("O servidor não tem autoroles ativos.")





bot.add_command(commands.Command(kick, name='kick', description='Expulsa  um membro do servidor'))
bot.add_command(commands.Command(ban, name='ban', description='Bane  um membro do servidor'))
bot.add_command(commands.Command(clear, name='clear', description='Limpa  mensagens do servidor'))
bot.add_command(commands.Command(userinfo, name='userinfo', description='Mostra informações do usuário'))
bot.add_command(commands.Command(ping, name='ping', description='Ping Pong'))
bot.add_command(commands.Command(info, name='info', description='Mostra informações do servidor'))
bot.add_command(commands.Command(clima, name='clima', description='Mostra o clima de uma cidade'))
bot.add_command(commands.Command(traduzir, name='traduzir', description='Traduz uma frase'))
bot.add_command(commands.Command(cat, name='cat', description='Mostra uma imagem de gato'))
bot.add_command(commands.Command(invite, name='invite', description='Mostra o link de convite do servidor'))
bot.add_command(commands.Command(unban, name='unban', description='Desbane um membro do servidor'))
bot.add_command(commands.Command(somar, name='somar', description='Soma dois números'))
bot.add_command(commands.Command(subtrair, name='subtrair', description='Subtrai dois números'))
bot.add_command(commands.Command(dividir, name='dividir', description='Divide dois números'))
bot.add_command(commands.Command(multiplicar, name='multiplicar', description='Multiplica dois números'))
bot.add_command(commands.Command(mute, name='mute', description='Silencia um membro do servidor'))
bot.add_command(commands.Command(unmute, name='unmute', description='Desativa o silenciamento de um membro do servidor'))
bot.add_command(commands.Command(lock, name='lock', description='Bloqueia o chat para apenas administradores'))
bot.add_command(commands.Command(unlock, name='unlock', description='Desbloqueia o chat'))
bot.add_command(commands.Command(add_role, name='add_role', description='Adiciona um cargo a um membro do servidor'))
bot.add_command(commands.Command(remove_role, name='remove_role', description='Remove um cargo de um membro do servidor'))
bot.add_command(commands.Command(say, name='say', description='Faz com que o bot diga uma frase'))
bot.add_command(commands.Command(nrandom, name='nrandom', description='Gera um número aleatório'))
bot.add_command(commands.Command(hug, name='hug', description='Dá em abraço algum membro'))
bot.add_command(commands.Command(kiss, name='kiss', description='Dá um beijo em algum membro'))
bot.add_command(commands.Command(slap, name='slap', description='Dar um tapa em algum usuário'))
bot.add_command(commands.Command(serverinfo, name='serverinfo', description='Mostra informações do servidor'))
bot.add_command(commands.Command(waifu, name='waifu', description='Gera uma imagem de waifu'))
bot.add_command(commands.Command(img, name='img', description='Busca uma imagem de acordo com a pesquisa'))
bot.add_command(commands.Command(playergi, name='playergi', description='Exibe informações gerais do perfil do jogador.'))
bot.add_command(commands.Command(chars, name='chars', description='Lista os personagens do jogador com seus respectivos níveis.'))
bot.add_command(commands.Command(char, name='char', description='Mostra as informações de um char.'))
bot.add_command(commands.Command(nick, name='nick', description='Altera o apelido de um usuário.'))
bot.add_command(commands.Command(coinflip, name='coinflip', description='Gira uma moeda.'))
bot.add_command(commands.Command(avatar, name='avatar', description='Mostra o avatar de um usuário.'))
bot.add_command(commands.Command(invertx, name='invertx', description='Inverte a imagem enviada no eixo x.'))
bot.add_command(commands.Command(inverty, name='inverty', description='Inverte a imagem enviada no eixo y.'))
bot.add_command(commands.Command(grayscale, name='grayscale', description='Deixe uma imagem em preto e branco.'))
bot.add_command(commands.Command(text, name='text', description='Adiciona texto à imagem.'))






async def sync_commands(guild_id=None):
    """Sincroniza comandos de slash com uma guilda específica ou globalmente."""
    if guild_id:
        guild = discord.Object(id=guild_id)
        bot.tree.add_command(app_commands.Command(name='userinfo', description='Mostrar informações sobre um usuário', callback=slash_userinfo))
        bot.tree.add_command(app_commands.Command(name='info', description='Informações do bot', callback=slash_info))
        bot.tree.add_command(app_commands.Command(name='serverinfo', description='Informações do servidor', callback=slash_serverinfo))
        bot.tree.add_command(app_commands.Command(name='ping', description='Ping Pong', callback=slash_ping))
        bot.tree.add_command(app_commands.Command(name='invite', description='Cria um convite para o canal atual', callback=slash_invite))
        bot.tree.add_command(app_commands.Command(name='somar', description='Soma dois números', callback=slash_somar))
        bot.tree.add_command(app_commands.Command(name='subtrair', description='Subtrai dois números', callback=slash_subtrair))
        bot.tree.add_command(app_commands.Command(name='dividir', description='Divide dois números', callback=slash_dividir))
        bot.tree.add_command(app_commands.Command(name='multiplicar', description='Multiplica dois números', callback=slash_multiplicar))
        bot.tree.add_command(app_commands.Command(name='say', description='Retorna o texto fornecido', callback=slash_say))
        bot.tree.add_command(app_commands.Command(name='random', description='Gera um número aleatório entre dois números', callback=slash_random))
        bot.tree.add_command(app_commands.Command(name='hug', description='Dá um abraço em alguém', callback=slash_hug))
        bot.tree.add_command(app_commands.Command(name='kiss', description='Dá um beijo em alguém', callback=slash_kiss))
        bot.tree.add_command(app_commands.Command(name='slap', description='Dá um tapa em alguém', callback=slash_slap))
        bot.tree.add_command(app_commands.Command(name='kick', description='Expulsar um membro do servidor', callback=slash_kick))
        bot.tree.add_command(app_commands.Command(name='ban', description='Banir um membro do servidor por menção ou ID', callback=slash_ban))
        bot.tree.add_command(app_commands.Command(name='clear', description='Limpar mensagens do servidor', callback=slash_clear))
        bot.tree.add_command(app_commands.Command(name='mute', description='Muta um membro no servidor', callback=slash_mute))
        bot.tree.add_command(app_commands.Command(name='unmute', description='Desmuta um membro no servidor', callback=slash_unmute))
        bot.tree.add_command(app_commands.Command(name='lock', description='Bloqueia o canal atual', callback=slash_lock))
        bot.tree.add_command(app_commands.Command(name='unlock', description='Desbloqueia o canal atual', callback=slash_unlock))
        bot.tree.add_command(app_commands.Command(name='add_role', description='Adiciona um cargo ao membro', callback=slash_add_role))
        bot.tree.add_command(app_commands.Command(name='remove_role', description='Remove um cargo do membro', callback=slash_remove_role))
        bot.tree.add_command(app_commands.Command(name='waifu', description='Gera uma imagem de waifu', callback=slash_waifu))
        bot.tree.add_command(app_commands.Command(name='clima', description='Mostra informações climáticas', callback=slash_clima))
        bot.tree.add_command(app_commands.Command(name='img', description='Gera imagem com base na pesquisa', callback=slash_img))
        bot.tree.add_command(app_commands.Command(name='cat', description='Gera a imagem de um gato', callback=slash_cat))
        bot.tree.add_command(app_commands.Command(name='traduzir', description='Traduz um texto para outro idioma', callback=slash_traduzir))
        bot.tree.add_command(app_commands.Command(name='coinflip', description='Gira uma moeda', callback=slash_coinflip))



        await bot.tree.sync(guild=guild)
        print(f"Comandos sincronizados com a guilda {guild_id}.")
    else:
        bot.tree.add_command(app_commands.Command(name='userinfo', description='Mostrar informações sobre um usuário', callback=slash_userinfo))
        bot.tree.add_command(app_commands.Command(name='info', description='Informações do bot', callback=slash_info))
        bot.tree.add_command(app_commands.Command(name='serverinfo', description='Informações do servidor', callback=slash_serverinfo))
        bot.tree.add_command(app_commands.Command(name='invite', description='Cria um convite para o canal atual', callback=slash_invite))
        bot.tree.add_command(app_commands.Command(name='somar', description='Soma dois números', callback=slash_somar))
        bot.tree.add_command(app_commands.Command(name='subtrair', description='Subtrai dois números', callback=slash_subtrair))
        bot.tree.add_command(app_commands.Command(name='dividir', description='Divide dois números', callback=slash_dividir))
        bot.tree.add_command(app_commands.Command(name='multiplicar', description='Multiplica dois números', callback=slash_multiplicar))
        bot.tree.add_command(app_commands.Command(name='say', description='Retorna o texto fornecido', callback=slash_say))
        bot.tree.add_command(app_commands.Command(name='random', description='Gera um número aleatório entre dois números', callback=slash_random))
        bot.tree.add_command(app_commands.Command(name='hug', description='Dá um abraço em alguém', callback=slash_hug))
        bot.tree.add_command(app_commands.Command(name='kiss', description='Dá um beijo em alguém', callback=slash_kiss))
        bot.tree.add_command(app_commands.Command(name='slap', description='Dá um tapa em alguém', callback=slash_slap))
        bot.tree.add_command(app_commands.Command(name='kick', description='Expulsar um membro do servidor', callback=slash_kick))
        bot.tree.add_command(app_commands.Command(name='ban', description='Banir um membro do servidor por menção ou ID', callback=slash_ban))
        bot.tree.add_command(app_commands.Command(name='clear', description='Limpar mensagens do servidor', callback=slash_clear))
        bot.tree.add_command(app_commands.Command(name='mute', description='Muta um membro no servidor', callback=slash_mute))
        bot.tree.add_command(app_commands.Command(name='unmute', description='Desmuta um membro no servidor', callback=slash_unmute))
        bot.tree.add_command(app_commands.Command(name='lock', description='Bloqueia o canal atual', callback=slash_lock))
        bot.tree.add_command(app_commands.Command(name='unlock', description='Desbloqueia o canal atual', callback=slash_unlock))
        bot.tree.add_command(app_commands.Command(name='add_role', description='Adiciona um cargo ao membro', callback=slash_add_role))
        bot.tree.add_command(app_commands.Command(name='remove_role', description='Remove um cargo do membro', callback=slash_remove_role))
        bot.tree.add_command(app_commands.Command(name='waifu', description='Gera uma imagem de waifu', callback=slash_waifu))
        bot.tree.add_command(app_commands.Command(name='clima', description='Mostra informações climáticas', callback=slash_clima))
        bot.tree.add_command(app_commands.Command(name='img', description='Gera imagem com base na pesquisa', callback=slash_img))
        bot.tree.add_command(app_commands.Command(name='cat', description='Gera a imagem de um gato', callback=slash_cat))
        bot.tree.add_command(app_commands.Command(name='traduzir', description='Traduz um texto para outro idioma', callback=slash_traduzir))
        bot.tree.add_command(app_commands.Command(name='coinflip', description='Gira uma moeda', callback=slash_coinflip))
        bot.tree.add_command(app_commands.Command(name='avatar', description='Mostrar o avatar de um usuário', callback=slash_avatar))



        await bot.tree.sync()
        print("Comandos sincronizados globalmente.")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    activity = discord.CustomActivity(
        name="Online!",
        )
    await bot.change_presence(activity=activity)
    await sync_commands()

@bot.event
async def on_guild_join(guild):
    print(f'Joined a new guild: {guild.name} (ID: {guild.id})')
    await sync_commands(guild_id=guild.id)


bot.run(TOKEN)


