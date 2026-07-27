import random
from flask import Flask, render_template_string, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

# Config Supabase
SUPABASE_URL = "https://invjsfghohqxsvtthnkp.supabase.co"
SUPABASE_KEY = "sb_publishable_8E3SXSuiyAcjwErBkxeRIw_HnddoigJ"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Design HTML "Eyes Wide Shut"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boîte à Secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Montserrat', sans-serif; 
            text-align: center; 
            background: #0d0d0d; 
            color: #e0e0e0; 
            margin: 0; 
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-image: radial-gradient(circle at center, #1a1625 0%, #08070c 100%);
        }
        .card { 
            background: rgba(20, 20, 25, 0.85); 
            max-width: 480px; 
            width: 90%;
            padding: 40px 30px; 
            border-radius: 16px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212, 175, 55, 0.15); 
            border: 1px solid rgba(212, 175, 55, 0.3);
            backdrop-filter: blur(10px);
        }
        h1 { 
            font-family: 'Cinzel', serif; 
            color: #d4af37; 
            font-size: 28px;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 25px;
            text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
        }
        textarea { 
            width: 90%; 
            padding: 12px; 
            background: rgba(10, 10, 12, 0.7);
            border: 1px solid #444; 
            border-radius: 8px; 
            color: #fff;
            font-family: 'Montserrat', sans-serif;
            margin-bottom: 20px; 
            resize: none;
            outline: none;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        textarea:focus {
            border-color: #d4af37;
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
        }
        button { 
            background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%); 
            color: #0d0d0d; 
            border: none; 
            padding: 14px 24px; 
            font-size: 14px; 
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-radius: 30px; 
            cursor: pointer; 
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        button:hover { 
            background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
        }
        .tirage-btn { 
            background: transparent; 
            color: #d4af37;
            border: 1px solid #d4af37;
            margin-top: 20px; 
        }
        .tirage-btn:hover { 
            background: rgba(212, 175, 55, 0.1); 
            color: #f3e5ab;
        }
        .resultat { 
            font-family: 'Cinzel', serif;
            font-size: 18px; 
            color: #f3e5ab; 
            margin-top: 25px; 
            padding: 20px; 
            background: rgba(212, 175, 55, 0.08); 
            border: 1px dashed rgba(212, 175, 55, 0.4);
            border-radius: 12px; 
            line-height: 1.6;
        }
        .message {
            color: #888;
            font-style: italic;
            font-size: 13px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🎭 Fidelio 🎭</h1>
        
        <form action="/ajouter" method="POST">
            <textarea name="idee" rows="3" placeholder="Murmurez votre secret ici..." required></textarea><br>
            <button type="submit">Sceller le secret</button>
        </form>

        <form action="/tirer" method="POST">
            <button type="submit" class="tirage-btn">🔮 Révéler un secret</button>
        </form>

        {% if idee_tiree %}
            <div class="resultat">
                📜 Secret révélé :<br><br>
                <em>« {{ idee_tiree }} »</em>
                <br><br><small style="font-size:11px; color:#888; font-family:'Montserrat';">(Ce secret s'est dissipé à jamais...)</small>
            </div>
        {% endif %}

        {% if message %}
            <p class="message">{{ message }}</p>
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
    return render_template_string(HTML_TEMPLATE, message="Votre secret a été scellé dans l'ombre.")

@app.route('/tirer', methods=['POST'])
def tirer():
    res = supabase.table('idees').select("*").execute()
    idees = res.data
    
    if not idees:
        return render_template_string(HTML_TEMPLATE, message="La boîte est vide. Aucun secret n'attend dans l'ombre.")
    
    # Tirage au sort
    choix = random.choice(idees)
    
    # Supprimer l'idée tirée de Supabase
    supabase.table('idees').delete().eq('id', choix['id']).execute()
    
    return render_template_string(HTML_TEMPLATE, idee_tiree=choix['texte'])

@app.route('/admin')
def admin():
    res = supabase.table('idees').select("*").execute()
    idees = res.data
    return f"<body style='background:#0d0d0d; color:#d4af37; font-family:sans-serif; padding:20px;'><h1>Secrets en attente ({len(idees)})</h1><ul>" + "".join([f"<li>{i['texte']}</li>" for i in idees]) + "</ul><br><a href='/' style='color:#fff;'>Retour</a></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
