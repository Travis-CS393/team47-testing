import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from stone import StoneEnum
from move_referee import MoveReferee
from score_referee import ScoreReferee
from go_player_base import GoPlayerBase

class GoReferee:

   ## Validators

   ## Class Variables
   move_ref = MoveReferee()
   score_ref = ScoreReferee()
   players = {StoneEnum.BLACK: None, StoneEnum.WHITE: None}

   ## Constructors
   def __init__(self, board_size=None, board=None, player1=None, player2=None):
      self.board_size = 19 if board_size is None else board_size
      self.board = [[ [" "] * self.board_size for row in range(self.board_size)]] if board is None else board
      self.player1 = "no name" if player1 is None else GoPlayerBase(player1, StoneEnum.BLACK)
      self.player2 = "no name" if player2 is None else GoPlayerBase(player2, StoneEnum.WHITE)

   ## Public Methods
   def register_player(self, stone_type, name):
      pass

   def execute_move(self, point):
      pass

   def get_winners(self):
      pass