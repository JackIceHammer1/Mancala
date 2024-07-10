import tkinter as tk
from tkinter import messagebox

class MancalaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala Game")
        self.root.geometry("1000x400")

        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.current_player = 1

        # Create the input screen for player names
        self.create_name_input_screen()

    def create_name_input_screen(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Player 1's Name:").pack()
        self.player1_entry = tk.Entry(self.root)
        self.player1_entry.pack()

        tk.Label(self.root, text="Enter Player 2's Name:").pack()
        self.player2_entry = tk.Entry(self.root)
        self.player2_entry.pack()

        tk.Button(self.root, text="Submit", command=self.start_instructions_screen).pack()

    def start_instructions_screen(self):
        self.player1_name = self.player1_entry.get() or "Player 1"
        self.player2_name = self.player2_entry.get() or "Player 2"

        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        instructions = (
            "Welcome to Mancala!\n\n"
            "Objective: Collect as many stones as possible in your store.\n"
            "Player 1's store is on the left, and Player 2's store is on the right.\n\n"
            "On your turn, click on one of your pits to distribute its stones counter-clockwise.\n"
            "If the last stone lands in your store, you get another turn.\n"
            "If the last stone lands in an empty pit on your side, you capture the stones in the opposite pit.\n\n"
            "The game ends when all pits on one side are empty.\n"
            "The player with the most stones in their store wins!\n\n"
            "Click 'Start Game' to begin."
        )

        tk.Label(self.root, text=instructions, wraplength=800, justify="left").pack(pady=20)
        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize the game board
        self.board = [4] * 14
        self.board[6] = 0  # Player 1's store
        self.board[13] = 0  # Player 2's store

        # Setup the canvas for drawing the board
        self.canvas = tk.Canvas(self.root, width=1000, height=400, bg="saddlebrown")
        self.canvas.pack()

        # Text bar to display which player's turn it is
        self.turn_text = self.canvas.create_text(500, 20, text=f"{self.player1_name}'s Turn", font=("Arial", 18, "bold"), fill="white")

        # Create and update the game board
        self.create_board()
        self.update_board()

    def create_board(self):
        # Initialize lists to store pits and stones
        self.pits = []

        # Create Player 1's store
        self.pits.append(self.canvas.create_oval(50, 100, 150, 300, fill="white", outline="black", tags="pit6"))

        # Create Player 2's store
        self.pits.append(self.canvas.create_oval(850, 100, 950, 300, fill="white", outline="black", tags="pit13"))

        # Create Player 1's pits
        for i in range(6):
            x1 = 200 + i * 100
            y1 = 250
            x2 = x1 + 75
            y2 = y1 + 75
            pit = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", tags=f"pit{i}")
            self.pits.append(pit)

        # Create Player 2's pits
        for i in range(6):
            x1 = 200 + (5 - i) * 100
            y1 = 50
            x2 = x1 + 75
            y2 = y1 + 75
            pit = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", tags=f"pit{i+7}")
            self.pits.append(pit)

        # Bind click events to pits
        for i in range(14):
            self.canvas.tag_bind(f"pit{i}", "<Button-1>", lambda event, i=i: self.make_move(i))

    def update_board(self):
        # Clear existing text and stones
        self.canvas.delete("text")
        self.canvas.delete("stone")
        for i in range(14):
            x1, y1, x2, y2 = self.canvas.coords(self.pits[i])
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            # Display number of stones in each pit
            self.canvas.create_text(cx, cy, text=str(self.board[i]), tags="text", font=("Arial", 18, "bold"))

            # Draw stones
            if self.board[i] > 0:
                for j in range(self.board[i]):
                    stone_x = x1 + 15 + (j % 4) * 15
                    stone_y = y1 + 15 + (j // 4) * 15
                    self.canvas.create_oval(stone_x, stone_y, stone_x + 10, stone_y + 10, fill="black", tags="stone")

        # Update the turn text
        current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
        self.canvas.itemconfig(self.turn_text, text=f"{current_player_name}'s Turn")

    def make_move(self, index):
        if (self.current_player == 1 and index > 5) or (self.current_player == 2 and index < 7):
            return

        stones = self.board[index]
        self.board[index] = 0
        pos = index

        while stones > 0:
            pos = (pos + 1) % 14
            if (self.current_player == 1 and pos == 13) or (self.current_player == 2 and pos == 6):
                continue
            self.board[pos] += 1
            stones -= 1

        # Check if the last stone lands in the player's store
        if (self.current_player == 1 and pos == 6) or (self.current_player == 2 and pos == 13):
            self.update_board()
            return

        # Capture opponent's stones if last stone lands in an empty pit on player's side
        if self.current_player == 1 and 0 <= pos < 6 and self.board[pos] == 1 or self.current_player == 2 and 7 <= pos < 13 and self.board[pos] == 1:
            opposite_pos = 12 - pos
            self.board[6 if self.current_player == 1 else 13] += self.board[opposite_pos] + 1
            self.board[pos] = self.board[opposite_pos] = 0

        # Switch the current player
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_board()

        # Check if the game is over
        if self.check_game_over():
            self.end_game()

    def check_game_over(self):
        return all(stone == 0 for stone in self.board[:6]) or all(stone == 0 for stone in self.board[7:13])

    def end_game(self):
        # Move remaining stones to players' stores
        for i in range(6):
            self.board[6] += self.board[i]
            self.board[i] = 0
        for i in range(7, 13):
            self.board[13] += self.board[i]
            self.board[i] = 0

        self.update_board()

        # Determine the winner
        if self.board[6] > self.board[13]:
            winner = self.player1_name
        elif self.board[6] < self.board[13]:
            winner = self.player2_name
        else:
            winner = "No one, it's a tie"

        # Display the winner and end the game
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MancalaGame(root)
    root.mainloop()
