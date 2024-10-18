import tkinter as tk
from tkinter import messagebox

# Constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x320")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.reset_game()

    def reset_game(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        colors = ['#FFDDC1', '#FFABAB', '#FFC3A0']
        for row in range(3):
            for col in range(3):
                color = colors[(row * 3 + col) % len(colors)]
                button = tk.Button(self.root, text=EMPTY, font=('Arial', 40, 'bold'), width=5, height=2,
                                  bg=color, fg='black', command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row+1, column=col, padx=5, pady=5, sticky="nsew")
                self.root.grid_rowconfigure(row+1, weight=1)
                self.root.grid_columnconfigure(col, weight=1)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.board[row][col] == EMPTY and self.current_player == PLAYER_X:
            self.board[row][col] = PLAYER_X
            self.buttons[row][col].config(text=PLAYER_X, fg='blue')
            if self.check_winner(PLAYER_X):
                messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = PLAYER_O
                self.ai_move()

    def ai_move(self):
        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            self.board[row][col] = PLAYER_O
            self.buttons[row][col].config(text=PLAYER_O, fg='red')
            if self.check_winner(PLAYER_O):
                messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = PLAYER_X

    def find_best_move(self):
        best_val = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == EMPTY:
                    self.board[row][col] = PLAYER_O
                    move_val = self.minimax(0, False)
                    self.board[row][col] = EMPTY
                    if move_val > best_val:
                        best_move = (row, col)
                        best_val = move_val
        return best_move

    def minimax(self, depth, is_max):
        if self.check_winner(PLAYER_O):
            return 10
        if self.check_winner(PLAYER_X):
            return -10
        if self.check_draw():
            return 0

        if is_max:
            best = -float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = PLAYER_O
                        best = max(best, self.minimax(depth + 1, not is_max))
                        self.board[row][col] = EMPTY
            return best
        else:
            best = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = PLAYER_X
                        best = min(best, self.minimax(depth + 1, not is_max))
                        self.board[row][col] = EMPTY
            return best

    def check_winner(self, player):
        win_conditions = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[2][0], self.board[1][1], self.board[0][2]]
        ]
        return [player, player, player] in win_conditions

    def check_draw(self):
        return all(cell != EMPTY for row in self.board for cell in row)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
