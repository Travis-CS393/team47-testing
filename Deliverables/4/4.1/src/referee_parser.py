import sys
sys.path.append('../../3/3.1/src/')
from constants import BOARD_DIM
from board import Board
from stone import Stone
from point import str_to_point
from move_referee import MoveReferee

def is_board(arr):
   return len(arr) == BOARD_DIM

def is_move(arr):
   return len(arr) == 2

def parse_board(matr):
   return Board([[Stone(matr[i][j]) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

def parse_move(arr):
   if isinstance(arr[1], str):
      return Stone(arr[0]).get_type(), arr[1]
   else:
      return Stone(arr[0]).get_type(), [str_to_point(arr[1][0]), [parse_board(board) for board in arr[1][1]]]