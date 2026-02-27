#!/usr/bin/env python
"""Script pour corriger le notebook Data_Analyst_Agent.ipynb"""
import json

notebook_path = "notebooks/Data_Analyst_Agent.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

modified = False

# Find cell with 'ÉTAPE 5: RAPPORT' and update it
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'ÉTAPE 5: RAPPORT' in src:
            new_code = """# ============================================
# ÉTAPE 5: RAPPORT
# ============================================

from pathlib import Path

print("=" * 60)
print("ÉTAPE 5: Génération du rapport")
print("=" * 60)

# Racine du projet (car notebook dans /notebooks)
PROJECT_ROOT = Path.cwd().parent

report_path = generate_report(
    analysis_summary=analysis_summary,
    figures_dir=Path.cwd() / OUTPUT_DIR / "figures",  # figures dans notebooks/outputs
    llm_config=llm_config
)

print(f"\\n✅ Rapport généré: {report_path}")

# Chemin absolu (robuste)
report_path = PROJECT_ROOT / report_path

print(f"\\nChemin du rapport:")
print(report_path)

print(f"\\nDossier figures:")
print(Path.cwd() / OUTPUT_DIR / "figures")
"""
            cell['source'] = new_code.splitlines(keepends=True)
            cell['outputs'] = []
            cell['execution_count'] = None
            print("Cellule 20 (Rapport) mise à jour")
            modified = True
        elif 'QUESTIONS/RÉPONSES (QA)' in src:
            # Update QA cell with interactive widgets
            new_qa_code = """# ============================================
# QUESTIONS/RÉPONSES (QA)
# ============================================

from pathlib import Path
import ipywidgets as widgets
from IPython.display import display

print("=" * 60)
print("QUESTIONS/RÉPONSES (QA)")
print("=" * 60)

# Trouver le répertoire racine du projet
current_dir = Path.cwd()
project_root = current_dir.parent if (current_dir / 'notebooks').exists() else current_dir
sys.path.insert(0, str(project_root))

from src.qa import DataQA

# Créer le système QA
qa = DataQA(df_clean, config)
print(f"Mode QA: {'LLM' if qa.llm_enabled else 'rule-based'}")

# Zone de texte pour la question
question_input = widgets.Text(
    value='',
    placeholder='Posez votre question ici...',
    description='Question:',
    layout=widgets.Layout(width='90%'),
    style={'description_width': 'initial'}
)

# Bouton pour envoyer
submit_btn = widgets.Button(
    description='Envoyer',
    button_style='primary'
)

# Bouton pour quitter
quit_btn = widgets.Button(
    description='Quitter',
    button_style='danger'
)

# Zone de sortie pour les réponses
output = widgets.Output()

# Affichage de l'interface
display(question_input, submit_btn, quit_btn, output)

def on_submit(button):
    question = question_input.value.strip()
    if not question:
        return

    with output:
        output.clear_output()
        answer = qa.answer(question, return_tool_results=True)
        print(f"\\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        print(f"\\nRéponse:\\n{answer['response']}")
        print(f"\\nMode utilisé: {answer['mode']}")

        if 'tool_results' in answer and answer['tool_results']:
            print(f"\\nOutils utilisés:")
            for tool_name, result, success in answer['tool_results']:
                status = "SUCCESS" if success else f"ERROR: {result.get('error', 'unknown')}"
                print(f"  - {tool_name}: {status}")

def on_quit(button):
    with output:
        output.clear_output()
        print("\\n" + "="*60)
        print("Au revoir!")
        print("="*60)
    question_input.disabled = True
    submit_btn.disabled = True
    quit_btn.disabled = True

submit_btn.on_click(on_submit)
quit_btn.on_click(on_quit)

print("\\nEntrez votre question ci-dessus et cliquez sur 'Envoyer'.")
"""
            cell['source'] = new_qa_code.splitlines(keepends=True)
            cell['outputs'] = []
            cell['execution_count'] = None
            print("Cellule 22 (QA) mise à jour")
            modified = True

if modified:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Fichier sauvegardé")
else:
    print("Aucune modification effectuée")
