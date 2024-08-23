import discord
from discord.ext import commands
from config import TOKEN
from admin_commands import kick, ban, clear, unban, mute, unmute, lock, unlock, add_role, remove_role, nick
from user_commands import ping, invite, somar, dividir, subtrair, multiplicar, say, nrandom, hug, slap, kiss, coinflip
from utility_commands import traduzir, cat, img
from info_commands import info, userinfo, serverinfo
from music_commands import play, skip, queue, stop, leave
from weather_commands import clima
from waifu_commands import waifu
from genshin_commands import playergi, char, chars
from slash_infoCommands import *
from slash_userCommands import *
from slash_adminCommands import *
from slash_waifuCommands import *
from slash_utilityCommands import *
from slash_watherCommands import*

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

@bot.command(name='help', description='Mostra ajuda sobre os comandos do bot')
async def help(ctx):
    embed = discord.Embed(title='Ajuda do Bot', description='Lista de comandos do bot', color=0x00ff00)

    comandos = [
        ('Admin', ['kick', 'ban', 'clear', 'unban', 'mute', 'unmute', 'lock', 'unlock', 'add_role', 'remove_role', 'nick']),
        ('Usuário', ['ping', 'invite', 'say', 'hug', 'slap', 'kiss']),
        ('Utilidade', ['clima', 'traduzir', 'cat', 'somar', 'dividir', 'subtrair', 'multiplicar', 'random']),
        ('Informação', ['info', 'userinfo', 'serverinfo']),
        ('Música', ['play', 'skip', 'queue', 'stop', 'leave']),
        ('Genshin',  ['playergi', 'char', 'chars'])
    ]

    for categoria, comandos_categoria in comandos:
        embed.add_field(name=categoria, value=', '.join(comandos_categoria), inline=False)

    await ctx.send(embed=embed)



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
bot.add_command(commands.Command(play, name='play', description='Toca uma música'))
bot.add_command(commands.Command(skip, name='skip', description='Pula a música atual'))
bot.add_command(commands.Command(queue, name='queue', description='Mostra a fila de músicas'))
bot.add_command(commands.Command(stop, name='stop', description='Para a música atual'))
bot.add_command(commands.Command(leave, name='leave', description='Deixa a sala de música'))
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
        bot.tree.add_command(app_commands.Command(name='unban', description='Desbanir um membro do servidor', callback=slash_unban))
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
        bot.tree.add_command(app_commands.Command(name='unban', description='Desbanir um membro do servidor', callback=slash_unban))
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


