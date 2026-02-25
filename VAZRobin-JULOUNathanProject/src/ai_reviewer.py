from openai import OpenAI
from src.config import API_KEY

# On garde le base_url d'OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

def review_code(diff_text, level="senior"):
    """
    Envoie le diff de code à l'IA avec un ton adapté au niveau choisi.
    """
    print(f"🧠 Analyse du code en cours (Niveau: {level.upper()})...")

    # On personnalise la consigne selon le niveau choisi par l'utilisateur
    if level == "junior":
        consignes_niveau = """
        Le développeur qui a écrit ce code est un profil Junior / Débutant.
        Ton ton doit être extrêmement pédagogique, bienveillant et encourageant.
        
        ATTENTION : Ta réponse doit être LONGUE, DÉTAILLÉE et EXHAUSTIVE.
        Tu dois agir comme un mentor dévoué :
        - EXPLIQUE EN PROFONDEUR : Ne te contente pas de corriger, explique exactement *pourquoi* la pratique initiale pose problème (mémoire, sécurité, lisibilité, etc.).
        - DÉFINIS LES CONCEPTS : Donne des définitions claires, avec des analogies si possible, pour chaque concept technique rencontré.
        - DÉTAILLE LE CODE : Lorsque tu proposes du code corrigé, ajoute beaucoup de commentaires directement dans le code pour expliquer chaque ligne modifiée.
        - DÉCOMPOSE : Explique ton raisonnement étape par étape de manière très explicite.
        N'hésite pas à être prolixe et à faire une réponse très longue pour t'assurer que le débutant comprenne chaque notion de A à Z.
        """
    else:
        consignes_niveau = """
        Le développeur qui a écrit ce code est un profil Senior / Expert.
        Ton ton doit être direct, concis et purement technique.
        Va droit au but. Ne fais aucune pédagogie sur les concepts de base. Concentre-toi uniquement sur l'architecture, l'optimisation algorithmique avancée, les failles de sécurité critiques et les subtilités du langage.
        """

    # On intègre ces consignes dans le Prompt principal
    prompt = f"""
    Tu es un expert en revue de code (Code Review).
    Ton objectif est d'analyser le diff git suivant et de fournir des retours.

    {consignes_niveau}

    Voici tes missions générales :
    1. Résumer brièvement ce que fait cette modification.
    2. Détecter des bugs potentiels ou des failles de sécurité.
    3. Suggérer des améliorations avec du code.

    Utilise le format Markdown pour ta réponse.

    Voici le diff à analyser :
    ```diff
    {diff_text}
    ```
    """

    try:
        print(f"📡 Appel à l'API via OpenRouter avec le modèle anthropic/claude-3.5-sonnet...")
        print(f"📊 Taille du prompt: {len(prompt)} caractères")

        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {
                    "role": "system", 
                    "content": "Tu es un expert en revue de code. Tu dois IMPÉRATIVEMENT structurer toute ta réponse avec du Markdown valide (utilise des ### pour chaque catégorie de tes suggestions)."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur API: {error_msg}")
        raise Exception(f"❌ Erreur lors de la communication avec l'IA : {error_msg}")

def chat_with_ia(messages_history):
    """
    Continue la conversation en envoyant tout l'historique du chat à l'IA.
    """
    print(f"💬 Relance de l'IA pour le chat (Historique: {len(messages_history)} messages)")
    
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=messages_history,
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur API Chat: {error_msg}")
        raise Exception(f"Erreur lors du chat avec l'IA : {error_msg}")