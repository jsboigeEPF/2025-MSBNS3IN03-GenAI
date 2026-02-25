from google import genai
from src.config import API_KEY

client = genai.Client(api_key=API_KEY)

def review_code(diff_text, level="senior"):
    """
    Envoie le diff de code à l'IA avec un ton adapté au niveau choisi.
    """
    print(f"🧠 Analyse du code en cours (Niveau: {level.upper()})...")
    
    # 1. On personnalise la consigne selon le niveau choisi par l'utilisateur
    if level == "junior":
        consignes_niveau = """
        Le développeur qui a écrit ce code est un profil Junior / Débutant. 
        Ton ton doit être extrêmement pédagogique, bienveillant et encourageant.
        Prends le temps d'expliquer *pourquoi* une pratique est mauvaise, donne des définitions claires des concepts de base, et explique comment ta correction fonctionne étape par étape. Évite le jargon trop complexe sans l'expliquer.
        """
    else:
        consignes_niveau = """
        Le développeur qui a écrit ce code est un profil Senior / Expert. 
        Ton ton doit être direct, concis et purement technique. 
        Va droit au but. Ne fais aucune pédagogie sur les concepts de base. Concentre-toi uniquement sur l'architecture, l'optimisation algorithmique avancée, les failles de sécurité critiques et les subtilités du langage.
        """

    # 2. On intègre ces consignes dans le Prompt principal
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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise Exception(f"❌ Erreur lors de la communication avec l'IA : {e}")