from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

score = {"wins": 0, "losses": 0, "draws": 0}

HTML = '''
<h1>🪨 Rock Paper Scissors ✂️</h1>
<form method="POST">
    <button name="choice" value="Rock">🪨 Rock</button>
    <button name="choice" value="Paper">📄 Paper</button>
    <button name="choice" value="Scissors">✂️ Scissors</button>
</form>

{% if result %}
<h2>You chose: {{ player }}</h2>
<h2>Computer chose: {{ computer }}</h2>
<h2>Result: {{ result }}</h2>
{% endif %}

<h3>Score:</h3>
<p>✅ Wins: {{ score.wins }} | ❌ Losses: {{ score.losses }} | 🤝 Draws: {{ score.draws }}</p>
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


