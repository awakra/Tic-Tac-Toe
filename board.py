from game import TicTacToe
from tkinter import messagebox
import tkinter as tk

class BoardGUI:
    def __init__(self, root):
        self.game = TicTacToe()
        self.root = root
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_interface()

    def create_interface(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, i, j):
        result = self.game.make_move(i, j)
        self.buttons[i][j]['text'] = self.game.board[i][j]
        if result:
            messagebox.showinfo('Game Over', result)
            self.root.destroy()
