import tkinter as tk
from tkinter import messagebox

class MancalaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala Game")
        self.root.geometry("1000x400")
        self.board = [4] * 14
        self.board[6] = 0
        self.board[13] = 0
        self.current_player = 1
        self.create_board()
        self.update_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=400, bg="saddlebrown")
        self.canvas.pack()
        self.pits = []
        self.pits.append(self.canvas.create_oval(50, 100, 150, 300, fill="white", outline="black"))
        self.pits.append(self.canvas.create_oval(850, 100, 950, 300, fill="white", outline="black"))
        for i in range(6):
            x1 = 200 + i * 100
            y1 = 250
            x2 = x1 + 75
            y2 = y1 + 75
            pit = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
            self.pits.append(pit)
            self.canvas.tag_bind(pit, "<Button-1>", lambda event, i=i: self.make_move(i))
        for i in range(6):
            x1 = 200 + (5 - i) * 100
            y1 = 50
            x2 = x1 + 75
            y2 = y1 + 75
            pit = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
            self.pits.append(pit)
            self.canvas.tag_bind(pit, "<Button-1>", lambda event, i=i+7: self.make_move(i))

    def update_board(self):
        self.canvas.delete("text")
        for i in range(14):
            x1, y1, x2, y2 = self.canvas.coords(self.pits[i])
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(cx, cy, text=str(self.board[i]), font=("Arial", 18, "bold"), tags="text")

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
        if (self.current_player == 1 and pos == 6) or (self.current_player == 2 and pos == 13):
            self.update_board()
            return
        if self.current_player == 1 and 0 <= pos < 6 and self.board[pos] == 1 or self.current_player == 2 and 7 <= pos < 13 and self.board[pos] == 1:
            opposite_pos = 12 - pos
            self.board[6 if self.current_player == 1 else 13] += self.board[opposite_pos] + 1
            self.board[pos] = self.board[opposite_pos] = 0
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_board()
        if self.check_game_over():
            self.end_game()

    def check_game_over(self):
        return all(stone == 0 for stone in self.board[:6]) or all(stone == 0 for stone in self.board[7:13])

    def end_game(self):
        for i in range(6):
            self.board[6] += self.board[i]
            self.board[13] += self.board[i + 7]
            self.board[i] = self.board[i + 7] = 0
        self.update_board()
        winner = "Player 1" if self.board[6] > self.board[13] else "Player 2" if self.board[13] > self.board[6] else "No one"
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")

if __name__ == "__main__":
    root = tk.Tk()
    game = MancalaGame(root)
    root.mainloop()
