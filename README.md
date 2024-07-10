# Mancala Game

This project is a web-based implementation of the classic board game Mancala using Flask for the backend and plain HTML, CSS, and JavaScript for the frontend.

## How to Play Mancala

### Gameplay
1. One player will start the game by picking any pocket containing stones from their own side.
2. The player will remove all the stones from that pocket, and deposit one stone at a time into neighboring pockets going counter-clockwise until the stones run out.
3. If a player encounters their own store, a stone is deposited in it.
4. If there are enough stones to go past the player’s own store, stones are deposited continuing on the other side’s pockets. However, if they encounter the other player’s store, that store is skipped over.
5. If the last stone is deposited in the player’s own store, the player gets another turn.
6. If the last stone is placed in an empty pocket on the player’s own side, the player takes this stone as well as the other player’s stones across from the empty pocket landed in, and places them in their own store.

### Winning the Game
When all six pockets on one side are emptied the game ends. Each player will count the number of stones in their store. The player who has the most stones in their store wins.

## Project Setup

### Requirements
- Python 3.x
- Flask

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mancala-game.git
    cd mancala-game
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Flask application:
    ```sh
    python app.py
    ```

4. Open your web browser and navigate to `http://127.0.0.1:5000/` to start playing the game.