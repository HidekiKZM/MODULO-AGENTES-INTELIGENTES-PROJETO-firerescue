import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurações do Ambiente
GRID_SIZE = 10
MAX_TURNS = 5
FIRE_SPREAD_CHANCE = 0.2