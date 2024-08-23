import discord
from discord.ext import commands
from enkapy import Enka
from enkanetwork import EnkaNetworkAPI



client = Enka()
icon_client = EnkaNetworkAPI() 


async def playergi(ctx, uid: int):
    
    user = await fetch_player_data(uid)
    
    if user:
        embed = discord.Embed(
            title=f"{user.player.nickname} - {user.uid}",
            description="Informações do jogador:",
            color=0x87CEEB
        )
        embed.add_field(name="Nível do Jogador:", value=user.player.level, inline=True)
        embed.add_field(name="Nível de Mundo:", value=user.player.world_level, inline=True)
        embed.add_field(name="Número de Conquistas:", value=user.player.achievement, inline=True)
        embed.add_field(name="Status do Abismo:", value=(f'{user.player.abyss_floor} -  {user.player.abyss_room}'), inline=True)
        

        if user.player.signature:
            embed.add_field(name="Assinatura", value=user.player.signature, inline=False)
        

        if user.player.avatar:
            embed.set_thumbnail(url=user.player.avatar.icon.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Não foi possível encontrar informações para este jogador.")
    
async def chars(ctx, uid: int):
    try:
        await client.load_lang()
        user = await client.fetch_user(uid)
        embed = discord.Embed(title=f"Personagens de {user.player.nickname}", description="**Genshin Impact**")
        
        for char in user.characters:
            embed.add_field(name=char.name, value=f"Nível: {char.level}", inline=False)
        
        if not user.characters:
            embed.add_field(name="Nenhum Personagem Encontrado", value="Este jogador não possui personagens.")
        
        await ctx.send(embed=embed)
    
    except Exception as e:
        await ctx.send(f"Erro ao buscar personagens: {e}")


async def fetch_character_data(uid: int, character_name: str):
    async with EnkaNetworkAPI() as enka:
        player_data = await enka.fetch_user(uid)

        character = next((char for char in player_data.characters if char.name == character_name), None)
        return character

async def fetch_weapon_data(uid: int, character_name: str):
    async with EnkaNetworkAPI() as enka:
        player_data = await enka.fetch_user(uid)
        
        if not player_data or not player_data.characters:
            return None
        
        # Busca o personagem específico
        character = next((c for c in player_data.characters if c.name == character_name), None)
        
        if character:
            for equip in character.equipments:
                if equip.type == 'Weapon':
                    weapon = equip.detail
                    return weapon
        
        return None


async def fetch_player_data(uid: int):
    async with EnkaNetworkAPI() as enka:
        player_data = await enka.fetch_user(uid)
        return player_data


async def char(ctx, uid: int, *, character_name: str):
    """Mostra informações de um personagem específico de um jogador."""
    character_name = ' '.join(word.capitalize() for word in character_name.split())

    character = await fetch_character_data(uid, character_name)
    user = await fetch_player_data(uid)
    weapon = await fetch_weapon_data(uid, character_name)


    
    if character:
        element_map = {
            "Fire": "Pyro",
            "Water": "Hydro",
            "Electric": "Electro",
            "Wind": "Anemo",
            "Ice": "Cryo",
            "Rock": "Geo",
            "Grass": "Dendro"
        }
        element_name = element_map.get(character.element.name, character.element.name)
        constellations_count = sum(1 for c in character.constellations if c.unlocked)

            
        embed = discord.Embed(title=f"Informações sobre {character.name}", description=f"Jogador: {user.player.nickname}", color=0x87CEEB)
        embed.add_field(name="Elemento", value=element_name, inline=True)
        embed.add_field(name="Raridade", value=f"{character.rarity}★", inline=True)
        embed.add_field(name="Nível", value=f"{character.level} / {character.max_level}", inline=True)
        embed.add_field(name="Constelações Desbloqueadas", value=f"C{constellations_count}", inline=True)
        embed.add_field(name="Nível de Amizade", value=character.friendship_level, inline=True)
        
        if weapon:
            embed.add_field(name="Nome da Arma", value=weapon.name, inline=True)
            embed.add_field(name="Nível da Arma", value=weapon.level, inline=True)

        CRIT_RATE = f"{character.stats.FIGHT_PROP_CRITICAL.value * 100:.1f}%"
        STR_HP = f"{character.stats.FIGHT_PROP_MAX_HP.value:.0f}"
        RECARGA = f"{character.stats.FIGHT_PROP_CHARGE_EFFICIENCY.value * 100:.0f}%"
        CRIT_DMG = f"{character.stats.FIGHT_PROP_CRITICAL_HURT.value * 100:.1f}%"
        EM = f"{character.stats.FIGHT_PROP_ELEMENT_MASTERY.value:.0f}"
        ATK = int(character.stats.FIGHT_PROP_CUR_ATTACK.value)
        DEF = int(character.stats.FIGHT_PROP_CUR_DEFENSE.value)
        BONUS_CURA = f"{character.stats.FIGHT_PROP_HEAL_ADD.value * 100:.1f}%"

        embed.add_field(name="HP", value=STR_HP, inline=True)
        embed.add_field(name="ATK", value=ATK, inline=True)
        embed.add_field(name="DEF", value=DEF, inline=True)
        embed.add_field(name="Recarga de Energia", value=RECARGA, inline=True)
        embed.add_field(name="Proficiência", value=EM, inline=True)
        embed.add_field(name="Taxa Crítica", value=CRIT_RATE, inline=True)
        embed.add_field(name="Dano Crítico", value=CRIT_DMG, inline=True)
        embed.add_field(name="Bônus de Cura", value=BONUS_CURA, inline=True)

        elemental_damage = {
            "Bônus de Dano Pyro": character.stats.FIGHT_PROP_FIRE_ADD_HURT.value,
            "Bônus de Dano Cryo": character.stats.FIGHT_PROP_ICE_ADD_HURT.value,
            "Bônus de Dano Electro": character.stats.FIGHT_PROP_ELEC_ADD_HURT.value,
            "Bônus de Dano Hydro": character.stats.FIGHT_PROP_WATER_ADD_HURT.value,
            "Bônus de Dano Geo": character.stats.FIGHT_PROP_ROCK_ADD_HURT.value,
            "Bônus de Dano Anemo": character.stats.FIGHT_PROP_WIND_ADD_HURT.value,
            "Bônus de Dano Dendro": character.stats.FIGHT_PROP_GRASS_ADD_HURT.value
        }

        for name, value in elemental_damage.items():
            if value > 0:
                embed.add_field(name=name, value=f"{value * 100:.1f}%", inline=True)

        if character.image:
            embed.set_image(url=character.image.banner.url)
        
        artifact_info = ""
        weapon_info = ""

        for i, equip in enumerate(character.equipments):
            detail = equip.detail
            if hasattr(detail, 'name'):
                if i == len(character.equipments) - 1:
                    weapon_info += f"- Nome: {detail.name}\n- Nível: {equip.level}\n"
                else:
                    artifact_info += f"- {detail.name}\n"

        if artifact_info:
            pass

        if weapon_info:
            embed.add_field(name="Arma", value=weapon_info, inline=False)
        
        artifact_sets = {}
        for equip in character.equipments:
            if hasattr(equip, 'detail'):
                detail = equip.detail
                if hasattr(detail, 'artifact_name_set') and detail.artifact_name_set:
                    set_name = detail.artifact_name_set
                    if set_name in artifact_sets:
                        artifact_sets[set_name] += 1
                    else:
                        artifact_sets[set_name] = 1
        if artifact_sets:
            sorted_sets = sorted(artifact_sets.items(), key=lambda x: x[1], reverse=True)
            top_sets = sorted_sets[:2] 

            artifact_info = "Artefatos:\n"
            for set_name, count in top_sets:
                artifact_info += f"- {set_name} ({count})\n"

            embed.add_field(name="Quantidade de artefatos:", value=artifact_info, inline=False)
        
        await ctx.send(embed=embed)