from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from src.git_parser import get_pr_diff
from src.ai_reviewer import review_code

# On initialise le serveur web Flask
app = Flask(__name__)

# --- 1. CONFIGURATION DE LA BASE DE DONNÉES ET SÉCURITÉ ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/code_reviewer_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clé secrète obligatoire pour les sessions et les redirections sécurisées
app.secret_key = "robin_nathan_projet_iag_2026" 

# On initialise l'outil de base de données (SQLAlchemy)
db = SQLAlchemy(app)

# --- 2. CRÉATION DES TABLES (MODÈLES) ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', backref='author', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(100), nullable=False)
    pr_number = db.Column(db.Integer, nullable=False)
    ai_result = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

# --- 3. NOS ROUTES ---

@app.route('/')
def home():
    # SÉCURITÉ : Si l'utilisateur n'est pas connecté, on le renvoie vers la page de login
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # MODIFIÉ : On transmet le nom d'utilisateur au template pour la barre de navigation
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Ce nom d'utilisateur existe déjà ! Essayez-en un autre."

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # On cherche l'utilisateur dans la base
        user = User.query.filter_by(username=username).first()

        # On vérifie si le compte existe ET si le mot de passe est bon
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"✅ Connexion réussie pour {username}")
            return redirect(url_for('home')) # On l'envoie vers l'application
        else:
            return "Identifiants incorrects. Veuillez réessayer."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # On supprime le badge de connexion
    return redirect(url_for('login'))

# NOUVEAU : LA PAGE D'HISTORIQUE
@app.route('/historique')
def historique():
    # 1. Sécurité : On vérifie que l'utilisateur est bien connecté
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. On récupère TOUTES les revues de cet utilisateur, triées par date (la plus récente en premier)
    user_reviews = Review.query.filter_by(user_id=session['user_id']).order_by(Review.date_created.desc()).all()
    
    # 3. On envoie ces données à la page HTML
    return render_template('historique.html', reviews=user_reviews, username=session.get('username'))

@app.route('/api/analyze', methods=['POST'])
def analyze_pr():
    # SÉCURITÉ : Bloque les requêtes si on n'est pas connecté
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401

    data = request.json
    repo_owner = data.get('owner')
    repo_name = data.get('repo')
    pr_number = data.get('pr')
    level = data.get('level', 'senior') 
    
    try:
        diff_text = get_pr_diff(repo_owner, repo_name, pr_number)
        review_result = review_code(diff_text, level)
        
        # ON SAUVEGARDE L'ANALYSE DANS LA BASE DE DONNÉES !
        new_review = Review(
            repo_name=f"{repo_owner}/{repo_name}",
            pr_number=pr_number,
            ai_result=review_result,
            user_id=session['user_id']
        )
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "result": review_result
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 400

if __name__ == '__main__':
    print("🚀 Serveur en cours de démarrage sur http://127.0.0.1:5000")
    app.run(debug=True, port=5000)