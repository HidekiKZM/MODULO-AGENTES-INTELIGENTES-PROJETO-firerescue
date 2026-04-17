from fire_system import FireSystem

class Environment:
    # Usando constantes na classe para evitar "magic strings"
    EMPTY = '.'
    FIRE = 'F'
    VICTIM = 'V'
    EXIT = 'E'
    WALL = '#'

    def __init__(self, grid_size: int, fire_spread_chance: float, 
                 pos_vitima=(2,2), pos_fogo=(4,4), pos_saida=(9,9)):
        self.size = grid_size
        self.grid = [[self.EMPTY for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Agora as posições são dinâmicas, passadas por parâmetro
        self.grid[pos_vitima[0]][pos_vitima[1]] = self.VICTIM
        self.grid[pos_fogo[0]][pos_fogo[1]] = self.FIRE
        self.grid[pos_saida[0]][pos_saida[1]] = self.EXIT
        
        # Adicionando uma parede de exemplo (pode ser passada como lista futuramente)
        self.grid[4][5] = self.WALL
        
        self.fire_system = FireSystem(spread_chance=fire_spread_chance)
        self.score = 0
        self.game_over = False # Flag para controlar o fim da simulação

    def update_fire_and_smoke(self):
        self.grid = self.fire_system.update(self.grid, self.size)

    def get_perception_llm(self, agent_pos: tuple) -> str:
        """Gera um texto de visão limitando a percepção (POMDP) para o Bombeiro."""
        x, y = agent_pos
        
        # Dicionário de tradução direta
        traducao = {
            self.EMPTY: 'Espaço Livre', 
            self.FIRE: 'Fogo', 
            self.VICTIM: 'Vítima', 
            self.EXIT: 'Saída de Emergência', 
            self.WALL: 'Parede'
        }
        
        # Coleta a visão verificando os limites do grid de forma mais segura e limpa
        visao = []
        if x > 0: visao.append(f"NORTE tem {traducao.get(self.grid[x-1][y], 'Desconhecido')}")
        if x < self.size - 1: visao.append(f"SUL tem {traducao.get(self.grid[x+1][y], 'Desconhecido')}")
        if y > 0: visao.append(f"OESTE tem {traducao.get(self.grid[x][y-1], 'Desconhecido')}")
        if y < self.size - 1: visao.append(f"LESTE tem {traducao.get(self.grid[x][y+1], 'Desconhecido')}")
        
        percepcao_str = ", ".join(visao)
        return f"Você está na posição ({x},{y}). Visão local: {percepcao_str}."

    def get_perception_robot(self, robot_pos: tuple, firefighter_pos: tuple) -> dict:
        """O Robô possui sensor exato de coordenadas (Totalmente Observável)."""
        return {"pos_robo": robot_pos, "pos_bombeiro": firefighter_pos}

    def apply_action(self, agent, action: str) -> str:
        """
        Aplica a ação e retorna uma mensagem de feedback (útil para o histórico do LLM).
        """
        x, y = agent.pos
        nova_pos = (x, y)

        # 1. Calcula a intenção de movimento
        if action == "MOVER_SUL" and x < self.size - 1: nova_pos = (x+1, y)
        elif action == "MOVER_NORTE" and x > 0: nova_pos = (x-1, y)
        elif action == "MOVER_LESTE" and y < self.size - 1: nova_pos = (x, y+1)
        elif action == "MOVER_OESTE" and y > 0: nova_pos = (x, y-1)
        else:
            return "Movimento inválido ou limite do mapa atingido."

        # 2. Verifica colisão com parede
        if self.grid[nova_pos[0]][nova_pos[1]] == self.WALL:
            return "Você bateu em uma parede e não saiu do lugar."

        # 3. Executa o movimento
        agent.pos = nova_pos
        conteudo_celula = self.grid[nova_pos[0]][nova_pos[1]]

        # 4. Avalia interação com o ambiente
        if conteudo_celula == self.FIRE:
            self.score -= 50
            self.game_over = True
            return "ALERTA CRÍTICO: Você pisou no fogo!"
        elif conteudo_celula == self.VICTIM:
            self.score += 100
            self.grid[nova_pos[0]][nova_pos[1]] = self.EMPTY # Remove a vítima do mapa
            return "Sucesso: Você resgatou a vítima!"
        elif conteudo_celula == self.EXIT:
            self.score += 50
            self.game_over = True
            return "Você alcançou a saída de emergência."

        return "Movimento realizado com sucesso para espaço livre."

    def compute_score(self):
        # Penalidade padrão por tempo/turno
        self.score -= 1 

    def render(self, pos_bombeiro: tuple, pos_robo: tuple):
        print("\n" + "=" * (self.size * 3))
        for i in range(self.size):
            row_str = ""
            for j in range(self.size):
                if (i, j) == pos_bombeiro: row_str += "A1 "
                elif (i, j) == pos_robo: row_str += "A2 "
                else: row_str += f"{self.grid[i][j]}  "
            print(row_str)
        print("=" * (self.size * 3))
        print(f"🏆 Score Global: {self.score}")