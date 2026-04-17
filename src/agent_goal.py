from utils import manhattan_distance

class SupportRobot:
    def __init__(self, agent_id: str, start_pos: tuple):
        self.id = agent_id
        self.pos = start_pos

    def decide(self, perception: dict) -> str:
        """
        Agente Baseado em Objetivos:
        Heurística simples: se mover na direção do Bombeiro para fornecer suporte/água.
        """
        pos_bombeiro = perception.get('pos_bombeiro')
        if not pos_bombeiro:
            return "ESPERAR"

        fx, fy = self.pos
        bx, by = pos_bombeiro

        if manhattan_distance(self.pos, pos_bombeiro) == 1:
            return "RECARREGAR_BOMBEIRO"

        # Tenta reduzir a distância Manhattan de forma gulosa (Greedy)
        if bx > fx: return "MOVER_SUL"
        if bx < fx: return "MOVER_NORTE"
        if by > fy: return "MOVER_LESTE"
        if by < fy: return "MOVER_OESTE"

        return "ESPERAR"