import random
from flask import Flask, render_template_string, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

# Config Supabase
SUPABASE_URL = "https://invjsfghohqxsvtthnkp.supabase.co"
SUPABASE_KEY = "sb_publishable_8E3SXSuiyAcjwErBk..." # Remplace par ta clé complète Publishable key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Design HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boîte à Secrets</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #f0f2f5; margin: 0; padding: 20px; }
        .card { background: white; max-width: 500px; margin: 20px auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        textarea, input[type="text"] { width: 90%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 15px; }
        button { background: #007bff; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .tirage-btn { background: #28a745; margin-top: 15px; }
        .tirage-btn:hover { background: #218838; }
        .resultat { font-size: 20px; font-weight: bold; color: #dc3545; margin-top: 20px; padding: 15px; background: #ffe6e6; border-radius: 8px; }
        .list-item { text-align: left; background: #f8f9fa; padding: 10px; border-bottom: 1px solid #ddd; margin-bottom: 5px; border-radius: 4px; display: flex; justify-content: space-between; }
    </style>
</head>
<body>
    <div class="card">
        <h1>✨ Boîte à Secrets ✨</h1>
        
        <form action="/ajouter" method="POST">
            <textarea name="idee" rows="3" placeholder="Tape ton idée ou ton secret ici..." required></textarea><br>
            <button type="submit">Ajouter l'idée</button>
        </form>

        <form action="/tirer" method="POST">
            <button type="submit" class="tirage-btn">🎲 Tirer au sort une idée</button>
        </form>

        {% if idee_tiree %}
            <div class="resultat">
                🎉 Idée tirée au sort :<br><br>
                "{{ idee_tiree }}"
                <br><small style="font-size:12px; color:#666;">(Cette idée a été tirée et supprimée de la boîte !)</small>
            </div>
        {% endif %}

        {% if message %}
            <p style="color: green;">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    nouvelle_idee = request.form.get('idee')
    if nouvelle_idee:
        supabase.table('idees').insert({"texte": nouvelle_idee}).execute()
    return render_template_string(HTML_TEMPLATE, message="Idée ajoutée avec succès !")

@app.route('/tirer', methods=['POST'])
def tirer():
    res = supabase.table('idees').select("*").execute()
    idees = res.data
    
    if not idees:
        return render_template_string(HTML_TEMPLATE, message="La boîte est vide ! Ajoutez des idées.")
    
    # Tirage au sort
    choix = random.choice(idees)
    
    # Option A : Supprimer l'idée tirée de la base de données
    supabase.table('idees').delete().eq('id', choix['id']).execute()
    
    return render_template_string(HTML_TEMPLATE, idee_tiree=choix['texte'])

@app.route('/admin')
def admin():
    res = supabase.table('idees').select("*").execute()
    idees = res.data
    return f"<h1>Administration</h1><p>Nombre d'idées en attente : {len(idees)}</p><ul>" + "".join([f"<li>{i['texte']}</li>" for i in idees]) + "</ul><br><a href='/'>Retour</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
