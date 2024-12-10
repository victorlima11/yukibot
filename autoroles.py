# autoroles.py
from db import Base, get_session
from sqlalchemy import Column, String

class AutoRole(Base):
    __tablename__ = 'autoroles'
    
    guild_id = Column(String, primary_key=True)
    role_ids = Column(String)

def save_autorole(guild_id, role_ids):
    """Salva ou atualiza o autorole para uma guilda."""
    session = get_session()
    
    # Verifica se o autorole já existe para a guilda
    autorole = session.query(AutoRole).filter_by(guild_id=guild_id).first()

    if autorole:
        # Atualiza o campo role_ids (caso já exista, adiciona mais cargos)
        current_role_ids = autorole.role_ids.split(",") if autorole.role_ids else []
        if str(role_ids) not in current_role_ids:
            current_role_ids.append(str(role_ids))  # Adiciona o novo cargo à lista
        autorole.role_ids = ",".join(current_role_ids)
    else:
        autorole = AutoRole(guild_id=guild_id, role_ids=str(role_ids))
        session.add(autorole)

    session.commit()
    session.close()

def load_autorole(guild_id):
    """Carrega os cargos configurados para autorole."""
    session = get_session()
    autorole = session.query(AutoRole).filter_by(guild_id=guild_id).first()
    session.close()
    
    return autorole.role_ids if autorole else None

def remove_autorole(guild_id, role_ids):
    """Remove um cargo do autorole de uma guilda."""
    session = get_session()
    autorole = session.query(AutoRole).filter_by(guild_id=guild_id).first()
    
    if autorole:
        current_role_ids = autorole.role_ids.split(",") if autorole.role_ids else []
        
        # Verifica se o cargo está na lista de autoroles
        if str(role_ids) in current_role_ids:
            current_role_ids.remove(str(role_ids))  # Remove o cargo da lista
            autorole.role_ids = ",".join(current_role_ids) if current_role_ids else None
            session.commit()
            session.close()
            return True  # Cargo removido com sucesso
    
    session.close()
    return False  # Cargo não encontrado para remoção
