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
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: white;
            text-align: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 10px #e94560;
        }
        .buttons {
            margin: 30px;
        }
        button {
            font-size: 2em;
            margin: 10px;
            padding: 20px 30px;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: transform 0.2s;
            background: #e94560;
            color: white;
        }
        button:hover {
            transform: scale(1.2);
            background: #ff6b6b;
        }
        .result-box {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            margin: 20px auto;
            max-width: 400px;
        }
        .result-box h2 {
            font-size: 1.5em;
            margin: 10px;
        }
        .win { color: #2ecc71; font-size: 2em; font-weight: bold; }
        .lose { color: #e74c3c; font-size: 2em; font-weight: bold; }
        .draw { color: #f39c12; font-size: 2em; font-weight: bold; }
        .scoreboard {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            margin: 20px auto;
            max-width: 400px;
        }
        .scoreboard h3 { font-size: 1.8em; margin-bottom: 10px; }
        .scores {
            display: flex;
            justify-content: space-around;
            font-size: 1.3em;
        }
        .wins { color: #2ecc71; }
        .losses { color: #e74c3c; }
        .draws { color: #f39c12; }
    </style>
</head>
<body>
    <h1>🪨 Rock Paper Scissors ✂️</h1>
    <p style="font-size:1.2em; color:#aaa;">Choose your weapon!</p>

    <form method="POST" class="buttons">
        <button name="choice" value="Rock">🪨<br>Rock</button>
        <button name="choice" value="Paper">📄<br>Paper</button>
        <button name="choice" value="Scissors">✂️<br>Scissors</button>
    </form>

    {% if result %}
    <div class="result-box">
        <h2>You chose: <strong>{{ player }}</strong></h2>
        <h2>Computer chose: <strong>{{ computer }}</strong></h2>
        {% if "Win" in result %}
            <p class="win">{{ result }}</p>
        {% elif "Lose" in result %}
            <p class="lose">{{ result }}</p>
        {% else %}
            <p class="draw">{{ result }}</p>
        {% endif %}
    </div>
    {% endif %}

    <div class="scoreboard">
        <h3>🏆 Scoreboard</h3>
        <div class="scores">
            <div class="wins">✅ Wins<br>{{ score.wins }}</div>
            <div class="draws">🤝 Draws<br>{{ score.draws }}</div>
            <div class="losses">❌ Losses<br>{{ score.losses }}</div>
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