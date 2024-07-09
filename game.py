import tkinter as tk

class MancalaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala Game")
        self.root.geometry("1000x400")
        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=400, bg="saddlebrown")
        self.canvas.pack()
        # Draw Player 1's store
        self.canvas.create_oval(50, 100, 150, 300, fill="white", outline="black")
        # Draw Player 2's store
        self.canvas.create_oval(850, 100, 950, 300, fill="white", outline="black")
        # Draw Player 1's pits
        for i in range(6):
            x1 = 200 + i * 100
            y1 = 250
            x2 = x1 + 75
            y2 = y1 + 75
            self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
        # Draw Player 2's pits
        for i in range(6):
            x1 = 200 + (5 - i) * 100
            y1 = 50
            x2 = x1 + 75
            y2 = y1 + 75
            self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")

if __name__ == "__main__":
    root = tk.Tk()
    game = MancalaGame(root)
    root.mainloop()
