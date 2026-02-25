import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# On récupère la clé API
API_KEY = os.getenv("API_KEY")

# On vérifie que la clé existe bien, sinon on bloque le programme
if not API_KEY:
    raise ValueError("⚠️ Erreur : La clé API est introuvable. Vérifie ton fichier .env !")