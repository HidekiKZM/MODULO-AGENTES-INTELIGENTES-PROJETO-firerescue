import time
from environment import Environment
from agent_llm import FirefighterLLM
from agent_goal import SupportRobot
from config import GRID_SIZE, MAX_TURNS, GEMINI_API_KEY, FIRE_SPREAD_CHANCE

def main():
    if not GEMINI_API_KEY:
        print("ERRO CRÍTICO: GEMINI_API_KEY não foi configurada no arquivo .env!")
        return 
        
    print("🚒 Inicializando FireRescue Agents Sim...")
    env = Environment(grid_size=GRID_SIZE, fire_spread_chance=FIRE_SPREAD_CHANCE)
    
    # Instanciando agentes
    bombeiro = FirefighterLLM(agent_id="A1", start_pos=(0, 0), api_key=GEMINI_API_KEY)
    robo = SupportRobot(agent_id="A2", start_pos=(9, 9))
    
    rodada = 1

    # O Ciclo Agente-Ambiente Clássico
    while rodada <= MAX_TURNS:
        print(f"\n--- ⏱️ Rodada {rodada}/{MAX_TURNS} ---")
        
        # 1. Mundo Dinâmico: Fogo se espalha
        env.update_fire_and_smoke()
        
        # 2. Sensores: Agentes percebem o mundo
        percepcao_bombeiro = env.get_perception_llm(bombeiro.pos)
        percepcao_robo = env.get_perception_robot(robo.pos, bombeiro.pos)
        
        # 3. Decisão: Cérebros escolhem ação
        acao_bombeiro = bombeiro.decide(percepcao_bombeiro)
        acao_robo = robo.decide(percepcao_robo)
        print(f"🤖 [Robô A2] Ação decidida: {acao_robo}")
        
        # 4. Atuadores: Aplicando ações no ambiente
        env.apply_action(bombeiro, acao_bombeiro)
        env.apply_action(robo, acao_robo)
        
        # 5. Avaliação e Renderização
        env.compute_score()
        env.render(bombeiro.pos, robo.pos)
        
        # Verifica fim de jogo
        if getattr(env, 'game_over', False):
            break
            
        # Pausa para não estourar a cota gratuita do Gemini
        time.sleep(6)
        rodada += 1

if __name__ == "__main__":
    main()
    print("Simulação de Resgate de Incêndio Finalizada!")