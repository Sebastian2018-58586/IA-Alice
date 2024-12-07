import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajedrez Pierde-Gana")
        self.root.configure(bg="black")  # Fondo negro para la ventana

        # Configurar tablero inicial y tablero de jugadas
        self.board1_state = self.create_initial_board()
        self.board2_state = self.create_empty_board()  # Tablero 2 vacío al inicio

        # Crear marcos para los tableros
        self.board1_frame = self.create_board_frame("Tablero 1 (Juego)")
        self.board2_frame = self.create_board_frame("Tablero 2 (Movimientos)")

        # Inicializar tableros gráficos
        self.initialize_boards()

        # Etiquetas informativas y botones
        self.info_label = tk.Label(
            root, text="Turno: Blancas", font=("Arial", 14), fg="white", bg="black"
        )
        self.info_label.pack(pady=10)

        self.reset_button = tk.Button(
            root, text="Reiniciar Juego", command=self.reset_game, bg="gray", fg="white"
        )
        self.reset_button.pack(pady=10)

    def create_initial_board(self):
        """Crea el estado inicial del tablero con las piezas."""
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
        """Crea un tablero vacío."""
        return [["."] * 8 for _ in range(8)]

    def create_board_frame(self, title):
        """Crea un marco para un tablero con título."""
        frame = tk.Frame(self.root, bg="black")
        frame.pack(side=tk.LEFT, padx=20, pady=20)
        label = tk.Label(frame, text=title, font=("Arial", 16), fg="white", bg="black")
        label.pack()
        board_canvas = tk.Canvas(frame, width=480, height=480, bg="black", highlightthickness=0)
        board_canvas.pack()
        return board_canvas

    def initialize_boards(self):
        """Inicializa los tableros gráficos."""
        self.draw_board(self.board1_frame, self.board1_state)
        self.draw_board(self.board2_frame, self.board2_state)

    def draw_board(self, canvas, board_state):
        """Dibuja el tablero y las piezas en el canvas."""
        square_size = 60
        for row in range(8):
            for col in range(8):
                # Alternar colores entre naranja claro y café claro
                color = "#FFCC99" if (row + col) % 2 == 0 else "#D2B48C"
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # Dibujar las piezas si existen
                piece = board_state[row][col]
                if piece != ".":
                    self.draw_piece(canvas, piece, x1, y1, square_size)

    def draw_piece(self, canvas, piece, x, y, size):
        """Dibuja una pieza en el tablero."""
        piece_symbols = {
            "p": "♟", "t": "♜", "c": "♞", "a": "♝", "d": "♛", "r": "♚",
            "P": "♙", "T": "♖", "C": "♘", "A": "♗", "D": "♕", "R": "♔",
        }
        color = "white" if piece.isupper() else "black"
        font_size = int(size * 0.6)
        canvas.create_text(
            x + size / 2, y + size / 2, text=piece_symbols[piece], fill=color, font=("Arial", font_size)
        )

    def reset_game(self):
        """Reinicia el juego."""
        self.board1_state = self.create_initial_board()
        self.board2_state = self.create_empty_board()
        self.initialize_boards()

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
