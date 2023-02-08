import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from random import randint

f = open('databaseURL.txt','r')
contents = f.read()
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': contents
})
f.close()
board = []

for x in range(0, 5):
  board.append(["O"] * 5)

def print_board(board):
  for row in board:
    print(" ".join(row))

print_board(board)

def random_row(board):
  return randint(0, len(board) - 1)

def random_col(board):
  return randint(0, len(board[0]) - 1)

ref = db.reference('/game')
game_data = ref.get()

if not game_data:
    ship_row = random_row(board)
    ship_col = random_col(board)
    print(ship_row)
    print(ship_col)

    ref.update({
        'ship_row': ship_row,
        'ship_col': ship_col
    })
else:
    ship_row = game_data['ship_row']
    ship_col = game_data['ship_col']

for turn in range(4):
  print("Turn", turn + 1)
  guess_row = int(input("Guess Row: "))
  guess_col = int(input("Guess Col: "))

  if guess_row == ship_row and guess_col == ship_col:
    print("Congratulations! You sank my battleship!")
    ref.update({
        'result': 'Win'
    })
    break
  else:
    if guess_row not in range(5) or \
      guess_col not in range(5):
      print("Oops, that's not even in the ocean.")
    elif board[guess_row][guess_col] == "X":
      print("You guessed that one already.")
    else:
      print("You missed my battleship!")
      board[guess_row][guess_col] = "X"
    print_board(board)
  if (turn == 3):
    print("Game Over")
    ref.update({
        'result': 'Loss'
    })