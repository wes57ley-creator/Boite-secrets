from flask import Flask, request, render_template_string
import random
import json
import os
import socket

app = Flask(__name__)
FICHIER_SAUVEGARDE = 'idees_vacances.json'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Boîte à Secrets 🎭</title>
    <style>
        body { 
            font-family: 'Georgia', serif; 
            text-align: center; 
            background-color: #111115;
            color: #e0e0e0;
            padding: 20px;
            margin: 0;
        }
        .container { 
            max-width: 400px; 
            margin: 40px auto; 
            background-color: #1c1c24; 
            padding: 30px 20px; 
            border-radius: 8px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            border: 1px solid #2a2a35;
        }
        h1 { color: #d4af37; font-size: 26px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
        .subtitle { font-size: 12px; color: #75758a; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 30px; }
        .badge { background-color: #8b0000; color: #fff; padding: 2px 6px; border-radius: 3px; font-size: 10px; vertical-align: middle; }
        input[type="text"] { 
            width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #3a3a4a; 
            border-radius: 4px; font-size: 16px; background-color: #0b0b0d; color: #fff; box-sizing: border-box; text-align: center;
        }
        button { 
            background-color: #252530; color: #d4af37; border: 1px solid #d4af37; padding: 12px 20px; 
            border-radius: 4px; cursor: pointer; font-size: 14px; width: 100%; text-transform: uppercase; letter-spacing: 1px; transition: 0.2s;
        }
        button:hover { background-color: #d4af37; color: #111115; }
        button.draw { background: linear-gradient(135deg, #8b0000, #4a0000); color: white; border: none; font-weight: bold; }
        button.draw:hover { background: linear-gradient(135deg, #a30000, #5a0000); }
        button.close-result { background-color: #111115; color: #75758a; border: 1px solid #3a3a4a; font-size: 11px; padding: 6px 12px; width: auto; margin-top: 10px; }
        button.reset { background-color: transparent; color: #ff4d4d; border: 1px solid #ff4d4d; font-size: 11px; width: auto; padding: 6px 12px; }
        button.delete-btn { background-color: transparent; color: #75758a; border: none; padding: 5px; font-size: 14px; width: auto; }
        button.delete-btn:hover { color: #ff4d4d; }
        .result { background-color: rgba(139, 0, 0, 0.15); border: 1px solid #8b0000; padding: 20px; border-radius: 4px; margin: 20px 0; }
        .result-title { font-size: 11px; color: #75758a; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
        ul { list-style-type: none; padding: 0; text-align: left; }
        li { padding: 10px; border-bottom: 1px solid #2a2a35; display: flex; justify-content: space-between; align-items: center; }
        .counter-msg { color: #d4af37; font-size: 13px; text-transform: uppercase; margin-top: 20px; }
        hr { border: 0; border-top: 1px solid #2a2a35; margin: 25px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>La Boîte à Secrets {% if est_admin %}<span class="badge">Maître</span>{% endif %}</h1>
        <div class="subtitle">Destinations de Vacances</div>
        <form method="POST">
            <input type="text" name="nouvelle_idee" placeholder="Votre suggestion anonyme..." required autocomplete="off">
            <button type="submit">Soumettre la suggestion</button>
        </form>
        <hr>
        <form method="POST">
            <button type="submit" name="tirer_au_sort" class="draw">🎭 Tirer au sort</button>
        </form>
        {% if gagnant %}
            <div class="result">
                <div class="result-title">Le choix du destin :</div>
                <span style="color: #d4af37; font-size: 1.4em; font-weight: bold;">✨ {{ gagnant }} ✨</span>
                <br>
                <form method="POST" style="margin: 0;">
                    <button type="submit" name="masquer_gagnant" class="close-result">Effacer le résultat 🤫</button>
                </form>
            </div>
        {% endif %}
        {% if est_admin %}
            <h3 style="color: #d4af37; font-weight: normal; font-size: 15px; margin-top: 25px;">Suggestions dans la boîte ({{ idees|length }}) :</h3>
            <ul>
                {% for idee in idees %}
                    <li>
                        <span>🔑 {{ idee }}</span>
                        <form method="POST" style="margin: 0;">
                            <input type="hidden" name="idee_a_supprimer" value="{{ idee }}">
                            <button type="submit" class="delete-btn">✕</button>
                        </form>
                    </li>
                {% endfor %}
            </ul>
            {% if idees %}
                <form method="POST" style="margin-top: 20px;">
                    <button type="submit" name="reinitialiser" class="reset">Vider toute la boîte</button>
                </form>
            {% endif %}
        {% else %}
            <div class="counter-msg">🔒 Nombre de secrets dans la boîte : {{ idees|length }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

def charger_donnees():
    if os.path.exists(FICHIER_SAUVEGARDE):
        with open(FICHIER_SAUVEGARDE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except json.JSONDecodeError: return {"idees": [], "gagnant": None}
    return {"idees": [], "gagnant": None}

def sauvegarder_donnees(donnees):
    with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)

def gerer_actions_communes(donnees, formulaire):
    if 'nouvelle_idee' in formulaire:
        idee = formulaire.get('nouvelle_idee').strip()
        if idee and idee not in donnees["idees"]:
            donnees["idees"].append(idee)
            sauvegarder_donnees(donnees)
    elif 'tirer_au_sort' in formulaire:
        if donnees["idees"]:
            choix = random.choice(donnees["idees"])
            donnees["gagnant"] = choix
            donnees["idees"].remove(choix)
            sauvegarder_donnees(donnees)
    elif 'masquer_gagnant' in formulaire:
        donnees["gagnant"] = None
        sauvegarder_donnees(donnees)

@app.route('/', methods=['GET', 'POST'])
def index():
    donnees = charger_donnees()
    if request.method == 'POST':
        gerer_actions_communes(donnees, request.form)
    return render_template_string(HTML_TEMPLATE, idees=donnees["idees"], gagnant=donnees["gagnant"], est_admin=False)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    donnees = charger_donnees()
    if request.method == 'POST':
        gerer_actions_communes(donnees, request.form)
        if 'idee_a_supprimer' in request.form:
            idee_cible = request.form.get('idee_a_supprimer')
            if idee_cible in donnees["idees"]:
                donnees["idees"].remove(idee_cible)
                if donnees["gagnant"] == idee_cible:
                    donnees["gagnant"] = None
                sauvegarder_donnees(donnees)
        elif 'reinitialiser' in request.form:
            donnees["idees"] = []
            donnees["gagnant"] = None
            sauvegarder_donnees(donnees)
    return render_template_string(HTML_TEMPLATE, idees=donnees["idees"], gagnant=donnees["gagnant"], est_admin=True)

def obtenir_ip_locale():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    ip_locale = obtenir_ip_locale()
    print(f"🎭 INITIÉS : http://{ip_locale}:5000")
    print(f"👑 MAÎTRE  : http://127.0.0.1:5000/admin")
    app.run(debug=False, host='0.0.0.0', port=5000)
