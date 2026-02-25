import requests

def get_pr_diff(repo_owner, repo_name, pr_number):
    """
    Récupère le texte 'diff' d'une Pull Request via l'API officielle de GitHub.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    print(f"📡 Récupération via l'API : {url}")
    
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": "Projet-Revieweur-IA-Etudiant" 
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Diff récupéré avec succès !")
        return response.text
    else:
        raise Exception(f"Impossible de récupérer la PR. Code d'erreur : {response.status_code}\nDétails : {response.text}")

# --- Zone de Test ---
if __name__ == "__main__":
    try:
        # On utilise une vraie PR vérifiée du projet Flask (PR 5000)
        test_diff = get_pr_diff("pallets", "flask", 5000)
        
        print("\n--- Aperçu du Diff ---")
        print(test_diff[:500]) 
        print("\n----------------------")
        
    except Exception as e:
        print(e)