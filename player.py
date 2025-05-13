import random

class Player:
    def __init__(self, symbol, name="Player"):
        self.symbol = symbol
        self.name = name

    def get_move(self, board):
        # Human move is handled by GUI, so nothing here
        pass

class AIPlayer(Player):
    def __init__(self, symbol, name="AI", difficulty="easy"):
        super().__init__(symbol, name)
        self.difficulty = difficulty

    def get_move(self, board):
        if self.difficulty == "easy":
            return self.random_move(board)
        elif self.difficulty == "hard":
            return self.minimax_move(board)
        else:
            return self.random_move(board)

    def random_move(self, board):
        empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
        return random.choice(empty) if empty else None

    def minimax_move(self, board):
        # Minimax implementation for hard AI
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = self.symbol
                    score = self.minimax(board, False, self.symbol)
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, is_maximizing, ai_symbol):
        opponent = 'O' if ai_symbol == 'X' else 'X'
        winner = self.check_winner(board)
        if winner == ai_symbol:
            return 1
        elif winner == opponent:
            return -1
        elif all(board[i][j] != '' for i in range(3) for j in range(3)):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = ai_symbol
                        score = self.minimax(board, False, ai_symbol)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = opponent
                        score = self.minimax(board, True, ai_symbol)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        # Check rows, columns, diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        return None