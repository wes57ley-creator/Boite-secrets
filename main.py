import os
from flask import Flask, request, redirect, url_for, render_template_string, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cle_secrete_boite_secrets_999")

# 🔒 VOTRE MOT DE PASSE ADMIN
ADMIN_PASSWORD = "rouge2026"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Erreur initialisation Supabase:", e)

# --- DESIGN EYES WIDE SHUT + CHÂTEAU + ANIMATION MYSTIQUE ---
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
            max-width: 440px;
            background: rgba(14, 14, 14, 0.88);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            padding: 30px 25px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.95);
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
        }
        
        textarea, input[type="password"] {
            width: 100%;
            background: rgba(10, 10, 10, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 10px;
            color: #f0f0f0;
            padding: 15px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.95em;
            margin-bottom: 20px;
        }
        
        textarea { height: 110px; font-style: italic; resize: none; }
        
        textarea:focus, input[type="password"]:focus {
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
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            font-style: italic;
            word-break: break-word;
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            font-size: 1.1em;
            line-height: 1.5;
        }

        /* Vos secrets (Admin) = OR */
        .secret-gold {
            background: rgba(212, 175, 55, 0.12);
            border: 1px solid rgba(212, 175, 55, 0.5);
            color: #f3e5ab;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        }

        /* Secrets invités = ROSE FONCÉ */
        .secret-pink {
            background: rgba(194, 24, 91, 0.12);
            border: 1px solid rgba(194, 24, 91, 0.5);
            color: #f8bbd0;
            box-shadow: 0 0 15px rgba(194, 24, 91, 0.2);
        }

        .delete-btn {
            color: #e74c3c;
            text-decoration: none;
            font-size: 0.8em;
            margin-left: 10px;
            font-style: normal;
        }

        .error-msg {
            color: #e74c3c;
            text-align: center;
            font-size: 0.85em;
            margin-bottom: 15px;
        }

        .warning-text {
            color: #8a7a6a;
            font-size: 0.75em;
            text-align: center;
            margin-top: 10px;
            font-style: italic;
        }

        /* --- ANIMATION DU SCEAU --- */
        .reveal-box {
            position: relative;
            min-height: 120px;
            margin: 15px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .seal-wrapper {
            position: absolute;
            z-index: 2;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .seal-wrapper:hover { transform: scale(1.08); }

        .seal {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: float 3s ease-in-out infinite;
        }

        .seal-gold {
            background: radial-gradient(circle at 30% 30%, #f3e5ab, #d4af37, #996515);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        }

        .seal-pink {
            background: radial-gradient(circle at 30% 30%, #f8bbd0, #c2185b, #6b002b);
            box-shadow: 0 0 20px rgba(194, 24, 91, 0.6);
        }

        .seal-icon { font-size: 1.8rem; color: #0d0d0d; user-select: none; }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        .seal-wrapper.breaking {
            animation: pulse-break 0.7s forwards;
        }

        @keyframes pulse-break {
            0% { transform: scale(1); filter: brightness(1); }
            50% { transform: scale(1.3); filter: brightness(2); }
            100% { transform: scale(0); opacity: 0; }
        }

        .secret-text {
            opacity: 0;
            visibility: hidden;
            width: 100%;
        }

        .secret-text.visible {
            visibility: visible;
            opacity: 1;
        }

        .letter {
            display: inline-block;
            opacity: 0;
            transform: translateY(8px);
            filter: blur(4px);
            transition: opacity 0.3s ease, transform 0.3s ease, filter 0.3s ease;
        }

        .letter.reveal {
            opacity: 1;
            transform: translateY(0);
            filter: blur(0);
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
                    <a href="/reveal_next" class="btn btn-reveal">Révéler</a>
                </div>
            </form>

            <div class="counter-box">
                <div class="counter-number">{{ total_secrets }}</div>
                <div class="counter-label">Secrets Scellés</div>
            </div>

        {% elif view == 'reveal' %}
            <label class="form-title" style="margin-bottom: 10px; display:block; text-align:center;">Secret Révélé</label>
            
            {% if secret %}
                <div class="reveal-box">
                    <div class="seal-wrapper" id="sealWrapper" onclick="breakSeal()">
                        <div class="seal {% if secret.is_admin %}seal-gold{% else %}seal-pink{% endif %}">
                            <span class="seal-icon">✦</span>
                        </div>
                    </div>

                    <div id="secretContainer" class="secret-text secret-item {% if secret.is_admin %}secret-gold{% else %}secret-pink{% endif %}">
                        "<span id="secretText">{{ secret.clean_text }}</span>"
                    </div>
                </div>

                <p id="hintText" style="text-align:center; color:#d4af37; font-size:0.8em; margin-bottom:10px; cursor:pointer;" onclick="breakSeal()">👉 Touchez le sceau pour le briser...</p>
                <p class="warning-text" id="warningText" style="display:none;">🔥 Ce secret s'est auto-détruit. Il n'existe plus.</p>

                <div id="actionButtons" style="margin-top: 20px; display:none; flex-direction:column; gap:10px;">
                    {% if remaining_secrets > 0 %}
                        <a href="/reveal_next" class="btn btn-reveal" style="width: 100%;">Secret Suivant ({{ remaining_secrets }} restant{% if remaining_secrets > 1 %}s{% endif %})</a>
                    {% endif %}
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
                </div>

                <script>
                    let isBroken = false;
                    function breakSeal() {
                        if (isBroken) return;
                        isBroken = true;

                        const seal = document.getElementById('sealWrapper');
                        const container = document.getElementById('secretContainer');
                        const textSpan = document.getElementById('secretText');
                        const hintText = document.getElementById('hintText');
                        const warningText = document.getElementById('warningText');
                        const actionButtons = document.getElementById('actionButtons');

                        seal.classList.add('breaking');
                        hintText.style.display = 'none';

                        const rawText = textSpan.innerText;
                        textSpan.innerHTML = '';
                        const letters = rawText.split('').map(char => {
                            const span = document.createElement('span');
                            span.className = 'letter';
                            span.innerHTML = char === ' ' ? '&nbsp;' : char;
                            textSpan.appendChild(span);
                            return span;
                        });

                        setTimeout(() => {
                            seal.style.display = 'none';
                            container.classList.add('visible');

                            letters.forEach((letter, index) => {
                                setTimeout(() => {
                                    letter.classList.add('reveal');
                                }, index * 30);
                            });

                            setTimeout(() => {
                                warningText.style.display = 'block';
                                actionButtons.style.display = 'flex';
                            }, letters.length * 30 + 300);

                        }, 500);
                    }
                </script>
            {% else %}
                <p style="text-align:center; color:#8a7a6a; font-style:italic; margin: 30px 0;">La boîte est vide... Aucun secret n'est scellé pour le moment.</p>
                <div style="margin-top: 25px;">
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
                </div>
            {% endif %}

        {% elif view == 'login' %}
            <label class="form-title" style="margin-bottom: 20px; display:block; text-align:center; color:#d4af37;">Accès Restreint</label>
            
            {% if error %}
                <div class="error-msg">{{ error }}</div>
            {% endif %}

            <form action="/admin" method="POST">
                <input type="password" name="password" placeholder="Mot de passe secret..." required>
                <button type="submit" class="btn btn-submit" style="width: 100%;">Entrer 🗝️</button>
            </form>

            <div style="margin-top: 15px; text-align:center;">
                <a href="/" style="color:#8a7a6a; text-decoration:none; font-size:0.8em;">Retour au site</a>
            </div>

        {% elif view == 'admin' %}
            <label class="form-title" style="margin-bottom: 15px; display:block; text-align:center; color:#d4af37;">Espace Admin (Gestion)</label>

            <form action="/add_admin" method="POST" style="margin-bottom: 25px;">
                <textarea name="content" placeholder="Déposer un secret d'Or (Créateur)..." style="height: 80px;" required></textarea>
                <button type="submit" class="btn btn-reveal" style="width: 100%;">Sceller en Or ✨</button>
            </form>

            <p style="text-align:center; color:#8a7a6a; font-size:0.8em; margin-bottom:15px;">Secrets actuellement en attente dans la boîte :</p>
            
            {% for s in secrets %}
                <div class="secret-item {% if s.is_admin %}secret-gold{% else %}secret-pink{% endif %}" style="font-size:0.9em; padding:10px;">
                    <span>"{{ s.clean_text }}"</span>
                    {% if s.id %}
                        <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Supprimer ce secret ?')">❌</a>
                    {% endif %}
                </div>
            {% else %}
                <p style="text-align:center; color:#8a7a6a; font-style:italic;">Aucune donnée trouvée.</p>
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
