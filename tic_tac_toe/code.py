# Create 3x3 board
def create_board():
    return [["-" for _ in range(3)] for _ in range(3)]

# Print the board
def show_board(board):
    for row in board:
        # print(" | ".join(row))
        print(row," ")

# Map cell number (1-9) to row, col
def cell_to_coords(cell):
    cell -= 1 # shift to 0–8
    return cell // 3, cell % 3


def is_full(board):
    return all(board[r][c] != "-" for r in range(3) for c in range(3))


def check_winner(board, player):
    # rows
    for r in range(3):
        if all(board[r][c] == player for c in range(3)):
            return True
    # cols
    for c in range(3):
        if all(board[r][c] == player for r in range(3)):
            return True
    # diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Player move 
def get_move(board, player):
    while True:
        try:
            cell = int(input(f"Player {player}, position: "))
            if cell < 1 or cell > 9:
                print("Please enter a number from 1 to 9.\n")
                continue
            r, c = cell_to_coords(cell)
            if board[r][c] != "-":
                print("That cell is already taken. Try again.\n")
                continue
            return r, c
        except ValueError:
            print("Please enter numbers only.\n")

# Main game loop
def play_game():
    board = create_board()
    current = "X" # Player X starts
    print("Tic Tac Toe — Two Players (1-9 version)\n")
    show_board(board)

    while True:
        r, c = get_move(board, current)
        board[r][c] = current
        show_board(board)

        if check_winner(board, current):
            print(f" Player {current} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    play_game()
