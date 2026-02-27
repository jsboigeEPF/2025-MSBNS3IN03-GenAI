"""
Interface locale Flask pour Data Analyst Agent.

Cette application Web permet de :
- Charger un fichier CSV/Excel
- Exécuter l'analyse complète
- Poser des questions via une interface chat
- Voir les visualisations générées
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import pandas as pd
import yaml
import json
import logging
import os
import uuid

# Import des modules du projet
from src.pipeline import run_pipeline
from src.qa import DataQA
from src.config_env import load_dotenv_config, get_openai_key, is_llm_enabled as llm_enabled

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUTS_FOLDER = Path('outputs')
SESSIONS = {}  # stocke les sessions: {session_id: {'df': df, 'qa': DataQA, ...}}
CONFIG_PATH = 'config.yaml'

# Créer les dossiers nécessaires
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUTS_FOLDER.mkdir(parents=True, exist_ok=True)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """Charge la configuration YAML."""
    config_path = Path(CONFIG_PATH)
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {
        "data": {"output_dir": "outputs"},
        "llm": {"enabled": False},
        "cleaning": {"handle_duplicates": True, "handle_outliers": True},
        "visualization": {"style": "default"}
    }


def get_llm_config():
    """Vérifie et retourne la configuration LLM."""
    config = load_config()
    llm_config = config.get("llm", {})

    if llm_config.get("enabled", False):
        try:
            load_dotenv_config()
            get_openai_key()
            logger.info("LLM activé avec clé API")
            return llm_config
        except ValueError as e:
            logger.warning(f"LLM désactivé: {e}")
            llm_config["enabled"] = False

    return llm_config


@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload et analyse un fichier."""
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Fichier vide'}), 400

    try:
        # Générer un ID de session unique
        session_id = str(uuid.uuid4())[:8]

        # Sauvegarder le fichier uploadé
        upload_path = UPLOAD_FOLDER / f"{session_id}_{file.filename}"
        file.save(upload_path)

        # Charger la config
        config = load_config()
        llm_config = get_llm_config()
        config['llm'] = llm_config

        # Exécuter la pipeline
        output_dir = OUTPUTS_FOLDER / session_id
        output_dir.mkdir(parents=True, exist_ok=True)

        results = run_pipeline(
            data_path=str(upload_path),
            config_path=CONFIG_PATH,
            outdir=str(output_dir)
        )

        # Charger les données nettoyées pour QA
        cleaned_path = output_dir / "cleaned.csv"
        df_clean = pd.read_csv(cleaned_path)

        # Initialiser le système QA
        qa = DataQA(df_clean, config)

        # Stocker la session
        SESSIONS[session_id] = {
            'df': df_clean,
            'qa': qa,
            'config': config,
            'results': results,
            'output_dir': output_dir
        }

        # Résumé pour l'utilisateur
        figures_count = sum(len(v) for v in results.get('figures', {}).values())
        insights_count = len(results.get('insights', []))

        return jsonify({
            'success': True,
            'session_id': session_id,
            'summary': {
                'rows': len(df_clean),
                'columns': len(df_clean.columns),
                'figures': figures_count,
                'insights': insights_count,
                'output_dir': output_dir.relative_to(Path.cwd()).as_posix()  # Forcer les slashes Unix
            }
        })

    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/qa/ask', methods=['POST'])
def ask_question():
    """Pose une question via l'interface QA."""
    data = request.get_json()
    session_id = data.get('session_id')
    question = data.get('question')

    if not session_id or session_id not in SESSIONS:
        return jsonify({'error': 'Session non trouvée'}), 404

    if not question:
        return jsonify({'error': 'Question vide'}), 400

    try:
        session = SESSIONS[session_id]
        qa = session['qa']

        # Poser la question
        response = qa.answer(question, return_tool_results=True)

        # Si c'est un dict, extraire la réponse
        if isinstance(response, dict):
            answer = response.get('response', str(response))
            mode = response.get('mode', 'unknown')
            tool_results = response.get('tool_results', [])
        else:
            answer = str(response)
            mode = 'unknown'
            tool_results = []

        return jsonify({
            'success': True,
            'answer': answer,
            'mode': mode,
            'tool_results': tool_results
        })

    except Exception as e:
        logger.error(f"Erreur lors de la question: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/qa/interactive')
def qa_interface():
    """Interface interactive pour poser des questions."""
    session_id = request.args.get('session_id')
    if not session_id or session_id not in SESSIONS:
        return render_template('error.html', error='Session non trouvée')

    return render_template('qa_interface.html', session_id=session_id)


@app.route('/get_visualizations/<session_id>')
def get_visualizations(session_id):
    """Renvoie la liste des visualisations."""
    if session_id not in SESSIONS:
        return jsonify({'error': 'Session non trouvée'}), 404

    session = SESSIONS[session_id]
    output_dir = session['output_dir']
    figures_dir = output_dir / 'figures'

    if not figures_dir.exists():
        return jsonify({'figures': []})

    figures = []
    for ext in ['*.png', '*.jpg', '*.jpeg']:
        figures.extend([str(p.relative_to(output_dir).as_posix()) for p in figures_dir.glob(ext)])

    return jsonify({'figures': figures})


@app.route('/outputs/<path:session_id>/<filename>')
def serve_output(session_id, filename):
    """Sert un fichier de sortie."""
    # Construire le chemin absolu complet pour éviter les problèmes de validation sur Windows
    base_path = Path.cwd()
    output_dir = base_path / OUTPUTS_FOLDER / session_id
    # Convertir en string pour send_from_directory
    output_dir_str = str(output_dir)
    # Formatter le chemin pour forcer les slashes (Windows compatibility)
    output_dir_str = output_dir_str.replace('\\', '/')
    return send_from_directory(output_dir_str, filename)


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Sert un fichier statique."""
    return send_from_directory('static', filename)


@app.route('/check_llm')
def check_llm():
    """Vérifie si LLM est disponible."""
    config = load_config()
    llm_config = get_llm_config()
    return jsonify({
        'enabled': llm_config.get('enabled', False),
        'llm_config': config.get('llm', {})
    })


@app.route('/sessions')
def list_sessions():
    """Liste les sessions disponibles."""
    sessions_list = []
    for sid, session in SESSIONS.items():
        sessions_list.append({
            'id': sid,
            'rows': len(session['df']),
            'columns': len(session['df'].columns),
            'figures': sum(len(v) for v in session['results'].get('figures', {}).values())
        })
    return jsonify({'sessions': sessions_list})


if __name__ == '__main__':
    logger.info("Démarrage de l'interface locale...")
    logger.info(f"LLM activé: {get_llm_config().get('enabled', False)}")
    app.run(debug=True, host='0.0.0.0', port=5000)
