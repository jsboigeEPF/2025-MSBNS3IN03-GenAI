import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """Tu es un agent de recherche web.
Tu dois produire une synthèse à partir de sources web.
Règles :
- Chaque fait doit être cité via [1], [2], etc.
- Dire explicitement quand une info est incertaine.
- Format : Résumé -> Points clés -> Limites -> Sources
"""

def build_context(question, docs):
    blocks = []
    idx = 1
    for d in docs:
        if not d["text"]:
            continue
        blocks.append(
            f"[{idx}] {d['title']}\nURL: {d['url']}\n{d['text']}\n"
        )
        idx += 1

    return f"QUESTION:\n{question}\n\nSOURCES:\n" + "\n".join(blocks)

def generate_report(question, docs):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = build_context(question, docs)

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content