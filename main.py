import os
from flask import Flask, request, redirect, url_for, render_template_string
from supabase import create_client, Client

app = Flask(__name__)

# Configuration Supabase via variables d'environnement
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- DESIGN HTML ENCAPSULÉ ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boîte-secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Montserrat:wght@300;400;600&family=Pinyon+Script&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: radial-gradient(circle at center, #1c1a1a 0%, #0d0d0d 100%);
            color: #e0d0b0;
            font-family: 'Montserrat', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .header { text-align: center; margin-bottom: 25px; }
        h1 {
            font-family: 'Pinyon Script', cursive;
            color: #d4af37;
            font-size: 3.8em;
            text-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
            line-height: 1.1;
        }
        .subtitle {
            font-family: 'Cinzel', serif;
            color: #a09080;
            font-size: 0.85em;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 5px;
        }
        .card {
            width: 100%;
            max-width: 420px;
            background: rgba(18, 18, 18, 0.85);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 16px;
            padding: 30px 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
        }
        .form-title {
            color: #8b0000;
            font-family: 'Cinzel', serif;
            font-size: 0.9em;
            letter-spacing: 1px;
            margin-bottom: 12px;
            display: block;
            text-transform: uppercase;
        }
        textarea {
            width: 100%;
            height: 110px;
            background: #141414;
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 10px;
            color: #f0f0f0;
            padding: 15px;
            font-family: 'Montserrat', sans-serif;
            font-style: italic;
            font-size: 0.95em;
            resize: none;
            margin-bottom: 20px;
        }
        textarea:focus {
            outline: none;
            border-color: #d4af37;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);
        }
        .buttons-group { display: flex; gap: 12px; margin-bottom: 25px; }
        .btn {
            border: none;
            border-radius: 8px;
            padding: 14px 10px;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            font-size: 0.85em;
            letter-spacing: 1px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-submit {
            flex: 1.8;
            background: linear-gradient(135deg, #7a0000 0%, #a81c1c 100%);
            color: #f3e5ab;
            border: 1px solid rgba(212, 175, 55, 0.3);
            box-shadow: 0 4px 15px rgba(122, 0, 0, 0.5);
        }
        .btn-reveal {
            flex: 1.2;
            background: linear-gradient(135deg, #c5a059 0%, #9e7d3b 100%);
            color: #0d0d0d;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.3);
        }
        .counter-box {
            text-align: center;
            border-top: 1px solid rgba(212, 175, 55, 0.15);
            padding-top: 20px;
        }
        .counter-number {
            font-family: 'Pinyon Script', cursive;
            color: #d4af37;
            font-size: 2.5em;
            line-height: 1;
        }
        .counter-label {
            font-family: 'Cinzel', serif;
            color: #8a7a6a;
            font-size: 0.75em;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }
        .secret-item {
            background: rgba(255, 255, 255, 0.03);
            border-left: 2px solid #d4af37;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Boîte-secrets</h1>
        <div class="subtitle">Le Sanctuaire de vos Désirs</div>
    </div>

    <div class="card">
        {% if view == 'home' %}
            <form action="/add" method="POST">
                <label class="form-title">Enfermez votre secret...</label>
                <textarea name="content" placeholder="Un désir, une confidence, un interdit..." required></textarea>
                
                <div class="buttons-group">
                    <button type="submit" class="btn btn-submit">Sceller 🔑</button>
                    <a href="/secrets" class="btn btn-reveal">Révéler</a>
                </div>
            </form>

            <div class="counter-box">
                <div class="counter-number">{{ total_secrets }}</div>
                <div class="counter-label">Secrets Scellés</div>
            </div>
        {% elif view == 'secrets' %}
            <label class="form-title" style="margin-bottom: 20px; display:block; text-align:center;">Confidences Révelées</label>
            
            {% for s in secrets %}
                <div class="secret-item">"{{ s.content }}"</div>
            {% else %}
                <p style="text-align:center; color:#8a7a6a; font-style:italic;">Aucun secret n'a encore été scellé...</p>
            {% endfor %}

            <div style="margin-top: 25px;">
                <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    total_secrets = 0
    if supabase:
        try:
            res = supabase.table('secrets').select('id', count='exact').execute()
            total_secrets = res.count if res.count is not None else len(res.data)
        except Exception as e:
            print("Erreur Supabase:", e)
    return render_template_string(HTML_TEMPLATE, view='home', total_secrets=total_secrets)

@app.route('/secrets')
def secrets():
    secrets_list = []
    if supabase:
        try:
            res = supabase.table('secrets').select('*').order('created_at', desc=True).limit(20).execute()
            secrets_list = res.data
        except Exception as e:
            print("Erreur Supabase:", e)
    return render_template_string(HTML_TEMPLATE, view='secrets', secrets=secrets_list)

@app.route('/add', methods=['POST'])
def add_secret():
    content = request.form.get('content')
    if content and supabase:
        try:
            supabase.table('secrets').insert({'content': content}).execute()
        except Exception as e:
            print("Erreur enregistrement:", e)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
