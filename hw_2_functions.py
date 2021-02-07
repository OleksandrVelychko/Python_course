# 1) Write a function that emulates the game "rock, scissors, paper"
# At the entrance, your function accepts your version printed from the console, the computer makes a decision randomly.
import random
import pprint


def get_input():
    """Function returns options dictionary key for item selected by user via entering key or value"""
    while True:
        inp = input('Enter "rock" or 1, "scissors" or 2, "paper" or 3 to play the game\n')
        if inp.isdigit():
            if int(inp) in rsp_options.keys():
                opt_key = int(inp)
                return opt_key
            else:
                continue
        elif inp.lower() in rsp_options.values():
            opt_key = int(list(rsp_options.keys())[list(rsp_options.values()).index(inp.lower())])
            return opt_key
        else:
            continue


def define_winner(hum, comp):
    # Define winner using win_loss_matrix
    human, computer = hum-1, comp-1
    win_loss_matrix = [[-1, 0, 2],
                       [0, -1, 1],
                       [2, 1, -1]]
    rsp_winner = win_loss_matrix[human][computer]
    if rsp_winner == human:
        print("Congratulations! You WIN!")
    elif rsp_winner == computer:
        print("Sorry, computer wins..")
    else:
        print("DRAW GAME. You both selected the same items.")


def play_game_rsp():
    global rsp_options
    rsp_options = {1: 'rock', 2: 'scissors', 3: 'paper'}
    # Getting inputs from human and computer
    user_move = get_input()
    user_item = rsp_options[user_move]
    computer_move = random.randint(1, 3)
    comp_item = rsp_options[computer_move]
    print(f'You selected "{user_item}". Computer selected "{comp_item}"')
    # Defining the winner
    define_winner(user_move, computer_move)


print('\nTask 1. Rock-scissors-paper game\n')
# Running the game in the loop
while True:
    play_game_rsp()
    play_again = input("\nPlay again? Press Y to continue or any other key to stop\n")
    if play_again.lower() != "y":
        break


# 2)Try to imagine a world in which you might have to stay home for (Corona virus) 14 days at any given time.
# Do you have enough toilet paper(TP) to make it through?
# Although the number of squares per roll of TP varies significantly, we'll assume each roll has 500 sheets,
# and the average person uses 57 sheets per day.

# Create a function that will receive a dictionary with two key/values:
# "people" ⁠— Number of people in the household.
# "tp" ⁠— Number of rolls.
# Return a statement telling the user if they need to buy more TP!

def get_paper_forecast(h_hold, forecast_period=14):
    """Function accepts following params:
        1) mandatory parameters people and tp - number of people and number of TP rolls}
        2) optional parameter forecast_period (days) that has default value of 14 days
        """
    sheets_per_roll = 500
    per_person_daily_sheets = 57
    consumption = h_hold['people'] * per_person_daily_sheets * forecast_period
    inventory = h_hold['tp'] * sheets_per_roll
    sheets_left = consumption - inventory
    if sheets_left:
        rolls = sheets_left//sheets_per_roll + 1 if (sheets_left%500) != 0 else sheets_left//500
    print(f"For the next {forecast_period} days You need {consumption} sheets. You have {inventory} sheets.")
    if inventory < consumption:
        return print(f"Alarm! Run to the nearest store and buy {rolls} roll(s) of toilet paper before it's too late\n")
    else:
        return print(f"Keep calm and keep pooping. You have enough toilet paper for {forecast_period} day(s):)\n")


# Testing TP rolls calculation
print('\nTask 2. Toilet paper - to buy or not to buy\n')
household_1 = {'people': 2, 'tp': 1}
household_2 = {'people': 2, 'tp': 1}
household_3 = {'people': 6, 'tp': 18}
household_4 = {'people': 6, 'tp': 6}
get_paper_forecast(household_1)
get_paper_forecast(household_4, 21)


# 3) Make a function that encrypts a given input with these steps:
# Input: "apple"
# Step 1: Reverse the input: "elppa"
# Step 2: Replace all vowels using the following chart:
# a => 0
# e => 1
# i => 2
# o => 2
# u => 3
# # "1lpp0"
# Example:
# encrypt("banana") ➞ "0n0n0b"
# encrypt("karaca") ➞ "0c0r0k"
# encrypt("burak") ➞ "k0r3b"
# encrypt("alpaca") ➞ "0c0pl0"


def encrypt_text(text):
    """Replaces every vowel letter in given text with corresponding digit from the dict"""
    text = text[::-1]
    vowels_dict = {'a': 0, 'e': 1, 'i': 2, 'o': 3, 'u': 4}
    for ch in text:
        if ch.isalpha() and ch.lower() in vowels_dict.keys():
            text = text.replace(ch, str(vowels_dict[ch.lower()]))
    return text


def decrypt_text(text):
    """Replaces every digit in the text with corresponding vowel from the dict"""
    text = text[::-1]
    digits_dict = {0: 'a', 1: 'e', 2: 'i', 3: 'o', 4: 'u'}
    for ch in text:
        if ch.isdigit() and int(ch) in digits_dict.keys():
            text = text.replace(ch, str(digits_dict[int(ch)]))
    return text


# Testing encrypt/decrypt functions
print('\nTask 3. Encrypt given text\n')
test_words_to_encrypt = ['apple', 'banana', 'alpaca', 'burak']
test_words_to_decrypt = []
for x in test_words_to_encrypt:
    print(f"Encrypting word '{x}': {encrypt_text(x)}")
    test_words_to_decrypt.append(x)
print("\nNow decrypting these words:\n")
for x in test_words_to_decrypt:
    print(f"Decrypting word '{x}': {decrypt_text(x)}")


# **4)Given a 3x3 matrix of a completed tic-tac-toe game, create a function that returns whether the game is a win
# for "X", "O", or a "Draw", where "X" and "O" represent themselves on the matrix, and "E" represents an empty spot.
# Example:
# tic_tac_toe([
#     ["X", "O", "X"],
#     ["O", "X", "O"],
#     ["O", "X", "X"]
# ]) ➞ "X"
#
# tic_tac_toe([
#     ["O", "O", "O"],
#     ["O", "X", "X"],
#     ["E", "X", "X"]
# ]) ➞ "O"
#
# tic_tac_toe([
#     ["X", "X", "O"],
#     ["O", "O", "X"],
#     ["X", "X", "O"]
# ]) ➞ "Draw"


# Run tic-tac-toe game matrix analysis
def tic_tac_toe_analyze(game_matrix):
    """Function accepts matrix for finished tic-tac-toe game - a list of 3 lists each containing 3 chars:
    'X', 'O', 'E' - crosses, zeros or empty cells
    based on
    """
    results = fill_x_o_positions(game_matrix)
    win = check_win(results)
    print_matrix(game_matrix)
    if win in ['X', 'O']:
        print(f"\n{win} wins in this game\n")
    elif win == 'D':
        print('\nThis is a draw game\n')
    elif win == 'U':
        print("\nStill more than 1 move to make. Might be a draw game though..\n")
    elif win == 'F':
        print("\nSomething is wrong with this game. Looks like some O's are missing\n")
    print("-"*20)


# Check if one of players wins
def check_win(filled_matrix):
    # All possible winning lines
    winner_lines = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    global winner
    winner = None
    x_pos = filled_matrix[0]
    o_pos = filled_matrix[1]
    e_pos = filled_matrix[2]
    if len(x_pos) - len(o_pos) > 1:
        winner = 'F'
        return winner
    # If one move is left and number of X's is the same as O's then we add last cell to X
    if len(e_pos) == 1 and len(x_pos) == len(o_pos):
        x_pos.append(e_pos[0])
    # Loop to check if any of the winning lines is in the list of X/O positions
    for line in winner_lines:
        if all(elem in x_pos for elem in line):
            winner = 'X'
            break
        elif all(elem in o_pos for elem in line):
            winner = 'O'
            break
    if winner not in ['X', 'O']:
        # analysis for more than 1 empty cell is out of scope of this task
        if len(e_pos) >= 2:
            winner = 'U'
        else:
            winner = 'D'
    return winner


def fill_x_o_positions(matrix):
    position = 0
    x_positions, o_positions, e_positions = [], [], []
    for line in matrix:
        for item in line:
            position += 1
            if item == 'X':
                x_positions.append(position)
            elif item == 'O':
                o_positions.append(position)
            else:
                e_positions.append(position)
    return x_positions, o_positions, e_positions


def print_matrix(matrix):
    my_printer = pprint.PrettyPrinter(width=30)
    my_printer.pprint(matrix)


tic_tac_toe_1 = ([
    ["X", "O", "X"],
    ["O", "X", "O"],
    ["O", "X", "X"]
])

tic_tac_toe_2 = ([
    ["O", "O", "O"],
    ["O", "X", "X"],
    ["E", "X", "X"]
])

tic_tac_toe_3 = ([
    ["X", "X", "O"],
    ["O", "O", "X"],
    ["X", "X", "O"]
])

tic_tac_toe_4 = ([
    ["X", "X", "O"],
    ["O", "O", "X"],
    ["X", "E", "O"]
])

tic_tac_toe_5 = ([
    ["X", "E", "O"],
    ["O", "O", "X"],
    ["X", "E", "O"]
])

tic_tac_toe_6 = ([
    ["X", "X", "O"],
    ["O", "X", "X"],
    ["X", "E", "O"]
])
print("\nTask 4. Tic-Tac-Toe game results analysis\n")
tic_tac_toe_analyze(tic_tac_toe_1)
tic_tac_toe_analyze(tic_tac_toe_2)
tic_tac_toe_analyze(tic_tac_toe_3)
tic_tac_toe_analyze(tic_tac_toe_4)
tic_tac_toe_analyze(tic_tac_toe_5)
tic_tac_toe_analyze(tic_tac_toe_6)
