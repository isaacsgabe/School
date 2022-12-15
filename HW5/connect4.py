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


def get_valid_location(board):
    validLoctns = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            validLoctns.append(col)
    return validLoctns


#picks the best move using the heuristic that professor Rosenfeld gave us
def pickBestMove(board,peice):
    valid_pos = get_valid_locations(board)
    bestCol = random.choice(valid_pos)
    for col in valid_pos:
        tmp = copy.deepcopy(board)
        row = get_next_open_row(tmp,col)      
        drop_chip(tmp,row,col,peice)
        if (game_is_won(tmp, peice)):
            bestCol = col  
            break
    if peice == BLUE_INT:
            peice = RED_INT
    else:
            peice = BLUE_INT
    for col in valid_pos:
        tmp = copy.deepcopy(board)
        row = get_next_open_row(tmp,col)      
        drop_chip(tmp,row,col,peice)
        if (game_is_won(tmp, peice)):
            bestCol = col  
            break
    return bestCol

def play_out_game(board,color):
    # plays out the game using the monte Carlo Algortithm

    #creates a list of amount of times blue wins in each column
    totals =[]
    change = color

    #put the peice in each of the 7 columns
    for x in range(0,7):
        color = change
        winningboard = copy.deepcopy(board)

        #if a column is full don't go there.
        row = get_next_open_row(board, x)
        if row ==None:
            totals.append(-100)
            continue
        drop_chip(winningboard, row, x, color)
        if color == BLUE_INT:
            color = RED_INT
        else:
            color = BLUE_INT

        #set a counter for how many times each peice won
        red = 0
        blue = 0

        #play out the game 30 times
        for y in range(0,30):
            num = 0
            play_out_game = copy.deepcopy(winningboard)
            while True:
                num+=1
                columns = get_valid_locations(play_out_game)
                if len(columns) == 0:
                    break
                if color == BLUE_INT:
                    #use the heuristic the professor gave us for blue
                    colToPut = pickBestMove(play_out_game,color)
                    r = get_next_open_row(play_out_game,colToPut)
                    drop_chip(play_out_game,r,colToPut,color)
                    if game_is_won(play_out_game,BLUE_INT):
                        blue+=1
                        break
                    color = RED_INT
                else:
                    #use the heuristic the professor gave us for red
                    colToPut = pickBestMove(play_out_game,color)
                    r = get_next_open_row(play_out_game,colToPut)
                    drop_chip(play_out_game,r,colToPut,color)
                    if game_is_won(play_out_game,RED_INT):
                        red+=1
                        break
                    color = BLUE_INT

        #add the total amount of times blue wins to list of spots the decide which is the best mve to make
        totals.append(blue)
    return totals
# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
red = 0
blue = 0
turn = 0
draw = 0

#play the game 10 times
for i in range(0,10):
    board = create_board()
    print_board(board)
    game_over = False


    while not game_over:
        if turn % 2 == 0:
            #Use professors heurisitic for blue
            colToPut = pickBestMove(board,RED_INT)
            r = get_next_open_row(board,colToPut)
            drop_chip(board,r,colToPut,RED_INT)

        if turn % 2 == 1 and not game_over:
            """
            assess state of the board = getvalue(board)
            get the next states of the board
                for each of  the next state
                if the value of the board is more than you have seen so far then keep that board11
            """

            #get the best columns from the mc algorithm
            next_column = play_out_game(board,BLUE_INT)
            num = max(next_column)
            listOfind = []
            for i in range(0,len(next_column)):
                if next_column[i] == num:
                    listOfind.append(i)

            #if 2 spots are just as good pick a random one
            indexBl = random.choice(listOfind)
            row = get_next_open_row(board, indexBl)
            drop_chip(board, row, indexBl, BLUE_INT)

        print_board(board)
        print()
        
        if game_is_won(board, RED_INT):
            red +=1
            game_over = True
            print(colored("Red wins!", 'red'))
        if game_is_won(board, BLUE_INT):
            blue += 1
            game_over = True
            print(colored("Blue wins!", 'blue'))
        if len(get_valid_locations(board)) == 0:
            draw +=1
            game_over = True
            print(colored("Draw!", 'blue'))
        turn += 1

#print final score
print("Red:" + str(red))
print("Blue:" + str(blue))
print("Draw:" + str(draw))

#tmp = copy.deepcopy(board)