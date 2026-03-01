from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

score = {"wins": 0, "losses": 0, "draws": 0}

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Rock Paper Scissors</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Raleway:wght@400;600&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Raleway', sans-serif;
            background: #0a0015;
            color: white;
            text-align: center;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated starry background */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: 
                radial-gradient(ellipse at 20% 50%, rgba(120,40,200,0.3) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(40,80,200,0.3) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 80%, rgba(200,40,120,0.2) 0%, transparent 50%);
            z-index: -1;
            animation: bgShift 8s ease-in-out infinite alternate;
        }

        @keyframes bgShift {
            0% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .stars {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
            background-image: 
                radial-gradient(1px 1px at 10% 15%, white, transparent),
                radial-gradient(1px 1px at 25% 40%, white, transparent),
                radial-gradient(1px 1px at 40% 10%, white, transparent),
                radial-gradient(1px 1px at 55% 60%, white, transparent),
                radial-gradient(1px 1px at 70% 25%, white, transparent),
                radial-gradient(1px 1px at 85% 70%, white, transparent),
                radial-gradient(1px 1px at 15% 80%, white, transparent),
                radial-gradient(1px 1px at 90% 45%, white, transparent),
                radial-gradient(1px 1px at 35% 90%, white, transparent),
                radial-gradient(1px 1px at 60% 5%,  white, transparent),
                radial-gradient(2px 2px at 5%  55%, #c084fc, transparent),
                radial-gradient(2px 2px at 75% 85%, #818cf8, transparent),
                radial-gradient(2px 2px at 45% 35%, #f0abfc, transparent);
            animation: twinkle 4s ease-in-out infinite alternate;
        }

        @keyframes twinkle {
            0%   { opacity: 0.6; }
            100% { opacity: 1; }
        }

        .container {
            padding: 40px 20px;
            max-width: 700px;
            margin: 0 auto;
        }

        .title {
            font-family: 'Cinzel', serif;
            font-size: 2.8em;
            background: linear-gradient(135deg, #c084fc, #818cf8, #f0abfc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            margin-bottom: 5px;
            animation: glow 3s ease-in-out infinite alternate;
        }

        @keyframes glow {
            0%   { filter: brightness(1); }
            100% { filter: brightness(1.4); }
        }

        .subtitle {
            color: #a78bfa;
            font-size: 1em;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 40px;
        }

        .choices {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .magic-btn {
            font-size: 1em;
            font-family: 'Raleway', sans-serif;
            font-weight: 600;
            letter-spacing: 1px;
            padding: 0;
            border: none;
            cursor: pointer;
            background: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            transition: transform 0.3s;
        }

        .magic-btn:hover { transform: translateY(-10px); }

        .btn-circle {
            width: 110px;
            height: 110px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.8em;
            position: relative;
            transition: box-shadow 0.3s;
        }

        .rock .btn-circle {
            background: linear-gradient(135deg, #7c3aed, #4c1d95);
            box-shadow: 0 0 20px rgba(124,58,237,0.6);
        }
        .paper .btn-circle {
            background: linear-gradient(135deg, #2563eb, #1e3a8a);
            box-shadow: 0 0 20px rgba(37,99,235,0.6);
        }
        .scissors .btn-circle {
            background: linear-gradient(135deg, #db2777, #831843);
            box-shadow: 0 0 20px rgba(219,39,119,0.6);
        }

        .rock:hover .btn-circle     { box-shadow: 0 0 40px rgba(124,58,237,1),  0 0 80px rgba(124,58,237,0.4); }
        .paper:hover .btn-circle    { box-shadow: 0 0 40px rgba(37,99,235,1),   0 0 80px rgba(37,99,235,0.4); }
        .scissors:hover .btn-circle { box-shadow: 0 0 40px rgba(219,39,119,1),  0 0 80px rgba(219,39,119,0.4); }

        .btn-label { color: #c4b5fd; font-size: 0.95em; }

        /* Result */
        .result-box {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(192,132,252,0.3);
            border-radius: 24px;
            padding: 30px;
            margin: 30px auto;
            max-width: 420px;
            backdrop-filter: blur(10px);
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .choices-made {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 20px;
        }

        .choice-card {
            text-align: center;
        }

        .choice-card .emoji { font-size: 3em; }
        .choice-card .label { color: #a78bfa; font-size: 0.85em; margin-top: 5px; }

        .vs { font-size: 1.5em; color: #6b7280; font-weight: bold; }

        .result-text {
            font-family: 'Cinzel', serif;
            font-size: 1.8em;
            margin-top: 10px;
        }
        .win  { color: #4ade80; text-shadow: 0 0 20px #4ade80; }
        .lose { color: #f87171; text-shadow: 0 0 20px #f87171; }
        .draw { color: #fbbf24; text-shadow: 0 0 20px #fbbf24; }

        /* Scoreboard */
        .scoreboard {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(192,132,252,0.2);
            border-radius: 24px;
            padding: 25px;
            margin: 20px auto;
            max-width: 420px;
            backdrop-filter: blur(10px);
        }

        .scoreboard h3 {
            font-family: 'Cinzel', serif;
            color: #c084fc;
            font-size: 1.2em;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        .scores {
            display: flex;
            justify-content: space-around;
        }

        .score-item { text-align: center; }
        .score-item .number {
            font-size: 2.5em;
            font-weight: bold;
            font-family: 'Cinzel', serif;
        }
        .score-item .slabel { font-size: 0.8em; letter-spacing: 2px; margin-top: 5px; }

        .wins-item  .number { color: #4ade80; }
        .draws-item .number { color: #fbbf24; }
        .loses-item .number { color: #f87171; }
        .wins-item  .slabel { color: #4ade80; }
        .draws-item .slabel { color: #fbbf24; }
        .loses-item .slabel { color: #f87171; }

        .divider {
            width: 1px;
            background: rgba(192,132,252,0.3);
            margin: 0 10px;
        }
    </style>
</head>
<body>
<div class="stars"></div>
<div class="container">

    <h1 class="title">✨ Mystical Duel ✨</h1>
    <p class="subtitle">Choose your spell</p>

    <form method="POST">
        <div class="choices">
            <button class="magic-btn rock" name="choice" value="Rock">
                <div class="btn-circle">🪨</div>
                <span class="btn-label">Rock</span>
            </button>
            <button class="magic-btn paper" name="choice" value="Paper">
                <div class="btn-circle">📄</div>
                <span class="btn-label">Paper</span>
            </button>
            <button class="magic-btn scissors" name="choice" value="Scissors">
                <div class="btn-circle">✂️</div>
                <span class="btn-label">Scissors</span>
            </button>
        </div>
    </form>

    {% if result %}
    <div class="result-box">
        <div class="choices-made">
            <div class="choice-card">
                <div class="emoji">
                    {% if player == "Rock" %}🪨{% elif player == "Paper" %}📄{% else %}✂️{% endif %}
                </div>
                <div class="label">You</div>
            </div>
            <div class="vs">VS</div>
            <div class="choice-card">
                <div class="emoji">
                    {% if computer == "Rock" %}🪨{% elif computer == "Paper" %}📄{% else %}✂️{% endif %}
                </div>
                <div class="label">Computer</div>
            </div>
        </div>
        {% if "Win" in result %}
            <div class="result-text win">{{ result }}</div>
        {% elif "Lose" in result %}
            <div class="result-text lose">{{ result }}</div>
        {% else %}
            <div class="result-text draw">{{ result }}</div>
        {% endif %}
    </div>
    {% endif %}

    <div class="scoreboard">
        <h3>⚔️ BATTLE RECORD ⚔️</h3>
        <div class="scores">
            <div class="score-item wins-item">
                <div class="number">{{ score.wins }}</div>
                <div class="slabel">WINS</div>
            </div>
            <div class="divider"></div>
            <div class="score-item draws-item">
                <div class="number">{{ score.draws }}</div>
                <div class="slabel">DRAWS</div>
            </div>
            <div class="divider"></div>
            <div class="score-item loses-item">
                <div class="number">{{ score.losses }}</div>
                <div class="slabel">LOSSES</div>
            </div>
        </div>
    </div>

</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    player = None
    computer = None

    if request.method == 'POST':
        player = request.form['choice']
        computer = random.choice(['Rock', 'Paper', 'Scissors'])

        if player == computer:
            result = "It's a Draw! 🤝"
            score['draws'] += 1
        elif (player == 'Rock' and computer == 'Scissors') or \
             (player == 'Paper' and computer == 'Rock') or \
             (player == 'Scissors' and computer == 'Paper'):
            result = "You Win! 🎉"
            score['wins'] += 1
        else:
            result = "You Lose! 😢"
            score['losses'] += 1

    return render_template_string(HTML, result=result, player=player, computer=computer, score=score)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)