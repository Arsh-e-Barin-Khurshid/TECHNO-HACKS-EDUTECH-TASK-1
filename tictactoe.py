from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Tic Tac Toe")

play_with_computer = False

def show_initial_screen():
    global frame_initial
    frame_initial = Frame(root)
    frame_initial.pack(pady=20)

    titleLabel = Label(frame_initial, text="Tic Tac Toe", font=("Comic Sans MS", 30, "bold"), bg="#FFC0CB", width=20)  # Pink background
    titleLabel.pack(pady=20)

    startButton = Button(frame_initial, text="Click to Play", width=16, height=2, font=("Comic Sans MS", 24), bg="#FF69B4", relief=RAISED, borderwidth=5, command=show_mode_selection_screen)  # Hot pink
    startButton.pack(pady=20)

def show_mode_selection_screen():
    frame_initial.pack_forget()
    global frame_mode_selection
    frame_mode_selection = Frame(root)
    frame_mode_selection.pack(pady=20)

    titleLabel = Label(frame_mode_selection, text="Tic Tac Toe", font=("Comic Sans MS", 30, "bold"), bg="#FFC0CB", width=20)  # Pink background
    titleLabel.pack(pady=20)

    Label(frame_mode_selection, text="Choose Mode:", font=("Comic Sans MS", 20), bg="#FFC0CB").pack(pady=10)

    Button(frame_mode_selection, text="Show Modes", width=16, height=2, font=("Comic Sans MS", 20), bg="#FF1493", relief=RAISED, borderwidth=5, command=show_mode_options).pack(pady=10)  # Deep pink

def show_mode_options():
    frame_mode_selection.pack_forget()
    global frame_mode_options
    frame_mode_options = Frame(root)
    frame_mode_options.pack(pady=20)

    titleLabel = Label(frame_mode_options, text="Tic Tac Toe", font=("Comic Sans MS", 30, "bold"), bg="#FFC0CB", width=20)  # Pink background
    titleLabel.pack(pady=20)

    Label(frame_mode_options, text="Choose Game Mode:", font=("Comic Sans MS", 20), bg="#FFC0CB").pack(pady=10)

    Button(frame_mode_options, text="AI Mode", width=16, height=2, font=("Comic Sans MS", 20), bg="#FF1493", relief=RAISED, borderwidth=5, command=lambda: [frame_mode_options.pack_forget(), set_mode("AI")]).pack(pady=10)
    Button(frame_mode_options, text="Multiplayer", width=16, height=2, font=("Comic Sans MS", 20), bg="#FF1493", relief=RAISED, borderwidth=5, command=lambda: [frame_mode_options.pack_forget(), set_mode("Multiplayer")]).pack(pady=10)

def set_mode(mode):
    global play_with_computer
    play_with_computer = (mode == "AI")
    show_game_screen(mode)

def show_game_screen(mode):
    global frame_game, buttons, board, turn, game_over, titleLabel, modeLabel
    frame_game = Frame(root)
    frame_game.pack(pady=20)

    titleLabel = Label(frame_game, text="Tic Tac Toe", font=("Comic Sans MS", 30, "bold"), bg="#FFC0CB", width=20)  # Pink background
    titleLabel.grid(row=0, column=0, columnspan=3)

    modeLabel = Label(frame_game, text=f"Playing Mode: {mode}", font=("Comic Sans MS", 20), bg="#FFC0CB")
    modeLabel.grid(row=1, column=0, columnspan=3)

    buttons = []

    # Reset game state
    board = {1: " ", 2: " ", 3: " ",
             4: " ", 5: " ", 6: " ",
             7: " ", 8: " ", 9: " "}
    turn = "X"
    game_over = False

    # Create 3x3 grid of buttons with equal width and height
    button_size = 4  # Smaller size for each button
    for row in range(3):
        for column in range(3):
            button = Button(frame_game, text=" ", font=("Comic Sans MS", 15), bg="#FFD700", relief=RAISED, borderwidth=5, fg="black", width=button_size, height=button_size)  # Gold background
            button.grid(row=row + 2, column=column, sticky="nsew")
            button.bind("<Button-1>", play)
            buttons.append(button)

    # Restart Button
    resultButton = Button(frame_game, text="RESTART GAME!", width=16, height=2, font=("Comic Sans MS", 24), bg="#FF69B4", relief=RAISED, borderwidth=5, command=restart_game)  # Hot pink
    resultButton.grid(row=5, column=0, columnspan=3, pady=20)

    # Adjust grid weights to ensure buttons expand properly
    for i in range(3):
        frame_game.grid_columnconfigure(i, weight=1)
        frame_game.grid_rowconfigure(i + 2, weight=1)

def checkForWin(player):
    # Rows
    if (board[1] == board[2] == board[3] == player or
        board[4] == board[5] == board[6] == player or
        board[7] == board[8] == board[9] == player):
        return True
    
    # Columns
    if (board[1] == board[4] == board[7] == player or
        board[2] == board[5] == board[8] == player or
        board[3] == board[6] == board[9] == player):
        return True
    
    # Diagonals
    if (board[1] == board[5] == board[9] == player or
        board[3] == board[5] == board[7] == player):
        return True
    
    return False

def checkForDraw():
    return all(value != " " for value in board.values())

def minimax(board, isMaximizing):
    if checkForWin("O"):
        return 1
    if checkForWin("X"):
        return -1
    if checkForDraw():
        return 0
    
    if isMaximizing:
        bestScore = -1000
        for key in board.keys():
            if board[key] == " ":
                board[key] = "O"
                score = minimax(board, False)
                board[key] = " "
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 1000
        for key in board.keys():
            if board[key] == " ":
                board[key] = "X"
                score = minimax(board, True)
                board[key] = " "
                if score < bestScore:
                    bestScore = score
        return bestScore

def playComputer():
    bestScore = -1000
    bestMove = 0
    for key in board.keys():
        if board[key] == " ":
            board[key] = "O"
            score = minimax(board, False)
            board[key] = " "
            if score > bestScore:
                bestScore = score
                bestMove = key
    board[bestMove] = "O"
    for button in buttons:
        row, column = button.grid_info()["row"], button.grid_info()["column"]
        if (row - 2) * 3 + column + 1 == bestMove:
            button["text"] = "O"
            break

def play(event):
    global turn, game_over
    if game_over:
        return

    button = event.widget
    row, column = button.grid_info()["row"], button.grid_info()["column"]
    clicked = (row - 2) * 3 + column + 1

    if board[clicked] == " ":
        button["text"] = turn
        board[clicked] = turn 
        
        if checkForWin(turn):
            game_over = True
            titleLabel.config(text=f"{turn} WINS THE GAME!", bg="#FFC0CB")
            disable_buttons()
        elif checkForDraw():
            game_over = True
            titleLabel.config(text="GAME DRAW!", bg="#FFC0CB")
            disable_buttons()
        else:
            turn = "O" if turn == "X" else "X"
            if play_with_computer and turn == "O" and not game_over:
                playComputer()
                if checkForWin("O"):
                    game_over = True
                    titleLabel.config(text="O WINS THE GAME!", bg="#FFC0CB")
                    disable_buttons()
                elif checkForDraw():
                    game_over = True
                    titleLabel.config(text="GAME DRAW!", bg="#FFC0CB")
                    disable_buttons()
                turn = "X"

def disable_buttons():
    for button in buttons:
        button.config(state=DISABLED)

def restart_game():
    global turn, game_over, frame_game
    turn = "X"
    game_over = False
    titleLabel.config(text="Tic Tac Toe", bg="#FFC0CB")  # Pink background
    modeLabel.config(text=f"Playing Mode: {'AI' if play_with_computer else 'Multiplayer'}", bg="#FFC0CB")
    for button in buttons:
        button.config(text=" ", state=NORMAL, fg="black")  # Reset button text color to black
    # Reset board dictionary
    for key in board:
        board[key] = " "
    frame_game.pack_forget()
    show_mode_selection_screen()

show_initial_screen()
root.mainloop()


