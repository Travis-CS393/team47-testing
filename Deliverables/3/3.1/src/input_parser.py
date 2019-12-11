import json
from stone import Stone
from constants import BOARD_DIM
from point import Point, str_to_point
from board import Board

class InputParser():

   def __init__(self, input_array):
      """
      This class implements an InputParser that takes in a string array
      and returns the statement or other information as game objects with 
      our internal representation.

      Ex. input_array has forms: 
      [Board, Statement]
      where Board is a dim x dim 2D array of MaybeStone representing a Go Board
      where MaybeStone is one of Stone or Empty 
         where Stone is one of "B" or "W"
         where Empty is " "
      where Statement is one of Command or Query
      where Query is one of 
         -["occupied?", Point]
         -["occupies?", Stone, Point]
         -["reachable?", Point, MaybeStone]
      where Command is one of 
         -["place", Stone, Point] 
         -["remove", Stone, Point] 
         -["get-points", MaybeStone]
      where Point is a string in form "N-N" and N is within dim size
      """
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

      