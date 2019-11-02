import sys
from constants import WHITE_STONE, BLACK_STONE, EMPTY_STONE
from enum import Enum

class StoneEnum(Enum):
   WHITE = 1
   BLACK = 2

class Stone():
   def __init__(self, s):
      if s == EMPTY_STONE:
         self.stone_type = None
      elif s == WHITE_STONE:
         self.stone_type = StoneEnum.WHITE
      elif s == BLACK_STONE:
         self.stone_type = StoneEnum.BLACK
      else:
         raise Exception("invalid maybe_stone input")
   
   def set_type(self, stone_type):
      self.stone_type = stone_type

   def get_type(self):
      return self.stone_type

   def get_raw(self):
      stone_type = self.get_type()
      if not stone_type:
         return EMPTY_STONE
      if stone_type is StoneEnum.WHITE:
         return WHITE_STONE
      return BLACK_STONE

def make_stone(stone_type):
   if stone_type == StoneEnum.WHITE:
      return Stone(WHITE_STONE)
   elif stone_type == StoneEnum.BLACK:
      return Stone(BLACK_STONE)
   elif stone_type == None:
      return Stone(EMPTY_STONE)
   else:
      raise Exception("Invalid stone type passed")

def get_other_type(stone_type):
   if stone_type == StoneEnum.WHITE:
      return StoneEnum.BLACK
   elif stone_type == StoneEnum.BLACK:
      return StoneEnum.WHITE
   else:
      raise Exception("Invalid input to get other type")
