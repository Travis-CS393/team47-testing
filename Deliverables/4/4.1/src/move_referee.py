import sys
sys.path.append('../../3/3.1/src/')
from copy import copy, deepcopy
from constants import PASS
from board import Board
from stone import StoneEnum, get_other_type
from point import Point

class MoveReferee:

   ## Validators
   def validate_stone(func):
      def wrapper(*args, **kwargs):
         if not args[1]:
            raise Exception("Invalid stone passed")
         return func(*args, **kwargs)
      return wrapper

   ## Public Methods
   @validate_stone
   def valid_play(self, stone_type, move):
      if move == PASS:
         return True
      point, boards = move
      current_board = boards[0]
      return self.valid_move(stone_type, point, boards, current_board) and \
             self.valid_history(stone_type, boards)


   @validate_stone
   def valid_move(self, stone_type, point, boards, current_board):
      return self._check_valid_point(current_board, point) and \
             self._check_ko(boards, stone_type, point) and \
             self._check_will_suicide(current_board, stone_type, point)

   @validate_stone
   def valid_history(self, stone_type, boards):
      return self._check_ko(boards, stone_type) and \
             self._check_history_prog(boards, stone_type) and \
             self._check_history_states(boards)

   ## Private Methods
   def _check_valid_point(self, board, point):
      return not board.occupied(point)

   def _check_ko(self, boards, stone_type, point=None):
      boards_lst = copy(boards)
      if point:
         test_board = deepcopy(boards[0])
         test_board.place_and_update(stone_type, point)
         boards_lst += [test_board]
      for i in range(len(boards_lst)):
         for j in range(i+2, len(boards_lst)):
            board1, board2 = boards_lst[i], boards_lst[j]
            if board1.equal(board2): 
               return False
      return True

   def _check_will_suicide(self, board, stone_type, point):
      test_board = deepcopy(board)
      test_board.place_and_update(stone_type, point)
      return test_board.get_type(point) != None

   def _check_history_states(self, boards):
      for board in boards:
         for x,y in list(board.get_points(StoneEnum.WHITE)):
            if not board.reachable(Point(x, y), None):
               return False
         for x,y in list(board.get_points(StoneEnum.BLACK)):
            if not board.reachable(Point(x, y), None):
               return False
      return True

   def _check_history_prog(self, boards, stone_type):
      if not self._valid_start(boards, stone_type):
         return False
      passes = int(len(boards) == 3 and boards[2].empty() and stone_type == StoneEnum.WHITE)
      max_passes = passes
      for i in range(len(boards) - 1, 0, -1):
         curr_board, next_board = boards[i], boards[i-1]
         mover = self._get_history_mover(i, stone_type)
         if curr_board.equal(next_board):
            passes += 1
         elif not self._valid_step(curr_board, mover, next_board):
            return False
         else:
            max_passes = max(max_passes, passes)
            passes = 0
      max_passes = max(max_passes, passes)
      return max_passes < 2

   def _valid_start(self, boards, stone_type):
      if len(boards) == 1:
         if stone_type != StoneEnum.BLACK:
            return False
         elif not boards[0].empty():
            return False
      if len(boards) == 2:
         if stone_type != StoneEnum.WHITE:
            return False
         elif not boards[1].empty():
            return False
         elif len(boards[0].get_points(StoneEnum.WHITE)) > 1:
            return False
      return True

   def _get_history_mover(self, i, stone_type):
      if i % 2:
         return get_other_type(stone_type)
      return stone_type

   def _valid_step(self, curr_board, mover, next_board):
      othr_mvr = get_other_type(mover)
      curr_mvr_pts, next_mvr_pts = curr_board.get_points(mover), next_board.get_points(mover)
      curr_othr_pts, next_othr_pts = curr_board.get_points(othr_mvr), next_board.get_points(othr_mvr)
      move = next_mvr_pts.difference(curr_mvr_pts)
      if len(move) is 0:
         return curr_board.equal(next_board)
      elif len(move) is 1:
         mv_x, mv_y = list(move)[0]
         test_board = deepcopy(curr_board)
         test_board.place_and_update(mover, Point(mv_x, mv_y))
         if not test_board.equal(next_board):
            return False
      else: 
         return False
      return True