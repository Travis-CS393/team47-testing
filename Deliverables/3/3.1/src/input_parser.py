import json
from stone import Stone
from constants import BOARD_DIM
from point import Point, str_to_point
from board import Board

class InputParser():

   def __init__(self, input_array):
      self.board_matr = input_array[0]
      self.statement_arr = input_array[1]

   def get_board(self):
      return Board([[Stone(self.board_matr[i][j]) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

   def get_statement(self):
      return self.statement_arr[0]

   def get_point(self):
      return str_to_point(self.statement_arr[1])
   
   def get_stone(self):
      return Stone(self.statement_arr[1]).get_type()

   def get_stone_and_point(self):
      return Stone(self.statement_arr[1]).get_type(), str_to_point(self.statement_arr[2])
   
   def get_point_and_stone(self):
      return str_to_point(self.statement_arr[1]), Stone(self.statement_arr[2]).get_type()