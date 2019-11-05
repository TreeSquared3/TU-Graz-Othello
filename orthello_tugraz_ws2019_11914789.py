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

def numsToCoord(field):
  return chr(ord("a")+field[0])+str(field[1])

def coordToNums(coord):
  return ord(coord[0])-ord("a"), int(coord[1])

def fieldInRange(field):
  if not (int(field[0]) in range(0,8) and int(field[1]) in range(0,8)):
    return False
  return True

def fieldOccupied(field):
  if not fieldValue(field) == 0:
    print(ERROR_OCCUPIED)
    return True
  return False

def validCoord(coord):
  if len(coord) != 2:
    return False
  
  try:
    field = coordToNums(coord)
  except:
    return False
  
  if not fieldInRange(field):
    return False

  return True

def fieldFull():
  for row in game_field:
    if 0 in row:
      return False
  return True

# returns number of stones that would be flipped of a player placed their stone
def turnStoneFlips(player, field):
  flippedStonesTotal = []
  
  opponent = (player % 2) + 1

  if fieldOccupied(field):
    return []

                                #up, up-right, right, down-right, down, down-left, left, up-left
  for offset_col, offset_row in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)):
    turnToCheck = list(field)
    turnToCheck[0] += offset_col
    turnToCheck[1] += offset_row

    if not fieldInRange(turnToCheck):
      continue

    flippedStonesCurDir = []

    outOfField = False

    while(fieldValue(turnToCheck) == opponent):
      flippedStonesCurDir.append(turnToCheck.copy())

      turnToCheck[0] += offset_col
      turnToCheck[1] += offset_row
      if not fieldInRange(turnToCheck):
        outOfField = True
        break
    
    if outOfField:
      continue

    if fieldValue(turnToCheck) == player:
      flippedStonesTotal.extend(flippedStonesCurDir)

  return flippedStonesTotal

def allTurnsPoints(player):
  turns = []
  for row in range(0,8):
      for column in range(0,8):
        field = (row,column)
        if fieldValue(field) == 0:
          points = len(turnStoneFlips(player,field))
          if points > 0:
            turns.append((field, points))
  
  random.shuffle(turns)
  turns.sort(key=lambda tupl: tupl[1], reverse=True)
  return turns

def turnPossible(player, field):
  return len(turnStoneFlips(player, field)) > 0

def anyTurnPossible(player):
  return len(allTurnsPoints(player)) > 0

def playStone(player, field):
  for fieldToFlip in turnStoneFlips(player, field):
    setStone(player, fieldToFlip)

  setStone(player, field)

def setStone(player, field):
  game_field[field[0]][field[1]] = player

def playTurnAi():
  possibleTurns = allTurnsPoints(2)

  if len(possibleTurns) <= 0:
    print(PROMPT_AI + INPUT_SKIP)
    return INPUT_SKIP

  coord = numsToCoord(possibleTurns[0][0])

  print(PROMPT_AI + coord)

  return coord

def playTurnHuman(mode, player):
  #input
  if player == 1:
    inp = input(PROMPT_PLAYER_1).lower()
  elif player == 2 and mode == MODE_HUMAN:
    inp = input(PROMPT_PLAYER_2).lower()
  elif player == 2 and mode == MODE_AI:
    inp = playTurnAi().lower()
  
  #process input
  if inp == INPUT_SKIP:
    if anyTurnPossible(player):
      print(ERROR_INVALID_INPUT)
      return TURN_ERROR
    return TURN_SKIP
  elif inp == INPUT_QUIT:
    return TURN_QUIT
  elif validCoord(inp):
    field = coordToNums(inp)

    if not turnPossible(player, field):
      print(ERROR_NOT_ALLOWED)
      return TURN_ERROR

    playStone(player, field)

    return TURN_PLACED_STONE
  else:
    print(ERROR_INVALID_INPUT)
    return TURN_ERROR

def main():
  #prompt AI or human
  mode = ""
  while(mode == ""):
    inp = str(input(PROMPT_HUMAN_AI)).lower()

    if inp == INPUT_COMPUTER:
      mode = MODE_AI
    elif inp == INPUT_HUMAN:
      mode = MODE_HUMAN
    else:
      print(ERROR_INVALID_INPUT)

  player = 1

  #play
  printBoard(game_field)

  lastPlay = -1

  while(True):
    turnResult = playTurnHuman(mode, player)

    printBoard(game_field)

    if turnResult == TURN_ERROR:
      continue
    elif turnResult == TURN_QUIT:
      return 0

    player = (player % 2) + 1

    # if no more moves possible, print results
    if fieldFull() or (turnResult == TURN_SKIP and lastPlay == TURN_SKIP):
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
    
    lastPlay = turnResult

if __name__ == "__main__":
  main()
