import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
"FUNCIONA EL CLICK EN EL 2DO TABLERO"
class ChessGUI:
    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("Ajedrez Pierde-Gana")  # Título de la ventana
        self.root.configure(bg="black")  # Fondo negro para la ventana principal

        # Configurar el estado inicial de los tableros
        self.board1_state = self.create_initial_board()  # Tablero 1 con la posición inicial de las piezas
        self.board2_state = self.create_empty_board()  # Tablero 2 vacío al inicio

        # Inicializamos el atributo selected_piece como None
        self.selected_piece = None  # Este atributo se usará para almacenar la pieza seleccionada

        # Crear y configurar los marcos para ambos tableros
        self.board1_frame = self.create_board_frame("Tablero 1 (Juego)")  # Tablero principal
        self.board2_frame = self.create_board_frame("Tablero 2 (Movimientos)")  # Tablero secundario

        # Dibujar los tableros gráficos
        self.initialize_boards()

        # Crear una etiqueta informativa para mostrar el turno
        self.info_label = tk.Label(
            root, text="Turno: Blancas", font=("Arial", 14), fg="white", bg="black"
        )
        self.info_label.pack(pady=10)  # Espaciado vertical

        # Botón para reiniciar el juego
        self.reset_button = tk.Button(
            root, text="Reiniciar Juego", command=self.reset_game, bg="gray", fg="white"
        )
        self.reset_button.pack(pady=10)

    def create_initial_board(self):
        """Crea el estado inicial del tablero con las piezas en sus posiciones iniciales."""
        return [
            ["t", "c", "a", "d", "r", "a", "c", "t"],  # Fila 1: Piezas negras
            ["p"] * 8,  # Fila 2: Peones negros
            ["."] * 8,  # Filas vacías
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["P"] * 8,  # Fila 7: Peones blancos
            ["T", "C", "A", "D", "R", "A", "C", "T"]   # Fila 8: Piezas blancas
        ]

    def create_empty_board(self):
        """Crea un tablero vacío."""
        return [["."] * 8 for _ in range(8)]  # 8x8 con casillas vacías

    def create_board_frame(self, title):
        """Crea un marco que contiene un tablero gráfico y su título."""
        frame = tk.Frame(self.root, bg="black")  # Marco con fondo negro
        frame.pack(side=tk.LEFT, padx=20, pady=20)  # Espaciado entre marcos
        
        # Etiqueta del título del tablero
        label = tk.Label(frame, text=title, font=("Arial", 16), fg="white", bg="black")
        label.pack()

        # Canvas para dibujar el tablero
        board_canvas = tk.Canvas(frame, width=480, height=480, bg="black", highlightthickness=0)
        board_canvas.pack()
        return board_canvas

    def initialize_boards(self):
        """Dibuja los tableros iniciales en sus respectivos marcos."""
        self.draw_board(self.board1_frame, self.board1_state)  # Dibuja Tablero 1
        self.draw_board(self.board2_frame, self.board2_state)  # Dibuja Tablero 2

    def draw_board(self, canvas, board_state):
        """Dibuja un tablero y sus piezas en un canvas."""
        square_size = 60  # Tamaño de cada casilla
        for row in range(8):
            for col in range(8):
                # Alternar colores entre naranja claro y café claro para las casillas
                color = "#FFCC99" if (row + col) % 2 == 0 else "#D2B48C"
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                
                # Dibuja la casilla
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # Asocia el evento de clic a cada casilla
                canvas.tag_bind(
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=""),
                    "<Button-1>", lambda event, r=row, c=col: self.on_square_click(event, r, c)
                )

                # Dibujar la pieza si existe en la posición actual
                piece = board_state[row][col]
                if piece != ".":
                    self.draw_piece(canvas, piece, x1, y1, square_size)

    def draw_piece(self, canvas, piece, x, y, size):
        """Dibuja una pieza en una posición específica del tablero."""
        piece_symbols = {
            "p": "♟", "t": "♜", "c": "♞", "a": "♝", "d": "♛", "r": "♚",  # Negras
            "P": "♙", "T": "♖", "C": "♘", "A": "♗", "D": "♕", "R": "♔"   # Blancas
        }
        color = "white" if piece.isupper() else "black"  # Determina el color según la pieza
        font_size = int(size * 0.6)  # Calcula el tamaño de la fuente relativo al tamaño de la casilla
        canvas.create_text(
            x + size / 2, y + size / 2, text=piece_symbols[piece], fill=color, font=("Arial", font_size)
        )

    def reset_game(self):
        """Reinicia los tableros al estado inicial.""" 
        self.board1_state = self.create_initial_board()  # Reinicia Tablero 1
        self.board2_state = self.create_empty_board()  # Reinicia Tablero 2
        self.selected_piece = None  # Reinicia la selección de la pieza
        self.initialize_boards()  # Redibuja los tableros

    def on_square_click(self, event, row, col):
        """Maneja los clics en las casillas del tablero."""
        if self.selected_piece is None:
            # Seleccionamos una pieza si la casilla contiene una pieza
            piece = self.board1_state[row][col]
            if piece != ".":
                self.selected_piece = (row, col)  # Guardamos la pieza seleccionada
                # Aquí podemos resaltar la pieza seleccionada si lo deseas
                print(f"Seleccionaste la pieza {piece} en la casilla ({row}, {col})")
            else:
                print("Haz clic en una casilla con una pieza")
        else:
            # Movemos la pieza seleccionada a la nueva casilla
            from_row, from_col = self.selected_piece
            piece = self.board1_state[from_row][from_col]  # Pieza seleccionada
            
            if self.is_valid_move(piece, from_row, from_col, row, col):
                # Realiza el movimiento (cambia el estado del tablero)
                self.board1_state[row][col] = piece
                self.board1_state[from_row][from_col] = "."  # Vacía la casilla original
                self.selected_piece = None  # Deselecciona la pieza
                self.initialize_boards()  # Redibuja los tableros para reflejar el movimiento
                print(f"Moviste la pieza {piece} de ({from_row}, {from_col}) a ({row}, {col})")
            else:
                print(f"Movimiento no válido para la pieza {piece}")

    def is_valid_move(self, piece, from_row, from_col, to_row, to_col):
        """Valida si el movimiento de una pieza es legal (para simplificación, comenzamos con peones)."""
        if piece == "P":  # Peón blanco
            if from_col == to_col and from_row - 1 == to_row and self.board1_state[to_row][to_col] == ".":
                return True  # Movimiento hacia adelante de una casilla
            elif from_col == to_col and from_row == 6 and to_row == 4 and self.board1_state[to_row][to_col] == ".":
                return True  # Movimiento hacia adelante de dos casillas (solo al inicio)
            elif abs(from_col - to_col) == 1 and from_row - 1 == to_row and self.board1_state[to_row][to_col].islower():
                return True  # Captura en diagonal
        elif piece == "p":  # Peón negro
            if from_col == to_col and from_row + 1 == to_row and self.board1_state[to_row][to_col] == ".":
                return True  # Movimiento hacia adelante de una casilla
            elif from_col == to_col and from_row == 1 and to_row == 3 and self.board1_state[to_row][to_col] == ".":
                return True  # Movimiento hacia adelante de dos casillas (solo al inicio)
            elif abs(from_col - to_col) == 1 and from_row + 1 == to_row and self.board1_state[to_row][to_col].isupper():
                return True  # Captura en diagonal

        # Lógica adicional para otras piezas vendrá después
        return False

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()  # Inicializa la ventana principal
    app = ChessGUI(root)  # Crea una instancia de la interfaz gráfica
    root.mainloop()  # Inicia el bucle principal de la interfaz
