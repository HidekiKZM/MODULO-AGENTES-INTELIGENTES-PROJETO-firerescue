import json
import google.generativeai as genai

class FirefighterLLM:
    def __init__(self, agent_id: str, start_pos: tuple, api_key: str):
        self.id = agent_id
        self.pos = start_pos
        self.energy = 100
        self.memory = [] # Nova lista para evitar loops infinitos batendo em paredes
        
        genai.configure(api_key=api_key)
        
        # System Instruction: Define a persona fixamente, economizando tokens no loop
        system_prompt = """Você é um agente bombeiro operando em um prédio em chamas.
        Seus objetivos prioritários:
        1. Resgatar vítimas.
        2. Evitar o fogo a todo custo.
        3. Encontrar a saída de emergência.
        Aja de forma estritamente lógica e use seu histórico recente para não repetir erros (como bater na mesma parede duas vezes).
        """
        
        # Configurando o modelo para forçar saída em JSON puro nativamente
        self.model = genai.GenerativeModel(
            model_name='models/gemini-2.5-flash',
            system_instruction=system_prompt,
            generation_config={"response_mime_type": "application/json"}
        )

    def decide(self, perception_text: str, feedback_anterior: str = "") -> str:
        # 1. Atualiza a memória com o resultado do turno anterior
        if feedback_anterior:
            self.memory.append(f"Resultado anterior: {feedback_anterior}")
            # Mantém apenas os últimos 3 eventos para não sobrecarregar o prompt
            if len(self.memory) > 3:
                self.memory.pop(0)

        historico_str = "\n".join(self.memory) if self.memory else "Nenhum passo dado ainda."

        # 2. Monta o prompt dinâmico do turno
        # Nota: Ajustei as ações válidas para refletirem o que o environment.py realmente aceita
        prompt = f"""
        Percepção atual da visão: {perception_text}
        Energia atual: {self.energy}%
        
        Histórico dos últimos passos:
        {historico_str}
        
        Ações válidas disponíveis: "MOVER_NORTE", "MOVER_SUL", "MOVER_LESTE", "MOVER_OESTE", "ESPERAR".
        (Lembrete: Para resgatar a vítima, basta se mover para o espaço onde ela está).
        
        Responda obrigatoriamente seguindo este esquema de chaves:
        {{"acao": "ACAO_ESCOLHIDA", "raciocinio": "Sua linha de pensamento explicada de forma curta"}}
        """
        
        try:
            # 3. Chama a API
            response = self.model.generate_content(prompt)
            decision_data = json.loads(response.text)
            
            acao_escolhida = decision_data.get("acao", "ESPERAR")
            
            # Salva o que ele decidiu fazer para compor a memória do próximo turno
            self.memory.append(f"Eu decidi: {acao_escolhida}")
            
            print(f"🔥 [{self.id}] Pensamento: {decision_data.get('raciocinio')}")
            print(f"➡️ [{self.id}] Ação escolhida: {acao_escolhida}")
            
            return acao_escolhida
            
        except Exception as e:
            print(f"⚠️ [{self.id}] Falha de processamento na API ou JSON: {e}")
            return "ESPERAR"