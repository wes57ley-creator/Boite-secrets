import os
from flask import Flask, request, redirect, url_for, render_template_string, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cle_secrete_boite_secrets_999")

# 🔒 VOTRE MOT DE PASSE ADMIN RESTAURÉ
ADMIN_PASSWORD = "Therec@nbeonly1"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Erreur initialisation Supabase:", e)

# --- DESIGN HAUTE COUTURE / MASQUERADE / RITE D'INITIATION ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boîte-secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Montserrat:ital,wght@0,300;0,400;1,300&family=Pinyon+Script&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: 
                radial-gradient(circle at center, rgba(20, 15, 15, 0.85) 0%, rgba(5, 5, 5, 0.98) 100%),
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
            font-size: 4.2em;
            text-shadow: 0 0 25px rgba(212, 175, 55, 0.5), 0 3px 6px rgba(0, 0, 0, 0.9);
            line-height: 1;
        }
        
        .subtitle {
            font-family: 'Cinzel', serif;
            color: #b0a090;
            font-size: 0.8em;
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-top: 8px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
        }
        
        .card {
            width: 100%;
            max-width: 460px;
            background: rgba(10, 8, 8, 0.94);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 8px;
            padding: 35px 28px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.98), inset 0 0 0 2px rgba(212, 175, 55, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            position: relative;
        }
        
        .form-title {
            color: #a81c1c;
            font-family: 'Cinzel', serif;
            font-size: 0.85em;
            letter-spacing: 2.5px;
            margin-bottom: 15px;
            display: block;
            text-transform: uppercase;
            text-align: center;
            font-weight: 700;
        }
        
        textarea, input[type="password"] {
            width: 100%;
            background: rgba(5, 5, 5, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 4px;
            color: #f0f0f0;
            padding: 16px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.95em;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        textarea { height: 110px; font-style: italic; resize: none; }
        
        textarea:focus, input[type="password"]:focus {
            outline: none;
            border-color: #d4af37;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        }
        
        .buttons-group { display: flex; gap: 12px; margin-bottom: 20px; }
        
        .btn {
            border: none;
            border-radius: 4px;
            padding: 15px 12px;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            font-size: 0.8em;
            letter-spacing: 2px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        
        .btn:hover { transform: translateY(-2px); }
        
        .btn-submit {
            flex: 1.8;
            background: linear-gradient(135deg, #4a0000 0%, #730d0d 100%);
            color: #f3e5ab;
            border: 1px solid rgba(212, 175, 55, 0.4);
            box-shadow: 0 4px 18px rgba(74, 0, 0, 0.7);
        }
        
        .btn-reveal {
            flex: 1.2;
            background: linear-gradient(135deg, #b89343 0%, #8c6a23 100%);
            color: #0d0d0d;
            box-shadow: 0 4px 18px rgba(184, 147, 67, 0.3);
        }
        
        .counter-box {
            text-align: center;
            border-top: 1px solid rgba(212, 175, 55, 0.2);
            padding-top: 20px;
        }
        
        .counter-number {
            font-family: 'Pinyon Script', cursive;
            color: #d4af37;
            font-size: 3em;
            line-height: 1;
        }
        
        .counter-label {
            font-family: 'Cinzel', serif;
            color: #8a7a6a;
            font-size: 0.7em;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        .sanctuary-vault {
            position: relative;
            background: rgba(15, 12, 12, 0.95);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 6px;
            padding: 30px 20px;
            min-height: 140px;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            margin: 15px 0 20px 0;
            overflow: hidden;
            box-shadow: inset 0 0 25px rgba(0,0,0,0.9);
        }

        .vault-lock {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at center, #1c1515 0%, #0a0707 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 10;
            transition: all 0.9s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(212, 175, 55, 0.3);
        }

        .vault-lock:hover {
            border-color: #d4af37;
            box-shadow: inset 0 0 20px rgba(212, 175, 55, 0.2);
        }

        .lock-icon {
            font-size: 2em;
            color: #d4af37;
            margin-bottom: 8px;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
            transition: transform 0.6s ease;
        }

        .vault-lock:hover .lock-icon {
            transform: scale(1.15) rotate(5deg);
        }

        .lock-text {
            font-family: 'Cinzel', serif;
            font-size: 0.8em;
            letter-spacing: 3px;
            color: #c5a059;
            text-transform: uppercase;
        }

        .vault-lock.unlocked {
            opacity: 0;
            transform: translateY(-100%);
            pointer-events: none;
        }

        .secret-text-display {
            font-size: 1.15em;
            line-height: 1.6;
            font-style: italic;
            opacity: 0;
            transform: scale(0.95);
            transition: opacity 1s ease 0.4s, transform 1s ease 0.4s;
            word-break: break-word;
        }

        .secret-text-display.visible {
            opacity: 1;
            transform: scale(1);
        }

        .gold-glow { color: #f3e5ab; text-shadow: 0 0 12px rgba(212, 175, 55, 0.3); }
        .pink-glow { color: #f8bbd0; text-shadow: 0 0 12px rgba(194, 24, 91, 0.4); }

        .warning-text {
            color: #7a6a5a;
            font-size: 0.75em;
            text-align: center;
            margin-top: 15px;
            font-style: italic;
            letter-spacing: 1px;
        }

        .delete-btn { color: #e74c3c; text-decoration: none; font-size: 0.8em; font-style: normal; }
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
                <label class="form-title">Enfermez votre secret</label>
                <textarea name="content" placeholder="Un désir, une confidence, un interdit..." required></textarea>
                
                <div class="buttons-group">
                    <button type="submit" class="btn btn-submit">Sceller 🔑</button>
                    <a href="/reveal_next" class="btn btn-reveal">Révéler</a>
                </div>
            </form>

            <div class="counter-box">
                <div class="counter-number">{{ total_secrets }}</div>
                <div class="counter-label">Secrets Scellés</div>
            </div>

        {% elif view == 'reveal' %}
            <label class="form-title">Secret Révélé</label>
            
            {% if secret and secret.clean_text %}
                <div class="sanctuary-vault">
                    <div class="vault-lock" id="vaultLock" onclick="unlockSecret()">
                        <div class="lock-icon">🎭</div>
                        <div class="lock-text">Bannir le Masque</div>
                    </div>

                    <div class="secret-text-display {% if secret.is_admin %}gold-glow{% else %}pink-glow{% endif %}" id="secretText">
                        "{{ secret.clean_text }}"
                    </div>
                </div>

                <p class="warning-text" id="warningText" style="display:none;">🔥 Ce secret s'est auto-détruit. Il n'existe plus.</p>

                <div id="actionButtons" style="margin-top: 20px; display:none; flex-direction:column; gap:10px;">
                    {% if remaining_secrets > 0 %}
                        <a href="/reveal_next" class="btn btn-reveal" style="width: 100%;">Secret Suivant ({{ remaining_secrets }} restant{% if remaining_secrets > 1 %}s{% endif %})</a>
                    {% endif %}
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
                </div>

                <script>
                    function unlockSecret() {
                        const lock = document.getElementById('vaultLock');
                        const text = document.getElementById('secretText');
                        const warning = document.getElementById('warningText');
                        const actions = document.getElementById('actionButtons');

                        lock.classList.add('unlocked');
                        text.classList.add('visible');

                        setTimeout(() => {
                            warning.style.display = 'block';
                            actions.style.display = 'flex';
                        }, 700);
                    }
                </script>
            {% else %}
                <p style="text-align:center; color:#7a6a5a; font-style:italic; margin: 30px 0;">La boîte est vide... Aucun secret n'est scellé pour le moment.</p>
                <div style="margin-top: 25px;">
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
                </div>
            {% endif %}

        {% elif view == 'login' %}
            <label class="form-title" style="color:#d4af37;">Accès Restreint</label>
            
            {% if error %}
                <div style="color:#a81c1c; text-align:center; font-size:0.85em; margin-bottom:15px;">{{ error }}</div>
            {% endif %}

            <form action="/admin" method="POST">
                <input type="password" name="password" placeholder="Mot de passe secret..." required>
                <button type="submit" class="btn btn-submit" style="width: 100%;">Entrer 🗝️</button>
            </form>

            <div style="margin-top: 15px; text-align:center;">
                <a href="/" style="color:#7a6a5a; text-decoration:none; font-size:0.8em;">Retour au site</a>
            </div>

        {% elif view == 'admin' %}
            <label class="form-title" style="color:#d4af37;">Espace Créateur (Gestion)</label>

            <form action="/add_admin" method="POST" style="margin-bottom: 25px;">
                <textarea name="content" placeholder="Déposer un secret d'Or (Créateur)..." style="height: 80px;" required></textarea>
                <button type="submit" class="btn btn-reveal" style="width: 100%;">Sceller en Or ✨</button>
            </form>

            <p style="text-align:center; color:#7a6a5a; font-size:0.8em; margin-bottom:15px;">Secrets actuellement scellés :</p>
            
            {% for s in secrets %}
                <div style="padding:12px; margin-bottom:10px; border-radius:4px; font-style:italic; font-size:0.9em; display:flex; justify-content:space-between; align-items:center; background:rgba(20,15,15,0.8); border:1px solid rgba(212,175,55,0.2);">
                    <span class="{% if s.is_admin %}gold-glow{% else %}pink-glow{% endif %}">"{{ s.clean_text }}"</span>
                    {% if s.id %}
                        <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Supprimer ce secret ?')">❌</a>
                    {% endif %}
                </div>
            {% else %}
                <p style="text-align:center; color:#7a6a5a; font-style:italic;">Aucun secret trouvé.</p>
            {% endfor %}

            <div style="margin-top: 25px; display:flex; gap:10px;">
                <a href="/" class="btn btn-submit" style="flex:1;">Accueil</a>
                <a href="/logout" class="btn btn-reveal" style="flex:1;">Déconnexion</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def parse_single_secret(item):
    if not item or not isinstance(item, dict):
        return None
    raw_text = item.get('content') or item.get('texte') or item.get('idee') or ""
    is_admin = False
    if raw_text.startswith("[ADMIN]"):
        is_admin = True
        clean_text = raw_text.replace("[ADMIN]", "", 1)
    else:
        clean_text = raw_text

    return {
        'id': item.get('id'),
        'clean_text': clean_text,
        'is_admin': is_admin
    }

def process_secrets(data):
    clean_list = []
    for item in data:
        s = parse_single_secret(item)
        if s:
            clean_list.append(s)
    return clean_list

@app.route('/')
def home():
    total_secrets = 0
    if supabase:
        try:
            res = supabase.table('idees').select('*', count='exact').execute()
            if res.count is not None:
                total_secrets = res.count
            elif res.data:
                total_secrets = len(res.data)
        except Exception as e:
            print("Erreur Supabase Home:", e)
            
    return render_template_string(HTML_TEMPLATE, view='home', total_secrets=total_secrets)

@app.route('/reveal_next')
def reveal_next():
    secret_to_show = None
    remaining_secrets = 0

    if supabase:
        try:
            res = supabase.table('idees').select('*').limit(1).execute()
            
            if res.data and len(res.data) > 0:
                raw_item = res.data[0]
                secret_to_show = parse_single_secret(raw_item)
                secret_id = raw_item.get('id')

                if secret_id:
                    supabase.table('idees').delete().eq('id', secret_id).execute()

                count_res = supabase.table('idees').select('*', count='exact').execute()
                if count_res.count is not None:
                    remaining_secrets = count_res.count
                elif count_res.data:
                    remaining_secrets = len(count_res.data)

        except Exception as e:
            print("Erreur Révélation Supabase:", e)

    return render_template_string(
        HTML_TEMPLATE, 
        view='reveal', 
        secret=secret_to_show, 
        remaining_secrets=remaining_secrets
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            session['logged_in'] = True
        else:
            error = "Mot de passe incorrect 🤫"

    if not session.get('logged_in'):
        return render_template_string(HTML_TEMPLATE, view='login', error=error)

    secrets_list = []
    if supabase:
        try:
            res = supabase.table('idees').select('*').execute()
            if res.data:
                secrets_list = process_secrets(res.data)
        except Exception as e:
            print("Erreur Supabase Admin:", e)
            
    return render_template_string(HTML_TEMPLATE, view='admin', secrets=secrets_list)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_secret():
    content = request.form.get('content')
    if content and supabase:
        try:
            try:
                supabase.table('idees').insert({'content': content}).execute()
            except:
                supabase.table('idees').insert({'texte': content}).execute()
        except Exception as e:
            print("Erreur enregistrement:", e)
    return redirect(url_for('home'))

@app.route('/add_admin', methods=['POST'])
def add_admin_secret():
    if session.get('logged_in'):
        content = request.form.get('content')
        if content and supabase:
            admin_content = "[ADMIN]" + content
            try:
                try:
                    supabase.table('idees').insert({'content': admin_content}).execute()
                except:
                    supabase.table('idees').insert({'texte': admin_content}).execute()
            except Exception as e:
                print("Erreur enregistrement admin:", e)
    return redirect(url_for('admin'))

@app.route('/delete/<int:secret_id>')
def delete_secret(secret_id):
    if session.get('logged_in') and supabase:
        try:
            supabase.table('idees').delete().eq('id', secret_id).execute()
        except Exception as e:
            print("Erreur suppression:", e)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
