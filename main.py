import os
from flask import Flask, request, redirect, url_for, render_template_string, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cle_secrete_boite_secrets_999")

# 🔒 MOT DE PASSE ADMIN
ADMIN_PASSWORD = "Therec@nbeonly1"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Erreur initialisation Supabase:", e)

# --- DESIGN HAUTE COUTURE / SCEAU 3D INTERACTIF & PARTICULES ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boîte-secrets</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        
        body {
            background: #070606;
            background-image: 
                radial-gradient(circle at 50% 30%, rgba(35, 15, 18, 0.6) 0%, rgba(5, 5, 5, 0.98) 80%),
                url('https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #d1c5b4;
            font-family: 'Montserrat', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .header { text-align: center; margin-bottom: 30px; }
        
        h1 {
            font-family: 'Cormorant Garamond', serif;
            font-weight: 400;
            font-style: italic;
            color: #d4af37;
            font-size: 3.6em;
            letter-spacing: 2px;
            text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
            line-height: 1;
        }
        
        .subtitle {
            font-family: 'Cinzel', serif;
            color: #8c7e6c;
            font-size: 0.7em;
            letter-spacing: 6px;
            text-transform: uppercase;
            margin-top: 10px;
        }
        
        .card {
            width: 100%;
            max-width: 480px;
            background: rgba(12, 10, 10, 0.88);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 4px;
            padding: 40px 32px;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.95), inset 0 0 0 1px rgba(212, 175, 55, 0.08);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            position: relative;
            overflow: hidden;
        }
        
        .form-title {
            color: #b39250;
            font-family: 'Cinzel', serif;
            font-size: 0.75em;
            letter-spacing: 3px;
            margin-bottom: 20px;
            display: block;
            text-transform: uppercase;
            text-align: center;
        }
        
        textarea, input[type="password"] {
            width: 100%;
            background: rgba(6, 5, 5, 0.85);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 2px;
            color: #e6dfd5;
            padding: 18px;
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.2em;
            font-style: italic;
            margin-bottom: 24px;
            transition: all 0.4s ease;
        }
        
        textarea { height: 120px; resize: none; user-select: text; }
        
        textarea:focus, input[type="password"]:focus {
            outline: none;
            border-color: rgba(212, 175, 55, 0.6);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
        }
        
        .buttons-group { display: flex; gap: 14px; margin-bottom: 20px; }
        
        .btn {
            border: none;
            border-radius: 2px;
            padding: 16px 14px;
            font-family: 'Cinzel', serif;
            font-size: 0.75em;
            letter-spacing: 3px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .btn-submit {
            flex: 1.6;
            background: linear-gradient(135deg, #3b0a0d 0%, #5e1117 100%);
            color: #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }
        
        .btn-submit:hover {
            background: linear-gradient(135deg, #4d0d11 0%, #73151d 100%);
            box-shadow: 0 0 20px rgba(94, 17, 23, 0.6);
        }
        
        .btn-reveal {
            flex: 1.2;
            background: transparent;
            color: #b39250;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }

        .btn-reveal:hover {
            background: rgba(212, 175, 55, 0.08);
            border-color: rgba(212, 175, 55, 0.6);
        }
        
        .counter-box {
            text-align: center;
            border-top: 1px solid rgba(212, 175, 55, 0.12);
            padding-top: 24px;
        }
        
        .counter-number {
            font-family: 'Cormorant Garamond', serif;
            color: #d4af37;
            font-size: 2.8em;
            line-height: 1;
        }
        
        .counter-label {
            font-family: 'Cinzel', serif;
            color: #6e6254;
            font-size: 0.65em;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 6px;
        }

        /* --- SANCTUAIRE & PERSPECTIVE 3D --- */
        .sanctuary-container {
            position: relative;
            min-height: 260px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            perspective: 1000px; /* Activer la profondeur 3D */
        }

        canvas#particleCanvas {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 15;
        }

        .hold-seal-area {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 20;
            transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* ENSEMBLE DU SCEAU EN REAL 3D CSS */
        .seal-3d-stage {
            position: relative;
            width: 130px;
            height: 130px;
            transform-style: preserve-3d;
            transition: transform 0.15s ease-out;
        }

        /* Tranche/Épaisseur de la pièce (Arrière 3D) */
        .seal-3d-stage::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 50%;
            background: linear-gradient(180deg, #d4af37 0%, #3a280b 50%, #0d0903 100%);
            transform: translateZ(-12px);
            box-shadow: 0 25px 35px rgba(0, 0, 0, 0.95), 0 0 20px rgba(212, 175, 55, 0.2);
        }

        /* Corps SVG Principal (Niveau 0) */
        .seal-svg-main {
            position: relative;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            transform: translateZ(0px);
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.8));
        }

        /* Emblème Gravé Flottant au-dessus (Relief Proéminent +20px) */
        .seal-floating-emblem {
            position: absolute;
            top: 50%; left: 50%;
            width: 60px; height: 60px;
            margin-top: -30px; margin-left: -30px;
            transform: translateZ(22px);
            pointer-events: none;
            transition: transform 0.3s ease;
        }

        .seal-instructions {
            font-family: 'Cinzel', serif;
            font-size: 0.7em;
            letter-spacing: 3px;
            color: #8c7e6c;
            text-transform: uppercase;
            margin-top: 25px;
            transition: color 0.4s ease, text-shadow 0.4s ease;
        }

        .hold-seal-area.holding .seal-instructions {
            color: #ffaa00;
            text-shadow: 0 0 12px rgba(255, 170, 0, 0.6);
        }

        /* Conteneur de Texte Révélé */
        .revealed-text-box {
            width: 100%;
            text-align: center;
            opacity: 0;
            filter: blur(14px);
            transform: scale(0.95);
            transition: opacity 1.6s cubic-bezier(0.16, 1, 0.3, 1), 
                        filter 1.6s cubic-bezier(0.16, 1, 0.3, 1), 
                        transform 1.6s cubic-bezier(0.16, 1, 0.3, 1);
            user-select: text;
        }

        .revealed-text-box.visible {
            opacity: 1;
            filter: blur(0px);
            transform: scale(1);
        }

        .secret-quote {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.45em;
            line-height: 1.6;
            font-style: italic;
            padding: 10px;
        }

        .gold-secret { color: #f2e3b6; text-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
        .pink-secret { color: #ebd0d5; text-shadow: 0 0 20px rgba(180, 80, 100, 0.3); }

        .warning-subtitle {
            color: #5a5045;
            font-family: 'Cinzel', serif;
            font-size: 0.65em;
            letter-spacing: 2px;
            text-align: center;
            margin-top: 20px;
            text-transform: uppercase;
        }

        .delete-btn { color: #a83b3b; text-decoration: none; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Boîte-secrets</h1>
        <div class="subtitle">Le Sanctuaire de vos Confidences</div>
    </div>

    <div class="card">
        {% if view == 'home' %}
            <form action="/add" method="POST">
                <label class="form-title">Confier un secret</label>
                <textarea name="content" placeholder="Une pensée, un désir, un aveu..." required></textarea>
                
                <div class="buttons-group">
                    <button type="submit" class="btn btn-submit">Sceller</button>
                    <a href="/reveal_next" class="btn btn-reveal">Révéler</a>
                </div>
            </form>

            <div class="counter-box">
                <div class="counter-number">{{ total_secrets }}</div>
                <div class="counter-label">Secrets Retenus</div>
            </div>

        {% elif view == 'reveal' %}
            <label class="form-title">Révélation</label>
            
            {% if secret and secret.clean_text %}
                <div class="sanctuary-container">
                    
                    <!-- CANVA PARTICULES EN TEMPS RÉEL -->
                    <canvas id="particleCanvas"></canvas>

                    <!-- SCEAU AVEC EFFET 3D PARALLAXE -->
                    <div class="hold-seal-area" id="sealArea">
                        <div class="seal-3d-stage" id="sealStage">
                            
                            <!-- SOCLE BASE VECTORIEL -->
                            <svg class="seal-svg-main" viewBox="0 0 130 130">
                                <defs>
                                    <radialGradient id="goldPlate" cx="35%" cy="30%" r="70%">
                                        <stop offset="0%" stop-color="#fff5cc"/>
                                        <stop offset="35%" stop-color="#d4af37"/>
                                        <stop offset="75%" stop-color="#6e5015"/>
                                        <stop offset="100%" stop-color="#241703"/>
                                    </radialGradient>

                                    <linearGradient id="liquidGrad" x1="0" y1="1" x2="0" y2="0">
                                        <stop offset="0%" stop-color="#800000"/>
                                        <stop offset="50%" stop-color="#ff3300"/>
                                        <stop offset="100%" stop-color="#ffcc00"/>
                                    </linearGradient>

                                    <clipPath id="liquidClip">
                                        <rect id="liquidRect" x="0" y="130" width="130" height="130"/>
                                    </clipPath>

                                    <filter id="glow">
                                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                                        <feMerge>
                                            <feMergeNode in="coloredBlur"/>
                                            <feMergeNode in="SourceGraphic"/>
                                        </feMerge>
                                    </filter>
                                </defs>

                                <!-- Pièce d'Or sculptée -->
                                <circle cx="65" cy="65" r="58" fill="url(#goldPlate)" stroke="#1a1203" stroke-width="3"/>
                                <circle cx="65" cy="65" r="50" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
                                <circle cx="65" cy="65" r="48" fill="#0c0806" stroke="#4a3610" stroke-width="2"/>

                                <!-- Reservoir de Liquide Magmatique -->
                                <circle cx="65" cy="65" r="47" fill="url(#liquidGrad)" clip-path="url(#liquidClip)" opacity="0.92"/>

                                <!-- Fissures / Incandescence -->
                                <g id="cracksGroup" opacity="0" filter="url(#glow)">
                                    <path d="M65 22 L60 42 L70 58 L52 80 L65 108" stroke="#ffeb3b" stroke-width="2.5" fill="none"/>
                                    <path d="M70 58 L92 52 L108 68" stroke="#ff9800" stroke-width="2" fill="none"/>
                                    <path d="M60 42 L32 36 L22 52" stroke="#ff5722" stroke-width="2" fill="none"/>
                                </g>
                            </svg>

                            <!-- EMBLEM FLOTTANT EN HAUTEUR 3D -->
                            <svg class="seal-floating-emblem" viewBox="0 0 60 60">
                                <polygon points="30,5 38,20 55,30 38,40 30,55 22,40 5,30 22,20" fill="none" stroke="#fceabb" stroke-width="2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.8))"/>
                                <circle cx="30" cy="30" r="5" fill="#fceabb"/>
                            </svg>

                        </div>
                        <div class="seal-instructions" id="sealInstruction">Maintenir pour rompre le sceau</div>
                    </div>

                    <!-- TEXTE RÉVÉLÉ -->
                    <div class="revealed-text-box" id="revealedBox">
                        <div class="secret-quote {% if secret.is_admin %}gold-secret{% else %}pink-secret{% endif %}">
                            « {{ secret.clean_text }} »
                        </div>
                    </div>
                </div>

                <div class="warning-subtitle" id="warningNotice" style="opacity: 0; transition: opacity 1s ease;">
                    — Ce secret s'est éteint à jamais —
                </div>

                <div id="actionControls" style="margin-top: 25px; display:none; flex-direction:column; gap:12px;">
                    {% if remaining_secrets > 0 %}
                        <a href="/reveal_next" class="btn btn-reveal" style="width: 100%;">Secret Suivant ({{ remaining_secrets }})</a>
                    {% endif %}
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer une confidence</a>
                </div>

                <script>
                    const sealArea = document.getElementById('sealArea');
                    const sealStage = document.getElementById('sealStage');
                    const sealInstruction = document.getElementById('sealInstruction');
                    const liquidRect = document.getElementById('liquidRect');
                    const cracksGroup = document.getElementById('cracksGroup');
                    const revealedBox = document.getElementById('revealedBox');
                    const warningNotice = document.getElementById('warningNotice');
                    const actionControls = document.getElementById('actionControls');
                    const canvas = document.getElementById('particleCanvas');
                    const ctx = canvas.getContext('2d');

                    let timer = null;
                    let startTime = 0;
                    const DURATION = 2400; // 2.4s
                    let isHolding = false;
                    let currentProgress = 0;

                    function resizeCanvas() {
                        canvas.width = canvas.offsetWidth;
                        canvas.height = canvas.offsetHeight;
                    }
                    resizeCanvas();
                    window.addEventListener('resize', resizeCanvas);

                    // --- PARALLAXE 3D INTERACTIF À LA SOURIS / TOUCHER ---
                    function handle3DTilt(e) {
                        if (isHolding || sealArea.style.pointerEvents === 'none') return;

                        const rect = sealArea.getBoundingClientRect();
                        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

                        const x = clientX - rect.left - rect.width / 2;
                        const y = clientY - rect.top - rect.height / 2;

                        // Angle de rotation max 25 deg
                        const tiltX = (y / (rect.height / 2)) * -25;
                        const tiltY = (x / (rect.width / 2)) * 25;

                        sealStage.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.04)`;
                    }

                    function reset3DTilt() {
                        if (!isHolding && sealArea.style.pointerEvents !== 'none') {
                            sealStage.style.transform = `rotateX(0deg) rotateY(0deg) scale(1)`;
                        }
                    }

                    sealArea.addEventListener('mousemove', handle3DTilt);
                    sealArea.addEventListener('mouseleave', reset3DTilt);
                    sealArea.addEventListener('touchmove', handle3DTilt, {passive: true});

                    // --- PARTICULES (FUMÉE & ÉTINCELLES INCANDESCENTES) ---
                    let particles = [];

                    class Particle {
                        constructor(x, y, type = 'smoke') {
                            this.x = x || canvas.width / 2 + (Math.random() - 0.5) * 30;
                            this.y = y || canvas.height / 2 + (Math.random() - 0.5) * 30;
                            this.type = type;

                            if (type === 'ember') {
                                this.radius = Math.random() * 3 + 1;
                                this.vx = (Math.random() - 0.5) * 4;
                                this.vy = -(Math.random() * 3.5 + 1.5);
                                this.alpha = 1;
                                this.decay = Math.random() * 0.03 + 0.015;
                                this.color = Math.random() > 0.4 ? '255, 200, 50' : '255, 80, 20';
                            } else {
                                this.radius = Math.random() * 10 + 6;
                                this.maxRadius = this.radius + 40;
                                this.vx = (Math.random() - 0.5) * 1.5;
                                this.vy = -(Math.random() * 1.8 + 0.6);
                                this.alpha = Math.random() * 0.35 + 0.15;
                                this.decay = Math.random() * 0.005 + 0.003;
                                this.color = Math.random() > 0.5 ? '212, 175, 55' : '90, 75, 65';
                            }
                        }

                        update() {
                            this.x += this.vx;
                            this.y += this.vy;
                            if (this.type === 'smoke' && this.radius < this.maxRadius) {
                                this.radius += 0.45;
                            }
                            this.alpha -= this.decay;
                        }

                        draw() {
                            if (this.alpha <= 0) return;
                            ctx.save();
                            ctx.beginPath();
                            if (this.type === 'ember') {
                                ctx.shadowBlur = 10;
                                ctx.shadowColor = `rgba(${this.color}, 0.9)`;
                                ctx.fillStyle = `rgba(${this.color}, ${this.alpha})`;
                                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                                ctx.fill();
                            } else {
                                let grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius);
                                grad.addColorStop(0, `rgba(${this.color}, ${this.alpha})`);
                                grad.addColorStop(0.7, `rgba(${this.color}, ${this.alpha * 0.3})`);
                                grad.addColorStop(1, `rgba(${this.color}, 0)`);
                                ctx.fillStyle = grad;
                                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                                ctx.fill();
                            }
                            ctx.restore();
                        }
                    }

                    function renderParticles() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        if (isHolding) {
                            particles.push(new Particle(null, null, 'smoke'));
                            if (currentProgress > 0.35 && Math.random() > 0.25) {
                                particles.push(new Particle(null, null, 'ember'));
                            }
                        }

                        for (let i = particles.length - 1; i >= 0; i--) {
                            particles[i].update();
                            particles[i].draw();
                            if (particles[i].alpha <= 0) {
                                particles.splice(i, 1);
                            }
                        }

                        requestAnimationFrame(renderParticles);
                    }
                    renderParticles();

                    function triggerExplosion() {
                        for (let i = 0; i < 50; i++) particles.push(new Particle(canvas.width / 2, canvas.height / 2, 'ember'));
                        for (let i = 0; i < 35; i++) particles.push(new Particle(canvas.width / 2, canvas.height / 2, 'smoke'));
                    }

                    // --- RITUEL DE MAINTIEN 3D ---
                    function startHold(e) {
                        e.preventDefault();
                        if (sealArea.style.pointerEvents === 'none') return;

                        isHolding = true;
                        startTime = Date.now();
                        sealInstruction.textContent = "Fusion en cours...";
                        sealArea.classList.add('holding');

                        timer = setInterval(() => {
                            const elapsed = Date.now() - startTime;
                            currentProgress = Math.min(elapsed / DURATION, 1);

                            // 1. Remplissage du liquide magmatique (130px -> 0px)
                            const liquidY = 130 - (currentProgress * 130);
                            liquidRect.setAttribute('y', liquidY);

                            // 2. Fissures incandescentes (50%+ progress)
                            if (currentProgress > 0.5) {
                                const crackOpacity = (currentProgress - 0.5) * 2;
                                cracksGroup.setAttribute('opacity', crackOpacity);
                            } else {
                                cracksGroup.setAttribute('opacity', 0);
                            }

                            // 3. Vibration & Oscillation 3D sous la pression
                            const vibrateX = (Math.random() - 0.5) * (currentProgress * 14);
                            const vibrateY = (Math.random() - 0.5) * (currentProgress * 14);
                            const vibrateRot = (Math.random() - 0.5) * (currentProgress * 8);
                            sealStage.style.transform = `rotateX(${vibrateX}deg) rotateY(${vibrateY}deg) rotateZ(${vibrateRot}deg) scale(${1 + currentProgress * 0.08})`;

                            if (currentProgress >= 1) {
                                completeReveal();
                            }
                        }, 20);
                    }

                    function cancelHold() {
                        if (sealArea.style.pointerEvents === 'none') return;
                        isHolding = false;
                        currentProgress = 0;
                        clearInterval(timer);
                        
                        // Réinitialiser les visuels 3D
                        liquidRect.setAttribute('y', 130);
                        cracksGroup.setAttribute('opacity', 0);
                        sealInstruction.textContent = "Maintenir pour rompre le sceau";
                        sealArea.classList.remove('holding');
                        reset3DTilt();
                    }

                    function completeReveal() {
                        clearInterval(timer);
                        isHolding = false;
                        sealArea.style.pointerEvents = 'none';

                        // Animation de rupture 3D (bascule vers l'arrière et s'enfonce dans le fond)
                        sealStage.style.transition = 'transform 0.8s cubic-bezier(0.5, 0, 0.75, 0)';
                        sealStage.style.transform = 'rotateX(85deg) rotateZ(180deg) translateZ(-400px) scale(0.2)';
                        sealArea.style.opacity = '0';

                        // Déflagration d'étincelles et fumée
                        triggerExplosion();

                        setTimeout(() => {
                            sealArea.style.display = 'none';
                            revealedBox.classList.add('visible');
                            warningNotice.style.opacity = '1';
                            actionControls.style.display = 'flex';
                        }, 600);
                    }

                    sealArea.addEventListener('mousedown', startHold);
                    sealArea.addEventListener('mouseup', cancelHold);
                    sealArea.addEventListener('mouseleave', cancelHold);

                    sealArea.addEventListener('touchstart', startHold, {passive: false});
                    sealArea.addEventListener('touchend', cancelHold);
                    sealArea.addEventListener('touchcancel', cancelHold);
                </script>
            {% else %}
                <p style="text-align:center; color:#6e6254; font-family:'Cormorant Garamond', serif; font-size: 1.2em; font-style:italic; margin: 40px 0;">Le sanctuaire est silencieux... Aucun secret n'attend d'être révélé.</p>
                <div style="margin-top: 25px;">
                    <a href="/" class="btn btn-submit" style="width: 100%;">Déposer un secret</a>
                </div>
            {% endif %}

        {% elif view == 'login' %}
            <label class="form-title">Accès Restreint</label>
            
            {% if error %}
                <div style="color:#a83b3b; text-align:center; font-size:0.8em; margin-bottom:15px; font-family:'Cinzel', serif;">{{ error }}</div>
            {% endif %}

            <form action="/admin" method="POST">
                <input type="password" name="password" placeholder="Mot de passe..." required>
                <button type="submit" class="btn btn-submit" style="width: 100%;">Franchir le Seuil</button>
            </form>

            <div style="margin-top: 20px; text-align:center;">
                <a href="/" style="color:#6e6254; text-decoration:none; font-size:0.75em; font-family:'Cinzel', serif; letter-spacing: 2px;">Retour</a>
            </div>

        {% elif view == 'admin' %}
            <label class="form-title">Espace Gardien</label>

            <form action="/add_admin" method="POST" style="margin-bottom: 30px;">
                <textarea name="content" placeholder="Déposer un secret d'Or..." style="height: 90px;" required></textarea>
                <button type="submit" class="btn btn-reveal" style="width: 100%;">Sceller en Or ✨</button>
            </form>

            <p style="text-align:center; color:#6e6254; font-family:'Cinzel', serif; font-size:0.7em; letter-spacing: 2px; margin-bottom:15px; text-transform:uppercase;">Secrets actuellement scellés</p>
            
            {% for s in secrets %}
                <div style="padding:14px; margin-bottom:12px; border-radius:2px; font-family:'Cormorant Garamond', serif; font-size:1.1em; font-style:italic; display:flex; justify-content:space-between; align-items:center; background:rgba(6,5,5,0.7); border:1px solid rgba(212,175,55,0.15);">
                    <span class="{% if s.is_admin %}gold-secret{% else %}pink-secret{% endif %}">« {{ s.clean_text }} »</span>
                    {% if s.id %}
                        <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Supprimer ce secret ?')">✕</a>
                    {% endif %}
                </div>
            {% else %}
                <p style="text-align:center; color:#5a5045; font-style:italic;">Aucun secret présent.</p>
            {% endfor %}

            <div style="margin-top: 30px; display:flex; gap:12px;">
                <a href="/" class="btn btn-submit" style="flex:1;">Accueil</a>
                <a href="/logout" class="btn btn-reveal" style="flex:1;">Quitter</a>
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
            error = "Accès refusé"

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
