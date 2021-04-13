import random


def display_board(board):
    print("-----------------------------------------")
    print(" " + str(list(reversed(board[7:13]))))
    print(str(board[13]) + "                  " + str(board[6]))
    print(" " + str(board[:6]))


def get_score(player_id, board):
    # The player's score is the number of seeds in the store to their right.
    return board[player_score_dish(player_id)]


def is_score_dish(pit_id):
    if pit_id % 7 == 6:
        return True
    return False


def get_opponent_id(player_id):
    return (player_id + 1) % 2


def player_score_dish(player_id):
    return (player_id + 1) * 7 - 1


def opponent_score_dish(player_id):
    return player_score_dish(get_opponent_id(player_id))


def opposite_pit(pit_id):
    return 12 - pit_id


# Each player controls the six houses and their seeds on the player's side of the board.
def is_player_pit(pit_id, player_id):
    if player_id == 0 and pit_id < 6:
        return True
    elif player_id == 1 and pit_id > 6 and pit_id < 13:
        return True
    else:
        return False


def set_up(number_of_stones):
    # At the beginning of the game, four seeds are placed in each house.
    # This is the traditional method.
    board = [0] * 14

    for i in range(0, 14):
        if is_score_dish(i):
            continue

        board[i] = number_of_stones

    return board


def try_capture(pit_id, player_id, board):
    # If the last sown seed lands in an empty house owned by the player,
    # and the opposite house contains seeds,
    # both the last seed and the opposite seeds are captured
    # and placed into the player's store.
    if board[pit_id] != 1:
        return board

    if not is_player_pit(pit_id, player_id):
        return board

    opposite_pit_id = opposite_pit(pit_id)
    if board[opposite_pit_id] == 0:
        return board

    new_board = board.copy()

    new_board[player_score_dish(player_id)] += board[opposite_pit_id]
    new_board[opposite_pit_id] = 0
    new_board[player_score_dish(player_id)] += board[pit_id]
    new_board[pit_id] = 0
    return new_board


# This is the function for the player's current turn.  It return the id of the player whose turn is next
def sow(pit_id, player_id, board):
    # Players take turns sowing their seeds.
    # On a turn, the player removes all seeds from one of the houses under their control.
    if not is_player_pit(pit_id, player_id):
        return player_id, board

    # Moving counter-clockwise, the player drops one seed in each house in turn,
    # including the player's own store but not their opponent's.
    num_seeds = board[pit_id]
    new_board = board.copy()
    new_board[pit_id] = 0
    curr_pit = pit_id
    while num_seeds > 0:
        curr_pit = (curr_pit + 1) % 14

        # place seed (skipping original pit and opponent score)
        if curr_pit != pit_id and curr_pit != opponent_score_dish(player_id):
            new_board[curr_pit] += 1
            num_seeds -= 1

    next_board = try_capture(curr_pit, player_id, new_board)
    next_player = get_opponent_id(player_id)
    # If the last sown seed lands in the player's store, the player gets an additional move.
    # There is no limit on the number of moves a player can make in their turn.
    if curr_pit == player_score_dish(player_id):
        next_player = player_id

    return next_player, next_board


def game_is_over(board):
    # When one player no longer has any seeds in any of their houses, the game ends.
    player0_count = sum(board[:6])
    player1_count = sum(board[7:13])

    # The other player moves all remaining seeds to their store,
    if player0_count == 0:
        return True
    if player1_count == 0:
        return True

    return False


# and the player with the most seeds in their store wins.
def who_won(board):
    player0_score = sum(board[:7])
    player1_score = sum(board[7:])
    if player0_score > player1_score:
        return 0
    elif player0_score < player1_score:
        return 1
    else:
        return 2  # draw


def print_end_game(board):
    winner = who_won(board)
    if winner == 2:
        print("Draw")
    else:
        print("Player " + str(winner) + " won!")


def play_game(choose_pit, should_display=False, start_player=0):
    board = set_up(4)

    player_id = start_player

    if should_display == True:
        print("First player " + str(player_id))
        display_board(board)

    while not game_is_over(board):
        if should_display == True:
            print("It's Player " + str(player_id) + "'s turn!")

        pit_id = choose_pit[player_id](player_id, board)
        (player_id, board) = sow(pit_id, player_id, board)

        if should_display == True:
            display_board(board)

    if should_display == True:
        print_end_game(board)

    return who_won(board)


def run_simulations(choose_pit, num_games, display_boards=False, print_statistics=False, x_starts=False):
    outcomes = [0] * 3

    for i in range(0, num_games):
        start_player = i % 2
        if x_starts:
            start_player = 0
        winner = play_game(choose_pit, should_display=display_boards, start_player=start_player)
        outcomes[winner] += 1

    if print_statistics:
        print("Player 0 won " + str(outcomes[0]) + " times: " + str(outcomes[0] / num_games))
        print("Player 1 won " + str(outcomes[1]) + " times: " + str(outcomes[1] / num_games))
        print("It was a draw " + str(outcomes[2]) + " times: " + str(outcomes[2] / num_games))

    return outcomes


# Possible AI or player interfaces
def human_player(player_id, board):
    possible_pit_id = input("Which pit would you like to sow from?")
    try:
        pit_id = int(possible_pit_id)
        return pit_id
    except ValueError:
        print("Invalid input")
        return human_player(player_id, board)
