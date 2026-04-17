def manhattan_distance(pos1: tuple, pos2: tuple) -> int:
    """Heurística para o agente baseado em objetivos calcular distância."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_adjacent_positions(pos: tuple, grid_size: int) -> list:
    """Retorna as coordenadas Norte, Sul, Leste e Oeste válidas."""
    x, y = pos
    adj = []
    if x > 0: adj.append((x - 1, y)) # NORTE
    if x < grid_size - 1: adj.append((x + 1, y)) # SUL
    if y > 0: adj.append((x, y - 1)) # OESTE
    if y < grid_size - 1: adj.append((x, y + 1)) # LESTE
    return adj