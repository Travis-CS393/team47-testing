import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../5.1/src/')
from copy import deepcopy
from stone import get_other_type
from point import Point
from go_player_base import GoPlayerBase
from move_referee import MoveReferee

class GoPlayerAdv(GoPlayerBase):

   def __init__(self, n = 1):
      super().__init__()
      self.n = n
   
   def choose_move(self, boards):
      if not self.move_referee.valid_history(self.stone_type, boards):
         return "This history makes no sense!"
      ret = self._choose_move_recur(boards, boards[0], self.n)
      return ret if ret else super().choose_move(boards)
   
   def _choose_move_recur(self, hist, curr, n):
      if n is 1:
         return self._choose_move_base(hist, curr)
      else: 
         for x, y in sorted(list(self._get_valid_moves(hist, curr))):
            next1 = deepcopy(curr)
            next1.place_and_update(self.stone_type, Point(x, y))
            for x2, y2 in sorted(list(self._get_valid_moves(hist, curr))):
               next2 = deepcopy(next1)
               next2.place_and_update(get_other_type(self.stone_type), Point(x2, y2))
               ret = self._choose_move_recur(hist, next2, n - 1)
               if ret:
                  return (x, y)
         return None
   
   def _choose_move_base(self, hist, curr):
      for x, y in sorted(list(self._get_valid_moves(hist, curr))):
         point = Point(x, y)
         if self._move_captures(curr, point):
            return (x, y)
      return None

   def _move_captures(self, board, point):
      test_board = deepcopy(board)
      other = get_other_type(self.stone_type)
      before = len(test_board.get_points(other))
      test_board.place_and_update(self.stone_type, point)
      return len(test_board.get_points(other)) < before

   def _get_valid_moves(self, hist, curr):
      empty = curr.get_points(None)
      out = filter(lambda tpl: self.move_referee.valid_move(self.stone_type, Point(tpl[0], tpl[1]), hist, curr), empty)
      return set(out)