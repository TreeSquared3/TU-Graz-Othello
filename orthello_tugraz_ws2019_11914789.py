# Orthello - DYOA at TU Graz WS 2019
# Name:       Martin Baumann
# Student ID: 11914789

import random

# STATIC STRINGS - DO NOT CHANGE

TERMINAL_COLOR_NC = '\033[0m'
TERMINAL_COLOR_1 = '\033[94m'
TERMINAL_COLOR_2 = '\033[92m'
TERMINAL_COLOR_EMPTY = '\033[93m'
TERMINAL_COLOR_ERROR = '\033[91m'

ERROR_INVALID_INPUT = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Invalid Input"
ERROR_NOT_ALLOWED = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Stone is not allowed to be placed here"
ERROR_OCCUPIED = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Field already occupied"

PROMPT_HUMAN_AI = "Play against a [human] or an [ai]? "

PROMPT_PLAYER_1 = TERMINAL_COLOR_1 + "player1>" + TERMINAL_COLOR_NC + " "
PROMPT_PLAYER_2 = TERMINAL_COLOR_2 + "player2>" + TERMINAL_COLOR_NC + " "
PROMPT_AI = TERMINAL_COLOR_2 + "ai plays>" + TERMINAL_COLOR_NC + " "

WON_PLAYER_1 = TERMINAL_COLOR_1 + "[player1]" + TERMINAL_COLOR_NC + " has won!"
WON_PLAYER_2 = TERMINAL_COLOR_2 + "[player2]" + TERMINAL_COLOR_NC + " has won!"
WON_DRAW = "It's a " + TERMINAL_COLOR_EMPTY + "[DRAW]" + TERMINAL_COLOR_NC

STATISTICS_1 = "[STATS]" + TERMINAL_COLOR_1 + "[player1]=" + TERMINAL_COLOR_NC
STATISTICS_2 = "[STATS]" + TERMINAL_COLOR_2 + "[player2]=" + TERMINAL_COLOR_NC

INPUT_HUMAN = "human"
INPUT_COMPUTER = "ai"
INPUT_SKIP = "skip"
INPUT_QUIT = "quit"

# END OF STATIC STRINGS

# OWN STATIC STRINGS

MODE_AI = "ai"
MODE_HUMAN = "human"

TURN_PLACED_STONE = 0
TURN_ERROR = 1
TURN_QUIT = 2
TURN_SKIP = 3

# END OF OWN STATIC STRINGS

""" game_field = [
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 0, 0, 0, 0, 1, 1],
  [1, 1, 0, 1, 2, 0, 1, 1],
  [1, 1, 0, 2, 1, 0, 1, 1],
  [1, 1, 0, 0, 0, 0, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
] """

game_field = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


# A function to print boardData provided.
def print_board(board_data):
    print("\n   ┌───┬───┬───┬───┬───┬───┬───┬───┐")

    row_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

    row_count = 0

    for row in board_data:
        column_string = " " + row_keys[row_count] + " │"
        for column in row:
            if column == 1:
                column_text = TERMINAL_COLOR_1 + "1" + TERMINAL_COLOR_NC
            elif column == 2:
                column_text = TERMINAL_COLOR_2 + "2" + TERMINAL_COLOR_NC
            else:
                column_text = TERMINAL_COLOR_EMPTY + "0" + TERMINAL_COLOR_NC

            column_string += " " + column_text + " │"
        print(column_string)

        row_count = row_count + 1
        if row_count < len(board_data):
            print("   ├───┼───┼───┼───┼───┼───┼───┼───┤")

    print("   └───┴───┴───┴───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4   5   6   7  ")


def field_value(field):
    return game_field[field[0]][field[1]]


def nums_to_coord(field):
    return chr(ord("a") + field[0]) + str(field[1])


def coord_to_nums(coord):
    return ord(coord[0]) - ord("a"), int(coord[1])


def field_in_range(field):
    if not (int(field[0]) in range(0, 8) and int(field[1]) in range(0, 8)):
        return False
    return True


def field_occupied(field):
    if not field_value(field) == 0:
        print(ERROR_OCCUPIED)
        return True
    return False


def valid_coord(coord):
    if len(coord) != 2:
        return False

    try:
        field = coord_to_nums(coord)
    except:
        return False

    if not field_in_range(field):
        return False

    return True


def field_full():
    for row in game_field:
        if 0 in row:
            return False
    return True


# returns number of stones that would be flipped of a player placed their stone
def turn_stone_flips(player, field):
    flipped_stones_total = []

    opponent = (player % 2) + 1

    if field_occupied(field):
        return []

        # up, up-right, right, down-right, down, down-left, left, up-left
    for offset_col, offset_row in ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)):
        turn_to_check = list(field)
        turn_to_check[0] += offset_col
        turn_to_check[1] += offset_row

        if not field_in_range(turn_to_check):
            continue

        flipped_stones_cur_dir = []

        out_of_field = False

        while field_value(turn_to_check) == opponent:
            flipped_stones_cur_dir.append(turn_to_check.copy())

            turn_to_check[0] += offset_col
            turn_to_check[1] += offset_row
            if not field_in_range(turn_to_check):
                out_of_field = True
                break

        if out_of_field:
            continue

        if field_value(turn_to_check) == player:
            flipped_stones_total.extend(flipped_stones_cur_dir)

    return flipped_stones_total


def all_turns_points(player):
    turns = []
    for row in range(0, 8):
        for column in range(0, 8):
            field = (row, column)
            if field_value(field) == 0:
                points = len(turn_stone_flips(player, field))
                if points > 0:
                    turns.append((field, points))

    random.shuffle(turns)
    turns.sort(key=lambda tupl: tupl[1], reverse=True)
    return turns


def turn_possible(player, field):
    return len(turn_stone_flips(player, field)) > 0


def any_turn_possible(player):
    return len(all_turns_points(player)) > 0


def play_stone(player, field):
    for fieldToFlip in turn_stone_flips(player, field):
        set_stone(player, fieldToFlip)

    set_stone(player, field)


def set_stone(player, field):
    game_field[field[0]][field[1]] = player


def play_turn_ai():
    possible_turns = all_turns_points(2)

    if len(possible_turns) <= 0:
        print(PROMPT_AI + INPUT_SKIP)
        return INPUT_SKIP

    coord = nums_to_coord(possible_turns[0][0])

    print(PROMPT_AI + coord)

    return coord


def play_turn_human(mode, player):
    # input
    if player == 1:
        inp = input(PROMPT_PLAYER_1).lower()
    elif player == 2 and mode == MODE_HUMAN:
        inp = input(PROMPT_PLAYER_2).lower()
    elif player == 2 and mode == MODE_AI:
        inp = play_turn_ai().lower()
    else:
        inp = ""

    # process input
    if inp == INPUT_SKIP:
        if any_turn_possible(player):
            print(ERROR_INVALID_INPUT)
            return TURN_ERROR
        return TURN_SKIP
    elif inp == INPUT_QUIT:
        return TURN_QUIT
    elif valid_coord(inp):
        field = coord_to_nums(inp)

        if not turn_possible(player, field):
            print(ERROR_NOT_ALLOWED)
            return TURN_ERROR

        play_stone(player, field)

        return TURN_PLACED_STONE
    else:
        print(ERROR_INVALID_INPUT)
        return TURN_ERROR


def main():
    # prompt AI or human
    mode = ""
    while mode == "":
        inp = str(input(PROMPT_HUMAN_AI)).lower()

        if inp == INPUT_COMPUTER:
            mode = MODE_AI
        elif inp == INPUT_HUMAN:
            mode = MODE_HUMAN
        else:
            print(ERROR_INVALID_INPUT)

    player = 1

    # play
    print_board(game_field)

    last_play = -1

    while True:
        turn_result = play_turn_human(mode, player)

        print_board(game_field)

        if turn_result == TURN_ERROR:
            continue
        elif turn_result == TURN_QUIT:
            return 0

        player = (player % 2) + 1

        # if no more moves possible, print results
        if field_full() or (turn_result == TURN_SKIP and last_play == TURN_SKIP):
            points_player1 = 0
            points_player2 = 0

            for i in game_field:
                for u in i:
                    if u == 1:
                        points_player1 += 1
                    elif u == 2:
                        points_player2 += 1

            print(STATISTICS_1 + str(points_player1))
            print(STATISTICS_2 + str(points_player2))

            if points_player1 > points_player2:
                print(WON_PLAYER_1)
                return 1
            elif points_player2 > points_player1:
                print(WON_PLAYER_2)
                return 2
            else:
                print(WON_DRAW)
                return 3

        last_play = turn_result


if __name__ == "__main__":
    main()
