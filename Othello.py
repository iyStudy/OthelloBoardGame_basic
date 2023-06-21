import numpy as np
import tkinter as tk
from tkinter import messagebox

# 定数の定義
BOARD_SIZE = 8
PLAYER_BLACK = 1
PLAYER_WHITE = -1
EMPTY = 0
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, -1)]


class OthelloBoard:
    def __init__(self):
        # オセロ盤の初期化。中央に2つずつの石がある
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.board[3, 3] = PLAYER_WHITE
        self.board[3, 4] = PLAYER_BLACK
        self.board[4, 3] = PLAYER_BLACK
        self.board[4, 4] = PLAYER_WHITE
    
    def is_valid_move(self, player, x, y):
        # 選択した位置に石を置けるかどうか判定
        if self.board[x, y] != EMPTY:
            return False, []

        to_flip = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            temp_flip = []
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx, ny] == -player:
                temp_flip.append((nx, ny))
                nx, ny = nx + dx, ny + dy

            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx, ny] == player:
                to_flip.extend(temp_flip)

        return len(to_flip) > 0, to_flip

    def make_move(self, player, x, y):
        # 石を置く
        valid, positions_to_flip = self.is_valid_move(player, x, y)
        if valid:
            self.board[x, y] = player
            for x, y in positions_to_flip:
                self.board[x, y] = player

    def get_valid_moves(self, player):
        # すべての有効な移動をリストとして返す
        valid_moves = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.is_valid_move(player, x, y)[0]:
                    valid_moves.append((x, y))
        return valid_moves

    def get_board_state(self):
        # 盤面の現在の状態を返す
        return self.board.copy()


class OthelloGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Othello")
        self.geometry("400x430")
        self.board = OthelloBoard()
        self.player = PLAYER_BLACK

        # GUIにプレイヤーのターンを表示するラベルを追加
        self.label = tk.Label(self, text="", font=("Helvetica", 16))
        self.label.pack()

        # GUIにボタンを配置するためのフレームを作成
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        # ボタンのリストを作成
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # ボタンをグリッド内に配置
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # ボタンが押された時にon_clickメソッドを呼ぶように設定
                b = tk.Button(self.button_frame, width=5, height=2, command=lambda x=x, y=y: self.on_click(x, y))
                b.grid(row=x, column=y)
                self.buttons[x][y] = b

        # GUI上のボタンを更新
        self.update_buttons()

    def on_click(self, x, y):
        # ボタンがクリックされた時の処理
        valid, positions_to_flip = self.board.is_valid_move(self.player, x, y)
        if valid:
            self.board.make_move(self.player, x, y)
            self.player = -self.player
            self.update_buttons()

            # ゲームが終了したかをチェック
            if not any(self.board.get_valid_moves(self.player)):
                messagebox.showinfo("Game Over", "Game Over")
                self.destroy()

    def update_buttons(self):
        # GUI上のボタンとラベルを更新
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                state = self.board.get_board_state()[x, y]
                text = ""
                if state == PLAYER_BLACK:
                    text = "B"
                elif state == PLAYER_WHITE:
                    text = "W"
                self.buttons[x][y].config(text=text)

        # ターンのラベルを更新
        turn = "Black" if self.player == PLAYER_BLACK else "White"
        self.label.config(text=f"Turn: {turn}")


if __name__ == "__main__":
    # プログラムを実行し、GUIを表示
    app = OthelloGUI()
    app.mainloop()
