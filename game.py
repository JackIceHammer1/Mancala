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

if __name__ == "__main__":
    root = tk.Tk()
    game = MancalaGame(root)
    root.mainloop()
