import copy
from pickle import FALSE
import numpy as np
import math
import random
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board():
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip):
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip


def is_valid_location(board, col):
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace("1", RED_CHAR).replace("2", BLUE_CHAR).replace("\n", "|\n") + "|")

def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :]))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c]))):
            return True
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def MoveRandom(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(valid_locations)   # you can replace with input if you like... -- line updated with Gilad's code-- thanks!
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

def evalWind(windowLength,AI):
    #this is my heuristic and will see how good a board is
    score = 0
    player2 = RED_INT
    if AI == RED_INT:
        player2 == BLUE_INT
    #if we can win go here
    if windowLength.count(AI) == 4:
        score += 100
    #if we can get 2 in a row or 3 in a row go here
    elif windowLength.count(AI) == 3 and  windowLength.count(EMPTY) == 1:
        score += 10
    elif windowLength.count(AI) == 2 and  windowLength.count(EMPTY) == 2:
        score += 5
    if windowLength.count(player2) == 3 and  windowLength.count(EMPTY) == 1:
        score -= 100
    if windowLength.count(player2) == 3 and  windowLength.count(EMPTY) == 1:
        score -= 7
    elif windowLength.count(player2) == 2 and  windowLength.count(EMPTY) == 2:
        score -= 2
    return score
#create heuristic to calculate the value of a board
# peiceValue = is it AI turn or or is it a pleayers turn?
def evaluate(board,AI):
    #score horizontal
    global turn
    score = 0

    #score center column (preferance the middle of the board) (only for the first 3 turns)
    if turn <= 2:
        center_array = [int(j) for j in list(board[:,COLUMN_COUNT//2])]
        center_count = center_array.count(AI)
        score +=  center_count

    #score this window vertically horizontally and d3iagnally
    for i in range(ROW_COUNT):
        if i < 4:
            score += 3
        #get the peices in the row
        row_array= [int(j) for j in list(board[i,:])]
        #look for the possible 4 combinations
        for c in range(COLUMN_COUNT-3):
            windowLength = row_array[c:c+4]
            score += evalWind(windowLength,AI)
            

    #score verticle
    for i in range(COLUMN_COUNT):
        col_array = [int(j) for j in list(board[:,i])]
        for c in range(ROW_COUNT-3):
            windowLength = col_array[c:c+4]
            score += evalWind(windowLength,AI)

    #score diagnal(positive)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            windowLength = [board[r+i][c+i] for i in range(4)]
            score += evalWind(windowLength,AI)

    #score negative diagnol 
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            windowLength = [board[r+3-i][c+i] for i in range(4) ]
            score += evalWind(windowLength,AI)
    return score

def is_ending_board(board):
    return game_is_won(board,RED_INT) or game_is_won(board,BLUE_INT) or len(get_valid_location(board)) == 0


#min/max algorithm
def alphaBeta(board,depth,a,b,maximizingPlayer):
    #us winnig, them winning, no more peices]
    valid_location = get_valid_locations(board)
    ending_board = is_ending_board(board)
    if depth == 0 or ending_board:
        #if we are AI and we won
        if ending_board:
            if game_is_won(board,BLUE_INT):
                return (None,100)
            elif game_is_won(board,RED_INT):
                return (None,-100)
            else: #no more valid moves
                return (None,0)
        else: # depth is 0 and we need to find heuristic of board
            return (None,evaluate(board,BLUE_INT))
    if maximizingPlayer:
        value = - math.inf
        bestColumn = random.choice(valid_location)
        for col in valid_location:
            #put a peice in every move and which is best
            row = get_next_open_row(board, col)
            board2 = copy.deepcopy(board)
            drop_chip(board2,row,col,BLUE_INT)
            #based on this move keep finiding the best move on a lower level
            newScore = alphaBeta(board2,depth-1,a,b,False)[1]
            #alpha beta pruning
            if newScore > value:
                value = newScore
                bestColumn = col
            a = max(a,value)
            if a >= b:
                break
        return bestColumn,value
    else: 
        #minimizing player
        value = math.inf
        bestColumn = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            board2 = copy.deepcopy(board)
            drop_chip(board2,row,col,RED_INT)
            newScore = alphaBeta(board2,depth-1,a,b,True)[1]
            #alpha beta pruning
            if newScore < value:
                value = newScore
                bestColumn = col
            a = min(a,value)
            if a >= b:
                break
        #return the best column and the best Value
        return bestColumn, value

def get_valid_location(board):
    validLoctns = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            validLoctns.append(col)
    return validLoctns

def pickBestMove(board, peice):
    validlctns = get_valid_locations(board)
    bestScore = -10000
    bestCol = random.choice(validlctns)
    #simulate the move
    for col in validlctns:
        row = get_next_open_row(board,col)
        holder_board = copy.deepcopy(board)
        drop_chip(holder_board,row,col,peice)
        score = evaluate(holder_board,peice)
        if score > bestScore:
            bestScore = score
            bestCol = col
    return bestCol

def agent1move(board):
  col,score = alphaBeta(board,3,-math.inf,math.inf,True)
  return col
# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
turn = 0

board = create_board()
print_board(board)
game_over = False

while not game_over:
    if turn % 2 == 0:
        col = int(input("RED please choose a column(1-7): "))
        while col > 7 or col < 1:
            col = int(input("Invalid column, pick a valid one: "))
        while not is_valid_location(board, col - 1):
            col = int(input("Column is full. pick another one..."))
        col -= 1

        row = get_next_open_row(board, col)
        drop_chip(board, row, col, RED_INT)

    if turn % 2 == 1 and not game_over:
        """
        assess state of the board = getvalue(board)
        get the next states of the board
            for each of  the next state
            if the value of the board is more than you have seen so far then keep that board11
        """
        col = agent1move(board)
        row = get_next_open_row(board, col)
        drop_chip(board, row, col, BLUE_INT)
        # MoveRandom(board,BLUE_INT)

    print_board(board)
    print()
    
    if game_is_won(board, RED_INT):
        game_over = True
        print(colored("Red wins!", 'red'))
    if game_is_won(board, BLUE_INT):
        game_over = True
        print(colored("Blue wins!", 'blue'))
    if len(get_valid_locations(board)) == 0:
        game_over = True
        print(colored("Draw!", 'blue'))
    turn += 1

#tmp = copy.deepcopy(board)