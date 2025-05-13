import tkinter as tk
from tkinter import messagebox
from game import TicTacToe
from player import Player, AIPlayer

class BoardGUI:
    def __init__(self, root):
        self.root = root
        self.game = None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = None
        self.score_label = None
        self.scores = {"Player 1": 0, "Player 2": 0, "AI": 0, "Draws": 0}
        self.player1 = None
        self.player2 = None
        self.setup_mode_selection()

    def setup_mode_selection(self):
        self.clear_window()
        label = tk.Label(self.root, text="Choose Game Mode", font=('Arial', 20))
        label.pack(pady=10)

        pvp_btn = tk.Button(self.root, text="Player vs Player", font=('Arial', 16), width=20, command=self.start_pvp)
        pvp_btn.pack(pady=5)

        ai_btn = tk.Button(self.root, text="Player vs AI", font=('Arial', 16), width=20, command=self.setup_ai_difficulty)
        ai_btn.pack(pady=5)

    def setup_ai_difficulty(self):
        self.clear_window()
        label = tk.Label(self.root, text="Select AI Difficulty", font=('Arial', 20))
        label.pack(pady=10)

        easy_btn = tk.Button(self.root, text="Easy", font=('Arial', 16), width=20, command=lambda: self.start_ai('easy'))
        easy_btn.pack(pady=5)

        hard_btn = tk.Button(self.root, text="Hard", font=('Arial', 16), width=20, command=lambda: self.start_ai('hard'))
        hard_btn.pack(pady=5)

    def start_pvp(self):
        self.player1 = Player('X', 'Player 1')
        self.player2 = Player('O', 'Player 2')
        self.start_game(self.player1, self.player2)

    def start_ai(self, difficulty):
        self.player1 = Player('X', 'Player 1')
        self.player2 = AIPlayer('O', 'AI', difficulty)
        self.start_game(self.player1, self.player2)

    def start_game(self, player1, player2):
        self.clear_window()
        self.game = TicTacToe(player1, player2)
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=('Arial', 16))
        self.score_label.grid(row=0, column=0, columnspan=3, pady=(5, 0))
        self.status_label = tk.Label(self.root, text=self.get_status_text(), font=('Arial', 20))
        self.status_label.grid(row=1, column=0, columnspan=3)
        self.create_interface()
        self.root.after(100, self.ai_move_if_needed)  # In case AI starts

    def create_interface(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i+2, column=j)  # Start from row 2 to leave space for labels
                self.buttons[i][j] = btn

    def on_click(self, i, j):
        if isinstance(self.game.current_player, AIPlayer):
            return  # Prevent clicking during AI's turn
        result = self.game.make_move(i, j)
        self.buttons[i][j]['text'] = self.game.board[i][j]
        if result:
            self.update_score(result)
            self.show_end_dialog(result)
        else:
            self.status_label.config(text=self.get_status_text())
            self.root.after(100, self.ai_move_if_needed)

    def ai_move_if_needed(self):
        if isinstance(self.game.current_player, AIPlayer):
            move = self.game.current_player.get_move(self.game.board)
            if move:
                result = self.game.make_move(*move)
                self.buttons[move[0]][move[1]]['text'] = self.game.board[move[0]][move[1]]
                if result:
                    self.update_score(result)
                    self.show_end_dialog(result)
                else:
                    self.status_label.config(text=self.get_status_text())

    def get_status_text(self):
        player = self.game.current_player
        return f"{player.name}'s turn ({player.symbol})"

    def get_score_text(self):
        if isinstance(self.player2, AIPlayer):
            return f"Player 1: {self.scores['Player 1']}   AI: {self.scores['AI']}   Draws: {self.scores['Draws']}"
        else:
            return f"Player 1: {self.scores['Player 1']}   Player 2: {self.scores['Player 2']}   Draws: {self.scores['Draws']}"

    def update_score(self, result):
        if "Player 1" in result:
            self.scores["Player 1"] += 1
        elif "Player 2" in result:
            self.scores["Player 2"] += 1
        elif "AI" in result:
            self.scores["AI"] += 1
        elif "Draw" in result:
            self.scores["Draws"] += 1
        if self.score_label:
            self.score_label.config(text=self.get_score_text())

    def show_end_dialog(self, result):
        dialog = tk.Toplevel(self.root)
        dialog.title("Game Over")
        dialog.grab_set()  # Make this window modal

        label = tk.Label(dialog, text=f"{result}\n\nWhat do you want to do?", font=('Arial', 16))
        label.pack(padx=20, pady=10)

        def play_again():
            dialog.destroy()
            self.start_game(self.player1, self.player2)

        def main_menu():
            dialog.destroy()
            self.scores = {"Player 1": 0, "Player 2": 0, "AI": 0, "Draws": 0}
            self.setup_mode_selection()

        def exit_game():
            self.root.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        play_again_btn = tk.Button(btn_frame, text="Play Again", width=12, command=play_again)
        play_again_btn.grid(row=0, column=0, padx=5)

        main_menu_btn = tk.Button(btn_frame, text="Main Menu", width=12, command=main_menu)
        main_menu_btn.grid(row=0, column=1, padx=5)

        exit_btn = tk.Button(btn_frame, text="Exit", width=12, command=exit_game)
        exit_btn.grid(row=0, column=2, padx=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()