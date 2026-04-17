import random
from utils import get_adjacent_positions

class FireSystem:
    def __init__(self, spread_chance: float):
        self.spread_chance = spread_chance

    def update(self, grid: list, grid_size: int) -> list:
        """Aplica a regra estocástica de espalhamento de fogo."""
        # Criamos a cópia para que o fogo não se espalhe por todo o mapa em um só turno
        new_grid = [row[:] for row in grid]
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Se a célula atual tem fogo
                if grid[i][j] == 'F':
                    # Tenta espalhar para os vizinhos
                    for ax, ay in get_adjacent_positions((i, j), grid_size):
                        
                        # O fogo pode se espalhar para: 
                        # '.' (Espaço), 'V' (Vítima) ou 'A1/A2' (Agentes)
                        # O fogo NÃO queima '#' (Paredes)
                        celula_alvo = grid[ax][ay]
                        
                        if celula_alvo not in ['#', 'E', 'F']: 
                            if random.random() < self.spread_chance:
                                new_grid[ax][ay] = 'F'
                                
        return new_grid