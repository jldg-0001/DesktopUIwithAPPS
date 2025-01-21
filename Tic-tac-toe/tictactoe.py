import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def main_page():
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def go_to_fillup_form():
        homepage_frame.pack_forget()
        player_entry_frame.pack(pady=50)

    def go_back_to_homepage():
        board_frame.pack_forget()
        label.pack_forget()
        restart_button.pack_forget()
        back_button.pack_forget()
        exit_button_game.pack_forget()
        homepage_frame.pack(fill="both", expand=True)

    def start_game():
        player1_name = player1_entry.get()
        player2_name = player2_entry.get()

        if not player1_name:
            messagebox.showerror("Error", "Please enter Player 1's name.")
            return
        if not player2_name:
            messagebox.showerror("Error", "Please enter Player 2's name.")
            return

        player1_symbol = player1_symbol_var.get()
        player2_symbol = player2_symbol_var.get()

        if player1_symbol == player2_symbol:
            messagebox.showerror("Error", "Players cannot choose the same symbol. Please select different symbols.")
            return

        player_entry_frame.pack_forget()
        initialize_game(player1_name, player2_name, player1_symbol, player2_symbol)

    def initialize_game(player1, player2, symbol1, symbol2):
        # Game state variables
        turns = 0
        game_over = False

        # Initialize the board
        board = [[None for _ in range(3)] for _ in range(3)]

        def set_tile(row, column):
            nonlocal turns, game_over
            curr_player_name = player1 if turns % 2 == 0 else player2
            curr_player_symbol = symbol1 if turns % 2 == 0 else symbol2

            if game_over or board[row][column]["text"]:
                return

            board[row][column]["text"] = curr_player_symbol
            if curr_player_symbol == "X":
                board[row][column]["fg"] = "#f64878"
            else:
                board[row][column]["fg"] = "#14618c"

            if check_winner(board):
                label["text"] = f"{curr_player_name} wins!"
                game_over = True
                return

            turns += 1
            if turns == 9:
                label["text"] = "It's a tie!"
                game_over = True
                return

            label["text"] = f"{player1 if turns % 2 == 0 else player2}'s turn"

        def check_winner(board):
            def highlight_winner_line(positions):
                for r, c in positions:
                    board[r][c].config(bg="#ffde57", fg="#343434")

            for r in range(3):
                if board[r][0]["text"] == board[r][1]["text"] == board[r][2]["text"] != "":
                    highlight_winner_line([(r, 0), (r, 1), (r, 2)])
                    return True

            for c in range(3):
                if board[0][c]["text"] == board[1][c]["text"] == board[2][c]["text"] != "":
                    highlight_winner_line([(0, c), (1, c), (2, c)])
                    return True

            if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
                highlight_winner_line([(0, 0), (1, 1), (2, 2)])
                return True
            if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
                highlight_winner_line([(0, 2), (1, 1), (2, 0)])
                return True

            return False

        label.pack(side="top", pady=20)
        label["text"] = f"{player1}'s turn"

        board_frame.pack(pady=20)
        for row in range(3):
            for column in range(3):
                board[row][column] = tk.Button(
                    board_frame,
                    text="",
                    font=("Consolas", 30, "bold"),
                    bg="#c7ebf8",
                    fg="#4584b6",
                    width=6,
                    height=2,
                    command=lambda r=row, c=column: set_tile(r, c),
                )
                board[row][column].grid(row=row, column=column)

        restart_button.pack(pady=10)
        back_button.pack(pady=10)
        exit_button_game.pack(pady=10)

    def new_game():
        board_frame.pack_forget()
        label.pack_forget()
        restart_button.pack_forget()
        back_button.pack_forget()
        exit_button_game.pack_forget()
        homepage_frame.pack(fill="both", expand=True)

    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.configure(bg="#FFFFFF")
    center_window(root, 600, 700)
    root.resizable(False, False)

    bg_image = Image.open("tictacbg.png")
    bg_photo = ImageTk.PhotoImage(bg_image.resize((600, 700), Image.Resampling.LANCZOS))

    homepage_frame = tk.Frame(root, bg="#FFFFFF")
    player_entry_frame = tk.Frame(root, bg="#FFFFFF")
    board_frame = tk.Frame(root, bg="#FFFFFF")

    bg_label = tk.Label(homepage_frame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    exit_button_homepage = tk.Button(
        homepage_frame,
        text="Exit",
        font=("Courier New", 16, "bold"),
        bg="#43a4d9",
        fg="#FFFFFF",
        command=root.quit,
    )
    exit_button_homepage.pack(side="bottom", pady=(5, 100))

    multiplayer_button = tk.Button(
        homepage_frame,
        text="Multiplayer", 
        font=("Courier New", 16, "bold"),
        bg="#f64878",
        fg="#FFFFFF",
        command=go_to_fillup_form,
    )
    multiplayer_button.pack(pady=(510, 0))

    homepage_frame.pack(fill="both", expand=True)

    player1_entry_label = tk.Label(player_entry_frame, text="Enter Your Name (Player 1):", font=("Courier New", 14), bg="#FFFFFF")
    player1_entry = tk.Entry(player_entry_frame, font=("Courier New", 14))
    player1_entry_label.pack(pady=(20, 5))
    player1_entry.pack(pady=5)

    player1_symbol_var = tk.StringVar(value="X")
    tk.Label(player_entry_frame, text="Select Your Symbol:", font=("Courier New", 14), bg="#FFFFFF").pack(pady=(20, 5))
    tk.Radiobutton(player_entry_frame, text="X", variable=player1_symbol_var, value="X").pack()
    tk.Radiobutton(player_entry_frame, text="O", variable=player1_symbol_var, value="O").pack()

    player2_entry_label = tk.Label(player_entry_frame, text="Enter Player 2 Name:", font=("Courier New", 14), bg="#FFFFFF")
    player2_entry = tk.Entry(player_entry_frame, font=("Courier New", 14))
    player2_entry_label.pack(pady=(20, 5))
    player2_entry.pack(pady=5)

    player2_symbol_label = tk.Label(player_entry_frame, text="Select Player 2 Symbol:", font=("Courier New", 14), bg="#FFFFFF")
    player2_symbol_var = tk.StringVar(value="O")
    player2_symbol_label.pack(pady=(20, 5))
    tk.Radiobutton(player_entry_frame, text="X", variable=player2_symbol_var, value="X").pack()
    tk.Radiobutton(player_entry_frame, text="O", variable=player2_symbol_var, value="O").pack()

    play_button_form = tk.Button(
        player_entry_frame, text="Play", font=("Courier New", 14, "bold"), bg="#f64878", fg="#FFFFFF", command=start_game
    )
    play_button_form.pack(pady=20)

    back_button_form = tk.Button(
        player_entry_frame, text="Back", font=("Courier New", 14, "bold"), bg="#43a4d9", fg="#FFFFFF", command=go_back_to_homepage
    )
    back_button_form.pack(pady=(5, 10))

    label = tk.Label(root, text="", font=("Courier New", 16), bg="#FFFFFF")

    restart_button = tk.Button(
        root,
        text="Restart Game",
        font=("Courier New", 16, "bold"),
        bg="#f64878",
        fg="#FFFFFF",
        command=new_game,
    )
    
    back_button = tk.Button(
        root,
        text="Back",
        font=("Courier New", 16, "bold"),
        bg="#fF7F4C",
        fg="#FFFFFF",
        command=go_back_to_homepage,
    )
    
    exit_button_game = tk.Button(
        root,
        text="Exit",
        font=("Courier New", 16,"bold"),
        bg="#71ac3d",
        fg="#FFFFFF",
        command=root.quit,
    )

    root.mainloop()


if __name__ == "__main__":
    main_page()
