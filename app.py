from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player1_name = request.form.get('player1_name', 'Player 1')
    player2_name = request.form.get('player2_name', 'Player 2')
    game_state = {
        'board': [4] * 6 + [0] + [4] * 6 + [0],
        'current_player': 1,
        'player1_name': player1_name,
        'player2_name': player2_name
    }
    return jsonify(game_state)

@app.route('/make_move', methods=['POST'])
def make_move():
    game_state = request.json
    board = game_state['board']
    current_player = game_state['current_player']
    index = game_state['index']
    
    # Handle move logic
    if (current_player == 1 and (index > 5 or index == 6)) or (current_player == 2 and (index < 7 or index == 13)):
        return jsonify(game_state)

    stones = board[index]
    board[index] = 0
    pos = index

    while stones > 0:
        pos = (pos + 1) % 14
        if (current_player == 1 and pos == 13) or (current_player == 2 and pos == 6):
            continue
        board[pos] += 1
        stones -= 1

    if (current_player == 1 and pos == 6) or (current_player == 2 and pos == 13):
        game_state['board'] = board
        return jsonify(game_state)

    if current_player == 1 and 0 <= pos < 6 and board[pos] == 1:
        opposite_pos = 12 - pos
        board[6] += board[opposite_pos] + 1
        board[pos] = board[opposite_pos] = 0
    elif current_player == 2 and 7 <= pos < 13 and board[pos] == 1:
        opposite_pos = 12 - pos
        board[13] += board[opposite_pos] + 1
        board[pos] = board[opposite_pos] = 0

    game_state['current_player'] = 2 if current_player == 1 else 1
    game_state['board'] = board

    # Check if the game is over
    if all(stone == 0 for stone in board[:6]) or all(stone == 0 for stone in board[7:13]):
        for i in range(6):
            board[6] += board[i]
            board[i] = 0
        for i in range(7, 13):
            board[13] += board[i]
            board[i] = 0
        game_state['board'] = board

        # Determine the winner
        if board[6] > board[13]:
            winner = game_state['player1_name']
        elif board[6] < board[13]:
            winner = game_state['player2_name']
        else:
            winner = "No one, it's a tie"
        game_state['winner'] = winner

    return jsonify(game_state)

if __name__ == "__main__":
    app.run(debug=True)
