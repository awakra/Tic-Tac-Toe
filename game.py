from player import Player, AIPlayer

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.players = [player1, player2]
        self.current_player_index = 0

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def make_move(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player.symbol
            if self.check_winner():
                return f'{self.current_player.name} ({self.current_player.symbol}) wins!'
            elif self.check_draw():
                return 'Draw!'
            self.current_player_index = 1 - self.current_player_index
            return None
        return 'Invalid move'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))