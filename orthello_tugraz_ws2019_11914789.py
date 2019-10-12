# Orthello - DYOA at TU Graz WS 2019
# Name:       Martin Baumann
# Student ID: 11914789

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
def printBoard(boardData):
  print("\n   ┌───┬───┬───┬───┬───┬───┬───┬───┐")

  row_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

  row_count = 0

  for row in boardData:
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
    if (row_count < len(boardData)):
      print("   ├───┼───┼───┼───┼───┼───┼───┼───┤")

  print("   └───┴───┴───┴───┴───┴───┴───┴───┘")
  print("     0   1   2   3   4   5   6   7  ")


def main():
  printBoard(game_field)
  in_progress = True
  current_player = 1

  while(in_progress):
    if not playTurn(current_player):
      continue

    printBoard(game_field)

    if current_player == 1:
      current_player = 2
    else:
      current_player = 1



def checkFieldInRange(field):
  if not (int(field[0]) in range(0,7) and int(field[1]) in range(0,7)):
    print(ERROR_INVALID_INPUT)
    return False
  return True

def checkFieldOccupied(field):
  if not fieldValue(field) == 0:
    print(ERROR_OCCUPIED)
    return False
  return True

def checkInput(inp):
  #implement detection stuff other than field
  return True

def fieldValue(field):
  return game_field[field[0]][field[1]]

def convNumToCoord(field):
  return chr(ord("A")+field[0])+str(field[1])

def convCoordToNum(field):
  return ord(field[0])-ord("A"), int(field[1])

def setStone(player, field):
  game_field[field[0]][field[1]] = player

<<<<<<< Updated upstream
def checkTurnPossible(field, current_player):
  if current_player == 1:
    opponent = 2
  else:
    opponent = 1
  
  for offset_col, offset_row in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(1,-1)): #up, up-right, right, down-right, down, down-left, left, up-left
    fieldToCheck = list(field)
    fieldToCheck[0] += offset_col
    fieldToCheck[1] += offset_row

    if fieldValue(fieldToCheck) == 0:
      continue
    if fieldValue(fieldToCheck) == current_player:
      continue

    while(fieldValue(fieldToCheck) == opponent):
      fieldToCheck[0] += offset_col
      fieldToCheck[1] += offset_row
    
    lastField = fieldToCheck

    if fieldValue(lastField) == 0:
      continue
    
    return True
=======
def checkTurnPossible(field, player):
  
>>>>>>> Stashed changes

def turnStones(field_placed):
  current_player = fieldValue(field_placed)
  if current_player == 1:
    opponent = 2
  else:
    opponent = 1
  
  for offset_col, offset_row in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(1,-1)): #up, up-right, right, down-right, down, down-left, left, up-left
    fieldToCheck = list(field_placed)
    fieldToCheck[0] += offset_col
    fieldToCheck[1] += offset_row

    if fieldValue(fieldToCheck) == 0:
      continue
    if fieldValue(fieldToCheck) == current_player:
      continue

    while(fieldValue(fieldToCheck) == opponent):
      fieldToCheck[0] += offset_col
      fieldToCheck[1] += offset_row
    
    lastField = fieldToCheck

    if fieldValue(lastField) == 0:
      continue

    fieldToTurn = list(field_placed)

    while fieldToTurn != lastField:
      setStone(current_player, fieldToTurn)
      fieldToTurn[0] += offset_col
      fieldToTurn[1] += offset_row


def playTurn(current_player):
  if current_player == 1:
    inp = str(input(PROMPT_PLAYER_1)).upper()
  elif current_player == 2:
    inp = str(input(PROMPT_PLAYER_2)).upper()
  
  if not checkInput(inp):
    return False

  field = convCoordToNum(inp)

  setStone(current_player, field)
<<<<<<< Updated upstream

  if not checkTurnPossible(field, current_player):
    print(ERROR_NOT_ALLOWED)
    setStone(0, field)
    return False

=======
>>>>>>> Stashed changes
  turnStones(field)
  return True


if __name__ == "__main__":
  main()
