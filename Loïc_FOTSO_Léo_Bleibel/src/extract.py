import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_and_extract(url: str, timeout: int = 12) -> str:
    """Télécharge une page et extrait un texte lisible (basique)."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # enlève scripts/styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # nettoyage simple
        text = " ".join(text.split())

        return text[:8000]

    except Exception:
        return ""