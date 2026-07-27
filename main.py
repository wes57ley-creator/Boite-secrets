import os
import random
from flask import Flask, render_template_string, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

# Config Supabase via les variables d'environnement
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://invjsfghohqxsvtthnkp.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- DESIGN PAGE INVITÉ (La Boîte à Secrets) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Boîte à Secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Montserrat:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Montserrat', sans-serif; 
            text-align: center; 
            background: #0a0507; 
            color: #e0e0e0; 
            margin: 0; 
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-image: radial-gradient(circle at center, #2b080e 0%, #0a0507 100%);
        }
        .card { 
            background: rgba(20, 10, 12, 0.9); 
            max-width: 500px; 
            width: 90%;
            padding: 40px 30px; 
            border-radius: 16px; 
            box-shadow: 0 10px 35px rgba(0,0,0,0.9), 0 0 20px rgba(178, 34, 34, 0.25); 
            border: 1px solid rgba(212, 175, 55, 0.4);
            backdrop-filter: blur(10px);
        }
        h1 { 
            font-family: 'Cinzel', serif; 
            color: #d4af37; 
            font-size: 30px;
            letter-spacing: 2px;
            margin-bottom: 5px;
            text-shadow: 0 2px 10px rgba(178, 34, 34, 0.5);
        }
        .counter-badge {
            font-size: 14px;
            color: #ff9999;
            background: rgba(139, 0, 0, 0.3);
            border: 1px solid rgba(178, 34, 34, 0.5);
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 25px;
            font-style: italic;
        }
        textarea { 
            width: 90%; 
            padding: 14px; 
            background: rgba(15, 5, 7, 0.8);
            border: 1px solid #5a1e24; 
            border-radius: 8px; 
            color: #fff;
            font-family: 'Montserrat', sans-serif;
            font-size: 15px;
            margin-bottom: 20px; 
            resize: none;
            outline: none;
            transition: all 0.3s;
        }
        textarea:focus {
            border-color: #d4af37;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.4);
        }
        .btn-submit { 
            background: linear-gradient(135deg, #b22222 0%, #700000 100%); 
            color: #fff; 
            border: 1px solid #d4af37; 
            padding: 14px 28px; 
            font-size: 14px; 
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-radius: 30px; 
            cursor: pointer; 
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .btn-submit:hover { 
            background: linear-gradient(135deg, #d32f2f 0%, #900000 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(178, 34, 34, 0.6);
        }
        .tirage-btn { 
            background: transparent; 
            color: #d4af37;
            border: 1px solid #d4af37;
            margin-top: 20px; 
            padding: 14px 28px; 
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-radius: 30px; 
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .tirage-btn:hover { 
            background: rgba(212, 175, 55, 0.15); 
            color: #fff;
            transform: translateY(-2px);
        }
        .resultat { 
            font-family: 'Cinzel', serif;
            font-size: 19px; 
            color: #ffe6e6; 
            margin-top: 25px; 
            padding: 22px; 
            background: rgba(139, 0, 0, 0.25); 
            border: 1px dashed #d4af37;
            border-radius: 12px; 
            line-height: 1.6;
        }
        .message {
            color: #d4af37;
            font-style: italic;
            font-size: 14px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌹 La Boîte à Secrets 🌹</h1>
        <div class="counter-badge">🔒 {{ nb_secrets }} secret{% if nb_secrets > 1 %}s{% endif %} scellé{% if nb_secrets > 1 %}s{% endif %} actuellement</div>
        
        <form action="/ajouter" method="POST">
            <textarea name="idee" rows="3" placeholder="Murmurez votre secret ici..." required></textarea><br>
            <button type="submit" class="btn-submit">Sceller le secret</button>
        </form>

        <form action="/tirer" method="POST">
            <button type="submit" class="tirage-btn">🔮 Révéler un secret</button>
        </form>

        {% if idee_tiree %}
            <div class="resultat">
                📜 Secret révélé :<br><br>
                <em>« {{ idee_tiree }} »</em>
                <br><br><small style="font-size:12px; color:#aaa; font-family:'Montserrat';">(Ce secret s'est dissipé à jamais...)</small>
            </div>
        {% endif %}

        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

# --- DESIGN PAGE ADMIN (Chaleureux & Grande Police) ---
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administration - La Boîte à Secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Montserrat', sans-serif; 
            background: #0a0507; 
            color: #f5f5f5; 
            margin: 0; 
            padding: 30px 15px;
            background-image: radial-gradient(circle at center, #2b080e 0%, #0a0507 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 700px; 
            margin: 0 auto; 
            background: rgba(20, 10, 12, 0.95); 
            padding: 35px; 
            border-radius: 16px; 
            border: 1px solid #d4af37;
            box-shadow: 0 10px 40px rgba(0,0,0,0.9), 0 0 25px rgba(178, 34, 34, 0.3);
        }
        h1 { 
            font-family: 'Cinzel', serif; 
            color: #d4af37; 
            font-size: 32px; 
            text-align: center;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #ff9999;
            margin-bottom: 30px;
        }
        .secret-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .secret-card {
            background: rgba(40, 15, 20, 0.7);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 18px 22px;
            margin-bottom: 15px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }
        .secret-text {
            font-size: 20px; /* Grande police bien lisible */
            line-height: 1.5;
            color: #ffffff;
            word-break: break-word;
        }
        .btn-delete {
            background: #8b0000;
            color: #ffffff;
            border: 1px solid #ff4d4d;
            padding: 10px 16px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }
        .btn-delete:hover {
            background: #ff0000;
            transform: scale(1.05);
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 30px;
            color: #d4af37;
            font-size: 18px;
            text-decoration: none;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌹 Sanctuaire Admin 🌹</h1>
        <p class="subtitle">Secrets actuellement conservés dans l'ombre : <strong>{{ idees|length }}</strong></p>
        
        {% if idees %}
            <ul class="secret-list">
                {% for item in idees %}
                    <li class="secret-card">
                        <span class="secret-text">« {{ item.texte }} »</span>
                        <a href="/admin/supprimer/{{ item.id }}" onclick="return confirm('Confirmer la suppression de ce secret ?');">
                            <button class="btn-delete">🗑️ Supprimer</button>
                        </a>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p style="text-align:center; font-size:20px; color:#aaa; margin:40px 0;"><em>Aucun secret enregistré pour le moment.</em></p>
        {% endif %}

        <a href="/" class="back-link">← Retour au rituel principal</a>
    </div>
</body>
</html>
"""

# --- ROUTES DE L'APPLICATION ---

@app.route('/')
def home():
    # Récupérer le nombre de secrets pour le compteur
    res = supabase.table('idees').select("*").execute()
    nb_secrets = len(res.data) if res.data else 0
    return render_template_string(HTML_TEMPLATE, nb_secrets=nb_secrets)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    nouvelle_idee = request.form.get('idee')
    if nouvelle_idee:
        supabase.table('idees').insert({"texte": nouvelle_idee}).execute()
    
    res = supabase.table('idees').select("*").execute()
    nb_secrets = len(res.data) if res.data else 0
    return render_template_string(HTML_TEMPLATE, message="Votre secret a été scellé dans l'ombre.", nb_secrets=nb_secrets)

@app.route('/tirer', methods=['POST'])
def tirer():
    res = supabase.table('idees').select("*").execute()
    idees = res.data if res.data else []
    
    if not idees:
        return render_template_string(HTML_TEMPLATE, message="La boîte est vide. Aucun secret n'attend dans l'ombre.", nb_secrets=0)
    
    # Tirage au sort
    choix = random.choice(idees)
    
    # Supprimer l'idée tirée de Supabase
    supabase.table('idees').delete().eq('id', choix['id']).execute()
    
    # Compteur mis à jour après suppression
    res_apres = supabase.table('idees').select("*").execute()
    nb_secrets = len(res_apres.data) if res_apres.data else 0
    
    return render_template_string(HTML_TEMPLATE, idee_tiree=choix['texte'], nb_secrets=nb_secrets)

@app.route('/admin')
def admin():
    try:
        res = supabase.table('idees').select("*").execute()
        idees = res.data if res.data else []
        return render_template_string(ADMIN_TEMPLATE, idees=idees)
    except Exception as e:
        return f"<body style='background:#0a0507; color:#ff4d4d; font-family:sans-serif; padding:40px;'><h2>Erreur d'accès :</h2><p>{str(e)}</p></body>"

@app.route('/admin/supprimer/<int:secret_id>')
def supprimer_admin(secret_id):
    try:
        supabase.table('idees').delete().eq('id', secret_id).execute()
    except Exception as e:
        pass
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
