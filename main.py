import os
from flask import Flask, request, redirect, url_for, render_template_string
from supabase import create_client, Client

app = Flask(__name__)

# Configuration Supabase via variables d'environnement
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Erreur initialisation Supabase:", e)

# --- DESIGN HTML AVEC ARRIÈRE-PLAN TEXTURÉ ET SANS MASQUE SVG ---
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
            /* Arrière-plan sombre élégant à texture profonde */
            background: 
                radial-gradient(circle at center, rgba(28, 26, 26, 0.75) 0%, rgba(10, 10, 10, 0.95) 100%),
                url('https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop') center/cover no-repeat fixed;
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
            font-size: 4em;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.4), 0 2px 4px rgba(0, 0, 0, 0.8);
            line-height: 1.1;
        }
        
        .subtitle {
            font-family: 'Cinzel', serif;
            color: #b0a090;
            font-size: 0.85em;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 5px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
        }
        
        .card {
            width: 100%;
            max-width: 420px;
            background: rgba(14, 14, 14, 0.88);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            padding: 30px 25px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.95), inset 0 0 20px rgba(212, 175, 55, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        
        .form-title {
            color: #9e1b1b;
            font-family: 'Cinzel', serif;
            font-size: 0.9em;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            display: block;
            text-transform: uppercase;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
        }
        
        textarea {
            width: 100%;
            height: 110px;
            background: rgba(10, 10, 10, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 10px;
            color: #f0f0f0;
            padding: 15px;
            font-family: 'Montserrat', sans-serif;
            font-style: italic;
            font-size: 0.95em;
            resize: none;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        textarea:focus {
            outline: none;
            border-color: #d4af37;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.35);
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
            transition: all 0.2s ease;
        }
        
        .btn:hover { transform: translateY(-2px); }
        
        .btn-submit {
            flex: 1.8;
            background: linear-gradient(135deg, #7a0000 0%, #a81c1c 100%);
            color: #f3e5ab;
            border: 1px solid rgba(212, 175, 55, 0.3);
            box-shadow: 0 4px 15px rgba(122, 0, 0, 0.6);
        }
        
        .btn-reveal {
            flex: 1.2;
            background: linear-gradient(135deg, #c5a059 0%, #9e7d3b 100%);
            color: #0d0d0d;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.35);
        }
        
        .counter-box {
            text-align: center;
            border-top: 1px solid rgba(212, 175, 55, 0.15);
            padding-top: 20px;
        }
        
        .counter-number {
            font-family: 'Pinyon Script', cursive;
            color: #d4af37;
            font-size: 2.8em;
            line-height: 1;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
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
            word-break: break-word;
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
            <label class="form-title" style="margin-bottom: 20px; display:block; text-align:center;">Confidences Révélées</label>
            
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
            res = supabase.table('idees').select('id', count='exact').execute()
            total_secrets = res.count if res.count is not None else len(res.data)
        except Exception as e:
            print("Erreur Supabase:", e)
    return render_template_string(HTML_TEMPLATE, view='home', total_secrets=total_secrets)

@app.route('/secrets')
def secrets():
    secrets_list = []
    if supabase:
        try:
            res = supabase.table('idees').select('*').order('created_at', desc=True).limit(20).execute()
            secrets_list = res.data
        except Exception as e:
            print("Erreur Supabase:", e)
    return render_template_string(HTML_TEMPLATE, view='secrets', secrets=secrets_list)

@app.route('/add', methods=['POST'])
def add_secret():
    content = request.form.get('content')
    if content and supabase:
        try:
            supabase.table('idees').insert({'content': content}).execute()
        except Exception as e:
            print("Erreur enregistrement:", e)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
