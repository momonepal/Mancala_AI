import mancala
import random


# random_player takes a player id and current board state and returns the id of the pit to play
# player_id is 0 or 1
# board is a list of ints representing the number of seeds in each of the 14 pits in the following layout:
#   12 11 10  9  8  7
# 13                  6
#    0  1  2  3  4  5
# player 0 can only play from pits 0 to 5
# player 1 can only play from pits 7 to 12

def gopen_pits(player_id: int, board: [int]) -> [int]:
    return [x for x in range(len(board)) if board[x] != 0 and mancala.is_player_pit(x, player_id) == True]


def random_player(player_id: int, board: [int]) -> int:
    open_pit = gopen_pits(player_id, board)
    return random.choice(open_pit)


def expert_player(player_id: int, board: [int]) -> int:
    open_pit = gopen_pits(player_id, board)

    for pits in open_pit:
        # if pits + board[pits] == 4:
        if pits + board[pits] == mancala.player_score_dish(player_id):
            return pits

    return sorted(open_pit)[-1]


def score_board(player_id: int, board: [int]) -> (int, bool):
    opponent_id = (player_id + 1) % 2
    if mancala.game_is_over(board) and mancala.who_won(board) == 0:
        return 24, True
    elif mancala.game_is_over(board) and mancala.who_won(board) == 1:
        return -24, True
    elif mancala.game_is_over(board) and mancala.who_won(board) == 2:
        return 1, True
    else:
        return (mancala.get_score(player_id, board) - mancala.get_score(mancala.get_opponent_id(player_id),
                                                                        board)), False


def generate_all_board(player_id: int, curr_board: [int], spot_to_play: int) -> [int]:
    new_board = curr_board.copy()
    next_player, new_board = mancala.sow(spot_to_play, player_id, new_board)
    return new_board


def minimax(player_id: int, curr_board: [int], depth: int, should_maximize: bool, alpha=float('-inf'),
            beta=float('inf')) -> int:
    curr_score, is_done = score_board(player_id, curr_board)

    if depth == 0 or is_done:
        return curr_score * (depth + 1)

    open_pit = gopen_pits(player_id, curr_board)

    if should_maximize:
        max_score = float('-inf')
        for pit in open_pit:
            board = generate_all_board(player_id, curr_board, pit)
            score = minimax(player_id, board, depth - 1, False, alpha, beta)
            max_score = max(max_score, score)
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score

    else:
        min_score = float('inf')
        for pit in open_pit:
            board = generate_all_board((player_id + 1) % 2, curr_board, pit)
            score = minimax(player_id, board, depth - 1, True, alpha, beta)
            min_score = min(min_score, score)
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score


def minimax_player(player_id: int, curr_board: [int]) -> int:
    open_pit = gopen_pits(player_id, curr_board)
    possible_boards = list(map(lambda x: generate_all_board(player_id, curr_board, x), open_pit))
    scored_board = list(map(lambda x: minimax(player_id, x, 1, False), possible_boards))
    best_score = max(scored_board)
    best_moves = [x for x, score in zip(open_pit, scored_board) if score == best_score]
    return random.choice(best_moves)


def score_boards(player_id: int, board: [int]) -> (int, bool):
    opponent_id = (player_id + 1) % 2
    if mancala.game_is_over(board) and mancala.who_won(board) == 0:
        return 1, True
    elif mancala.game_is_over(board) and mancala.who_won(board) == 1:
        return -1, True
    elif mancala.game_is_over(board) and mancala.who_won(board) == 2:
        return 0, True
    else:
        return 0, False


def playout(player_id: int, curr_board: [int]) -> bool:
    score, is_finished = score_boards(player_id, curr_board)
    if is_finished:
        return score == 1
    next_board = curr_board
    next_player = 1 - player_id

    while not is_finished:
        spot_to_play = random_player(next_player, next_board)
        next_board = generate_all_board(next_player, next_board, spot_to_play)
        score, is_finished = score_boards(player_id, next_board)
        next_player = 1 - next_player

    return score == 1


def monte_carlo_player(player_id: int, curr_board: [int]) -> int:
    open_pit = gopen_pits(player_id, curr_board)
    possible_boards = list(map(lambda x: generate_all_board(player_id, curr_board, x), open_pit))

    num_sim = 100
    wins = [sum([1 for _ in range(num_sim) if playout(player_id, board)]) for board in possible_boards]
    # print(wins)

    index = max(range(len(open_pit)), key=lambda i: wins[i])
    return open_pit[index]


def competition_player(player_id: int, board: [int]) -> int:
    open_pit = gopen_pits(player_id, board)

    for pits in open_pit:
        # if pits + board[pits] == 4:
        if pits + board[pits] == mancala.player_score_dish(player_id):
            return pits

    return sorted(open_pit)[-1]


# mancala.play_game([random_player, minimax_player], should_display=True, start_player=0)

# mancala.run_simulations([monte_carlo_player, random_player], 100, display_boards=False, print_statistics=True)

mancala.run_simulations([monte_carlo_player, minimax_player], 100, display_boards=False, print_statistics=True)
# mancala.run_simulations([minimax_player, expert_player], 1000, display_boards=False, print_statistics=True)
# mancala.run_simulations([minimax_player, random_player], 1000, display_boards=False, print_statistics=True)
