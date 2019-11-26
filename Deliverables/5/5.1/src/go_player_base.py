import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from stone import StoneEnum
from move_referee import MoveReferee
from point import Point
from output_formatter import format_board

class GoPlayerBase:

   ## Decorators
   def valid_stone(func):
      def wrapper(*args, **kwargs):
         if not args[1] or not isinstance(args[1], StoneEnum):
            raise Exception("Invalid Parameter: bad stone passed")
         return func(*args, **kwargs)
      return wrapper

   def protocol_registered(func):
      def wrapper(*args, **kwargs):
         if not args[0].name:
            raise Exception("Invalid Protocol: Player must be registered first.")
         return func(*args, **kwargs)
      return wrapper

   def protocol_stone_set(func):
      def wrapper(*args, **kwargs):
         if not args[0].stone_type:
            raise Exception("Invalid Protocol: Stone must be received first.")
         return func(*args, **kwargs)
      return wrapper

   ## Constructor
   def __init__(self, name):
      self.name = None
      self.default_name = "default_player"
      self.stone_type = None
      self.move_referee = MoveReferee()

   ## Public Methods
   def register(self):
      if not self.name:
         self.name = self.default_name
      return self.name

   @valid_stone
   @protocol_registered
   def receive_stone(self, stone_type):
      self.stone_type = stone_type

   @protocol_registered
   @protocol_stone_set
   def choose_move(self, boards):
      if not self.move_referee.valid_history(self.stone_type, boards):
         print(format_board(boards))
         return "This history makes no sense!"
      for x, y in sorted(list(boards[0].get_points(None))):
         if self.move_referee.valid_move(self.stone_type, Point(x, y), boards, boards[0]):
            return (x, y)
      return "pass"

   def game_over(self, end_tag):
      # Reset default player for next game
      self.stone_type = None
      self.move_referee = MoveReferee()
      return "OK"