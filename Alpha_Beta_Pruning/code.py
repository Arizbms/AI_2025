import math

# Initialize board
board = [" " for _ in range(9)]

# Function to print the board
def print_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i*3:(i+1)*3]))
        if i < 2:
            print("---------")
    print()

# Check winner or draw
def check_winner(board):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for (x, y, z) in win_positions:
        if board[x] == board[y] == board[z] and board[x] != " ":
            return board[x]
    if " " not in board:
        return "Draw"
    return None

def available_moves(board):
    return [i for i in range(9) if board[i] == " "]

# Alpha-Beta Pruning (Minimax)
def minimax(board, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_val = -math.inf
        for move in available_moves(board):
            board[move] = "O"
            val = minimax(board, False, alpha, beta)
            board[move] = " "
            best_val = max(best_val, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val
    else:
        best_val = math.inf
        for move in available_moves(board):
            board[move] = "X"
            val = minimax(board, True, alpha, beta)
            board[move] = " "
            best_val = min(best_val, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val

# AI selects best move
def best_move(board):
    best_val = -math.inf
    move = None
    for i in available_moves(board):
        board[i] = "O"
        move_val = minimax(board, False, -math.inf, math.inf)
        board[i] = " "
        if move_val > best_val:
            best_val = move_val
            move = i
    return move

# Game loop
def play_game():
    print("Welcome to Tic-Tac-Toe! You are X, and AI is O.")
    print_board(board)

    while True:
        # Human move
        try:
            human_move = int(input("Enter your move (1-9): ")) - 1
            if human_move not in range(9):
                print("Invalid input! Choose 1–9.")
                continue
            if board[human_move] != " ":
                print("That spot is taken! Try again.")
                continue
        except ValueError:
            print("Enter a number between 1–9.")
            continue

        board[human_move] = "X"

        # Check if player wins before AI moves
        if check_winner(board):
            break

        # AI move
        ai_move = best_move(board)
        board[ai_move] = "O"

        # Print board only after both have played
        print_board(board)

        # Check winner after AI move
        if check_winner(board):
            break

    winner = check_winner(board)
    if winner == "Draw":
        print("It's a draw!")
    else:
        print(f"{winner} wins!")

# Run
if __name__ == "__main__":
    play_game()
