import sys
sys.path.append('../../3/3.1/src/')
from point import Point, str_to_point
from constants import PASS, BOARD_DIM
from board import Board
from stone import Stone

def format_input(string):
	if string == PASS:
		return "pass"
	else:
		return str_to_point(string)

def get_board(board_matr):
	return Board([[Stone(board_matr[i][j]) for i in range(len(board_matr))] for j in range(len(board_matr))])