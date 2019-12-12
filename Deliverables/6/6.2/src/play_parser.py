import sys
sys.path.append('../../../3/3.1/src/')
from point import Point, str_to_point
from board import Board
from stone import Stone
from constants import PASS, BOARD_DIM

# Play Parser handles converting python input into game object representation. 

def format_input(string):
	if string == PASS:
		return PASS
	else:
		return str_to_point(string)

def get_board(board_matr):
     return Board([[Stone(board_matr[i][j]) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])