import random

def create_board():
    """
    Create an empty board.
    """
    board = [['O'] * 9 for _ in range(9)]
    return board

def place_ships(board):
    """
    Randomly place ships on the board.
    """
    ships = {'Destroyer': 3, 'Cruiser': 4, 'Carrier': 5}  # Names and sizes of the ships
    for ship_name, ship_size in ships.items():
        while True:
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                row = random.randint(0, 8)
                col = random.randint(0, 9 - ship_size)
                if all(board[row][col+i] == 'O' for i in range(ship_size)):
                    for i in range(ship_size):
                        board[row][col+i] = 'S'
                    break
            else:
                row = random.randint(0, 9 - ship_size)
                col = random.randint(0, 8)
                if all(board[row+i][col] == 'O' for i in range(ship_size)):
                    for i in range(ship_size):
                        board[row+i][col] = 'S'
                    break

def print_board(board, show_ships=False):
    """
    Print the board.
    """
    print('   A B C D E F G H I ')
    for i in range(9):
        row = []
        for j in range(9):
            if board[i][j] == 'S' and not show_ships:
                row.append('O')
            else:
                row.append(board[i][j])
        print(f'{i+1}  {" ".join(row)}')

def validate_input(guess):
    """
    Validate user input.
    """
    if len(guess) != 2:
        return False
    col = guess[0].upper()
    row = guess[1:]
    if col not in 'ABCDEFGHI' or not row.isdigit():
        return False
    row = int(row)
    if row < 1 or row > 9:
        return False
    return True

def check_guess(guess, board):
    """
    Check if the guess is a hit or miss.
    """
    col = ord(guess[0].upper()) - ord('A')
    row = int(guess[1:]) - 1
    if board[row][col] == 'S':
        return 'hit'
    else:
        return 'miss'

def update_board(guess, result, board):
    """
    Update the board based on the guess result.
    """
    col = ord(guess[0].upper()) - ord('A')
    row = int(guess[1:]) - 1
    if result == 'hit':
        board[row][col] = 'X'  # Mark as hit
    else:
        board[row][col] = 'M'  # Mark as missed

def all_ships_sunk(board):
    """
    Check if all ships are sunk.
    """
    for row in board:
        if 'S' in row:
            return False  # Not all ships are sunk
    return True  # All ships are sunk

def play_game():
    """
    Main game loop.
    """
    print('Welcome to Battleships!')
    player_name = input('Please enter your name: ')
    print(f'Hello {player_name}! Let\'s play Battleships!')

    player_board = create_board()
    computer_board = create_board()
    place_ships(player_board)
    place_ships(computer_board)

    ships_remaining = {'Destroyer': 3, 'Cruiser': 4, 'Carrier': 5}  # Names and sizes of the ships remaining

    while True:
        print('Player Board:')
        print_board(player_board)
        print('Computer Board:')
        print_board(computer_board, show_ships=False)

        # Player's turn
        while True:
            guess = input('Enter your guess (e.g. A1): ')
            if validate_input(guess):
                break
            print('Invalid input. Must be a letter A-I followed by a number 1-9. Try again.')

        # Check if the player's guess is a hit or miss
        player_result = check_guess(guess, computer_board)
        print(f'{player_name} guessed {player_result}!')

        # Computer's turn (random guess)
        computer_guess = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']) + str(random.randint(1, 9))

        # Check if the computer's guess is a hit or miss
        computer_result = check_guess(computer_guess, player_board)
        print(f'Computer guessed {computer_guess} and {computer_result}!')

        # Update the boards based on the guess results
        update_board(guess, player_result, computer_board)
        update_board(computer_guess, computer_result, player_board)

        # Check if a ship has been sunk and update the ships_remaining dictionary
        for ship_name, ship_size in ships_remaining.items():
            if ship_size > 0 and all_ships_sunk(player_board) and ship_name in str(computer_board):
                ships_remaining[ship_name] -= 1
                print(f"The enemy's {ship_name} has been sunk! {ships_remaining[ship_name]} more ship(s) remaining.")

        # Check if the game is over (all ships are sunk) and end the game if necessary
        if all_ships_sunk(player_board) or all_ships_sunk(computer_board):
            print('Game over!')
            break

# Start the game
play_game()
