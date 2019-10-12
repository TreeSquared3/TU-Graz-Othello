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

game_field_start = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 2, 0, 0, 0],
  [0, 0, 0, 2, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
]

game_field = game_field_start


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


def fieldValue(field):
  return game_field[field[0]][field[1]]

def convNumToCoord(field):
  return chr(ord("A")+field[0])+str(field[1])

def convCoordToNum(coord):
  return ord(coord[0])-ord("A"), int(coord[1])
  

def checkFieldInRange(field):
  if not (int(field[0]) in range(0,8) and int(field[1]) in range(0,8)):
    return False
  return True

def checkFieldOccupied(field):
  if not fieldValue(field) == 0:
    print(ERROR_OCCUPIED)
    return True
  return False

def checkValidCoord(coord):
  if len(coord) != 2:
    return False
  
  try:
    field = convCoordToNum(coord)
  except:
    return False
  
  if not checkFieldInRange(field):
    return False

  return True

def checkTurnPossible(field, current_player):
  if current_player == 1:
    opponent = 2
  else:
    opponent = 1
  
  if checkFieldOccupied(field):
    return False

  for offset_col, offset_row in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(1,-1)): #up, up-right, right, down-right, down, down-left, left, up-left
    fieldToCheck = list(field)
    fieldToCheck[0] += offset_col
    fieldToCheck[1] += offset_row

    if not checkFieldInRange(fieldToCheck):
      continue
    if not fieldValue(fieldToCheck) == opponent:
      continue

    while(fieldValue(fieldToCheck) == opponent):
      fieldToCheck[0] += offset_col
      fieldToCheck[1] += offset_row
      if not checkFieldInRange(fieldToCheck):
        continue

    if not fieldValue(fieldToCheck) == current_player:
      continue
    
    return True

  return False

def checkAnyTurnPossible(current_player):
  for i in range(0,8):
      for u in range(0,8):
        if fieldValue((i,u)) == 0:
          if checkTurnPossible((i,u), current_player):
            return True
  return False

def turnPoints(current_player, field):
  points = 0
  
  if current_player == 1:
    opponent = 2
  else:
    opponent = 1

  if checkFieldOccupied(field):
    return 0

  for offset_col, offset_row in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)): #up, up-right, right, down-right, down, down-left, left, up-left
    fieldToCheck = list(field)
    fieldToCheck[0] += offset_col
    fieldToCheck[1] += offset_row

    if not checkFieldInRange(fieldToCheck):
      continue

    points_temp = 0

    while(fieldValue(fieldToCheck) == opponent):
      points_temp += 1

      fieldToCheck[0] += offset_col
      fieldToCheck[1] += offset_row
      if not checkFieldInRange(fieldToCheck):
        continue

    if fieldValue(fieldToCheck) == current_player:
      points += points_temp

  return points

def allTurnsPoints(current_player):
  turns = list()
  for i in range(0,8):
      for u in range(0,8):
        if fieldValue((i,u)) == 0:
          points = turnPoints(current_player,(i,u))
          if points > 0:
            turns.append(((i,u), points))
  turns.sort(key=lambda tupl: tupl[1], reverse=True)
  return turns

def setStone(player, field):
  game_field[field[0]][field[1]] = player

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
  print(allTurnsPoints(current_player))

  #input
  if current_player == 1:
    inp = str(input(PROMPT_PLAYER_1)).upper()
  elif current_player == 2:
    inp = str(input(PROMPT_PLAYER_2)).upper()
  
  #process input
  if inp == "SKIP":
    if checkAnyTurnPossible(current_player):
      print(ERROR_INVALID_INPUT)
      return 1
    return 0
  elif inp == "QUIT":
    return 2
  elif checkValidCoord(inp):
    field = convCoordToNum(inp)

    if not checkTurnPossible(field, current_player):
      print(ERROR_NOT_ALLOWED)
      return 1

    setStone(current_player, field)

    turnStones(field)
    return 0
  else:
    print(ERROR_INVALID_INPUT)
    return 1

def main():
  printBoard(game_field)
  current_player = 1

  while(True):
    turnResult = playTurn(current_player)

    if turnResult == 1:
      continue
    elif turnResult == 2:
      return 0

    printBoard(game_field)

    if current_player == 1:
      current_player = 2
    else:
      current_player = 1
    
    if not (checkAnyTurnPossible(1) or checkAnyTurnPossible(2)):
        pointsPlayer1 = 0
        pointsPlayer2 = 0

        for i in game_field:
          for u in i:
            if u == 1:
              pointsPlayer1 += 1
            elif u == 2:
              pointsPlayer2 += 1

        print(STATISTICS_1 + str(pointsPlayer1))
        print(STATISTICS_2 + str(pointsPlayer2))

        if pointsPlayer1 > pointsPlayer2:
          print(WON_PLAYER_1)
          return 1
        elif pointsPlayer2 > pointsPlayer1:
          print(WON_PLAYER_2)
          return 2
        else:
          print(WON_DRAW)
          return 3
          

if __name__ == "__main__":
  main()
