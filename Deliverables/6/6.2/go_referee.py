import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from stone import Stone, StoneEnum, get_other_type
from board import Board
from point import Point
from copy import deepcopy
from move_referee import MoveReferee
from score_referee import ScoreReferee
from constants import BOARD_DIM, PASS, EMPTY_STONE
from obj_parser import parse_board
from output_formatter import format_board_if_valid


class GoReferee:

   ## Validators
   def valid_stone(func):
      def wrapper(*args, **kwargs):
         if not args[1] or not isinstance(args[1], StoneEnum):
            raise Exception("Invalid Parameter: bad stone passed")
         return func(*args, **kwargs)
      return wrapper

   ## Class Variables
   

   ## Constructors
   def __init__(self, board_size=None, board=None, player1=None, player2=None):
      self.board_size = BOARD_DIM if board_size is None else board_size
      self.board_history = [Board([[Stone(EMPTY_STONE)] * self.board_size for row in range(self.board_size)] if board is None else board)]
      
      self.players = {StoneEnum.BLACK: player1, StoneEnum.WHITE: player2}
      self.current_player = StoneEnum.BLACK

      self.move_ref = MoveReferee()
      self.score_ref = ScoreReferee()
      
      self.game_over = False
      self.winner_declared = False
      self.winner = None
     
   ## Public Method

   def execute_move(self, move):
      if self.game_over:
         if self.winner_declared:
            return
         else:
            self.winner_declared = True
            return self.get_winners()
         
      old_history = deepcopy(self.board_history)
      if move == PASS:
         self.execute_pass()
      elif isinstance(move, Point):
         self.execute_place(move)
      self.current_player = get_other_type(self.current_player)
      return old_history

   def execute_pass(self):
      add_board = self.board_history[0]
      self.update_history(add_board)

      if ((self.board_history[0] == self.board_history[1]) and (self.board_history[1] == self.board_history[2])):
         self.game_over = True

   def execute_place(self, point):
      if (self.move_ref.valid_move(self.current_player, point, self.board_history, self.board_history[0])):
         add_board = self.make_move(self.current_player, point)
         self.update_history(add_board)
      else:
         self.game_over = True
         self.winner = get_other_type(self.current_player)

   def make_move(self, stone, point):
      last_board = deepcopy(self.board_history)[0]
      return last_board

   def update_history(self, board):
      old_history = deepcopy(self.board_history)
      if (len(old_history) == 1):
         new_history = [board, old_history[0]]
         self.board_history = new_history

      if ((len(old_history) == 2) or (len(old_history) == 3)) :
         new_history = [board, old_history[0], old_history[1]]
         self.board_history = new_history

   def get_winners(self):
      if (self.winner != None):
         return [self.players[self.winner]]
      else:
         final_score = self.score_ref.get_score(self.board_history[0])
         black_score = final_score[StoneEnum.BLACK]
         white_score = final_score[StoneEnum.WHITE]

         if black_score > white_score:
            return [self.players[StoneEnum.BLACK]]
         elif white_score > black_score:
            return [self.players[StoneEnum.WHITE]]
         else:
            tied_game = [self.players[StoneEnum.BLACK], self.players[StoneEnum.WHITE]]
            tied_game = sorted(tied_game)
            return tied_game

