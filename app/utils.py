"""
Funções utilitárias do CEITECGAME
"""

def calcular_nivel(xp_total):
    """
    Calcula o nível e nome do nível baseado no XP total
    
    Args:
        xp_total (int): Total de XP acumulado
    
    Returns:
        tuple: (nome_nivel, numero_nivel)
    
    Níveis:
        0-100: Explorador (1)
        101-300: Programador (2)
        301-600: Maker (3)
        601-1000: Engenheiro (4)
        1000+: Mentor (5)
    """
    if xp_total < 100:
        return "Explorador", 1
    elif xp_total < 300:
        return "Programador", 2
    elif xp_total < 600:
        return "Maker", 3
    elif xp_total < 1000:
        return "Engenheiro", 4
    else:
        return "Mentor", 5


def get_progresso_nivel(xp_total):
    """
    Calcula o progresso percentual dentro do nível atual
    
    Args:
        xp_total (int): Total de XP acumulado
    
    Returns:
        dict: {
            'nivel_atual': str,
            'numero_nivel': int,
            'xp_atual': int,
            'xp_proximo': int,
            'progresso': float (0-100)
        }
    """
    niveis = [
        (0, 100, "Explorador", 1),
        (100, 300, "Programador", 2),
        (300, 600, "Maker", 3),
        (600, 1000, "Engenheiro", 4),
        (1000, float('inf'), "Mentor", 5)
    ]
    
    for xp_min, xp_max, nome, numero in niveis:
        if xp_total < xp_max:
            xp_no_nivel = xp_total - xp_min
            xp_necessario = xp_max - xp_min
            
            if xp_necessario == float('inf'):
                progresso = 100.0
            else:
                progresso = (xp_no_nivel / xp_necessario) * 100
            
            return {
                'nivel_atual': nome,
                'numero_nivel': numero,
                'xp_atual': xp_total,
                'xp_proximo': xp_max if xp_max != float('inf') else None,
                'progresso': round(progresso, 1)
            }
    
    # Fallback (não deve acontecer)
    return {
        'nivel_atual': 'Mentor',
        'numero_nivel': 5,
        'xp_atual': xp_total,
        'xp_proximo': None,
        'progresso': 100.0
    }


def get_badge_nivel(numero_nivel):
    """
    Retorna a classe CSS para o badge do nível
    
    Args:
        numero_nivel (int): Número do nível (1-5)
    
    Returns:
        str: Classe CSS do Bootstrap
    """
    badges = {
        1: 'badge-explorador',
        2: 'badge-programador',
        3: 'badge-maker',
        4: 'badge-engenheiro',
        5: 'badge-mentor'
    }
    return badges.get(numero_nivel, 'badge-secondary')
