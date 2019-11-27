import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from stone import Stone, StoneEnum, get_other_type
from board import Board
from point import Point, str_to_point
from copy import deepcopy
from move_referee import MoveReferee
from score_referee import ScoreReferee
from constants import BOARD_DIM, PASS, EMPTY_STONE
from obj_parser import parse_board
from output_formatter import format_board_if_valid, format_board, format_one_board
from play_parser import get_board

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
      self.board_history = [get_board([[" "] * self.board_size for row in range(self.board_size)])]

      self.player1 = player1
      self.player2 = player2
      self.players = {StoneEnum.BLACK: None, StoneEnum.WHITE: None}
      self.current_player = StoneEnum.BLACK

      self.move_ref = MoveReferee()
      self.score_ref = ScoreReferee()

      self.game_over = False
      self.winner_declared = False
      self.winner = None

   def decide_stones(self):
      pass

   ## Public Methods
   def referee_game(self):
      # Play game after registration complete 
      self.play_black_move()

      if self.game_over:
         return

      self.play_white_move()

   def play_black_move(self):
      p = self.players[StoneEnum.BLACK].choose_move(self.board_history)
      if self.validate_player_move(p):
         if isinstance(p, str):
            if p == "pass":
               self.execute_move(p)
            else:            
               p = p.replace("\"","").replace("\n","")
               self.execute_move(str_to_point(p))
         elif isinstance(p, tuple):
            self.execute_move(Point(p[0], p[1]))
      else:
         raise TypeError("Invalid responded move")

   def play_white_move(self):
      p = self.players[StoneEnum.WHITE].choose_move(self.board_history)
      if self.validate_player_move(p):
         if isinstance(p, str):
            if p == "pass":
               self.execute_move(p)
            else:
               p = p.replace("\"","").replace("\n","")
               self.execute_move(str_to_point(p))
         elif isinstance(p, tuple):
            self.execute_move(Point(p[0], p[1]))
      else:
         raise TypeError("Invalid responded move")

   def validate_player_move(self, check_response):
      if check_response == "pass":
         return True
      elif isinstance(check_response, tuple):
         return True
      elif isinstance(check_response, str):
         check_response_tmp = check_response.replace("\"","").replace("\n","").split("-")
         if len(check_response_tmp) != 2:
            return False
         elif int(check_response_tmp[0]) < 1 or int(check_response_tmp[0]) > 9:
            return False
         elif int(check_response_tmp[0]) < 1 or int(check_response_tmp[0]) > 9:
            return False
         else:
            return True

   def execute_move(self, move):
      if (not self.game_over):
         old_history = deepcopy(self.board_history)
         if (move == PASS):
            add_board = old_history[0]
            self.update_history(add_board)

            # Check for both players consecutive passes 
            if len(self.board_history) == 3:
               if self.board_history[0].equal(self.board_history[1]) and self.board_history[1].equal(self.board_history[2]):
                  self.game_over = True
         elif isinstance(move, Point):
            if (self.move_ref.valid_move(self.current_player, move, self.board_history, self.board_history[0])):
               add_board = self.make_move(self.current_player, move)
               self.update_history(add_board)
            else:
               self.game_over = True
               self.winner = get_other_type(self.current_player)
         else:
            raise Exception("Not a valid move.")
         self.current_player = get_other_type(self.current_player)
         return old_history

   def make_move(self, stone, point):
      last_board = deepcopy(self.board_history)[0]
      new_board = last_board.place_and_update(stone, point)
      return new_board

   def update_history(self, board):
      old_history = deepcopy(self.board_history)
      if (len(old_history) == 1):
         new_history = [board, old_history[0]]
         self.board_history = new_history
      if ((len(old_history) == 2) or (len(old_history) == 3)):
         new_history = [board, old_history[0], old_history[1]]
         self.board_history = new_history

   def get_winners(self):
      if (self.winner != None):
         return [self.players[self.winner].name]
      else:
         final_score = self.score_ref.get_score(self.board_history[0])
         black_score = final_score[StoneEnum.BLACK]
         white_score = final_score[StoneEnum.WHITE]

         if black_score > white_score:
            return [self.players[StoneEnum.BLACK].name]
         elif white_score > black_score:
            return [self.players[StoneEnum.WHITE].name]
         else:
            tied_game = [self.players[StoneEnum.BLACK].name, self.players[StoneEnum.WHITE].name]
            tied_game = sorted(tied_game)
            return tied_game




"""
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
      self.board_history = [get_board([[" "] * self.board_size for row in range(self.board_size)])]
      
      self.players = {StoneEnum.BLACK: player1, StoneEnum.WHITE: player2}
      self.current_player = StoneEnum.BLACK

      self.move_ref = MoveReferee()
      self.score_ref = ScoreReferee()
      
      self.game_over = False
      self.winner_declared = False
      self.winner = None
     
   ## Public Method

   def execute_move(self, move):

      if (not self.game_over):
         old_history = deepcopy(self.board_history)
         if (move == PASS):
            add_board = old_history[0]
            self.update_history(add_board)
            forced_equality = []
            for board in self.board_history:
               forced_equality.append(format_one_board(board))
               
            if (len(forced_equality) == 3):
               if ((forced_equality[0] == forced_equality[1]) and (forced_equality[1] == forced_equality[2])):
                  self.game_over = True
               #return self.get_winners()
         elif isinstance(move, Point):
               if (self.move_ref.valid_move(self.current_player, move, self.board_history, self.board_history[0])):
                  add_board = self.make_move(self.current_player, move)
                  self.update_history(add_board)
               else:
                  self.game_over = True
                  self.winner = get_other_type(self.current_player)
                  #return self.get_winners()
         else:
            raise Exception("Not a valid move.")
         self.current_player = get_other_type(self.current_player)
         return old_history


   def make_move(self, stone, point):
      last_board = deepcopy(self.board_history)[0]
      new_board = last_board.place_and_update(stone, point)
      return new_board

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
"""
