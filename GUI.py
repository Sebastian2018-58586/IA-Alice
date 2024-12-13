import tkinter as tk 
from PIL import Image, ImageDraw, ImageTk

class ChessGUI:
    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("Ajedrez Pierde-Gana")
        self.root.configure(bg="black")

        # Configurar el estado inicial de los tableros
        self.board1_state = self.create_initial_board()
        self.board2_state = self.create_empty_board()

        # Inicializamos el atributo selected_piece como None
        self.selected_piece = None

        # Crear y configurar los marcos para ambos tableros
        self.board1_frame = self.create_board_frame("Tablero 1 (Juego)")
        self.board2_frame = self.create_board_frame("Tablero 2 (Movimientos)")

        # Dibujar los tableros gráficos
        self.initialize_boards()

        # Crear una etiqueta informativa para mostrar el turno
        self.info_label = tk.Label(
            root, text="Turno: Blancas", font=("Arial", 14), fg="white", bg="black"
        )
        self.info_label.pack(pady=10)

        # Crear etiqueta de error para mostrar los mensajes de error
        self.error_label = tk.Label(
            root, text="", font=("Arial", 12), fg="red", bg="black"
        )
        self.error_label.pack(pady=10)

        # Botón para reiniciar el juego
        self.reset_button = tk.Button(
            root, text="Reiniciar Juego", command=self.reset_game, bg="gray", fg="white"
        )
        self.reset_button.pack(pady=10)

    def create_initial_board(self):
        return [
            ["t", "c", "a", "d", "r", "a", "c", "t"],
            ["p"] * 8,
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["P"] * 8,
            ["T", "C", "A", "D", "R", "A", "C", "T"]
        ]

    def create_empty_board(self):
        return [["."] * 8 for _ in range(8)]

    def create_board_frame(self, title):
        frame = tk.Frame(self.root, bg="black")
        frame.pack(side=tk.LEFT, padx=20, pady=20)
        label = tk.Label(frame, text=title, font=("Arial", 16), fg="white", bg="black")
        label.pack()
        board_canvas = tk.Canvas(frame, width=480, height=480, bg="black", highlightthickness=0)
        board_canvas.pack()
        return board_canvas

    def initialize_boards(self):
        self.draw_board(self.board1_frame, self.board1_state)
        self.draw_board(self.board2_frame, self.board2_state)

    def draw_board(self, canvas, board_state):
        square_size = 60
        for row in range(8):
            for col in range(8):
                color = "#FFCC99" if (row + col) % 2 == 0 else "#D2B48C"
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                canvas.tag_bind(
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=""),
                    "<Button-1>", lambda event, r=row, c=col: self.on_square_click(event, r, c)
                )
                piece = board_state[row][col]
                if piece != ".":
                    self.draw_piece(canvas, piece, x1, y1, square_size)

    def draw_piece(self, canvas, piece, x, y, size):
        piece_symbols = {
            "p": "♟", "t": "♜", "c": "♞", "a": "♝", "d": "♛", "r": "♚",
            "P": "♙", "T": "♖", "C": "♘", "A": "♗", "D": "♕", "R": "♔"
        }
        color = "white" if piece.isupper() else "black"
        font_size = int(size * 0.6)
        canvas.create_text(
            x + size / 2, y + size / 2, text=piece_symbols[piece], fill=color, font=("Arial", font_size)
        )

    def reset_game(self):
        self.board1_state = self.create_initial_board()
        self.board2_state = self.create_empty_board()
        self.selected_piece = None
        self.error_label.config(text="")
        self.initialize_boards()

    def on_square_click(self, event, row, col):
        if self.selected_piece is None:
            piece = self.board1_state[row][col]
            if piece != ".":
                self.selected_piece = (row, col)
                print(f"Seleccionaste la pieza {piece} en la casilla ({row}, {col})")
            else:
                self.show_error("Haz clic en una casilla con una pieza")
        else:
            from_row, from_col = self.selected_piece
            piece = self.board1_state[from_row][from_col]
            if self.is_valid_move(piece, from_row, from_col, row, col):
                self.board1_state[row][col] = piece
                self.board1_state[from_row][from_col] = "."
                self.board2_state[7 - row][7 - col] = piece
                self.board2_state[7 - from_row][7 - from_col] = "."
                self.selected_piece = None
                self.initialize_boards()
                print(f"Moviste la pieza {piece} de ({from_row}, {from_col}) a ({row}, {col})")
            else:
                self.show_error(f"Movimiento no válido para la pieza {piece}")

    def show_error(self, message):
        self.error_label.config(text=message)

    def is_valid_move(self, piece, from_row, from_col, to_row, to_col):
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        target_piece = self.board1_state[to_row][to_col]
        if piece.isupper() and target_piece.isupper():
            return False
        if piece.islower() and target_piece.islower():
            return False

        mirror_row, mirror_col = 7 - to_row, 7 - to_col
        if self.board2_state[mirror_row][mirror_col] != ".":
            self.show_error("No puedes mover aquí porque la casilla espejo está ocupada")
            return False

        return True

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
