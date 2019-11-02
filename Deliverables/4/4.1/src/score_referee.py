import sys
sys.path.append('../../3/3.1/src/')
from board import Board
from stone import StoneEnum
from point import Point

class ScoreReferee:

   ## Validators
   def validate_board(func):
      def wrapper(*args, **kwargs):
         if not isinstance(args[1], Board):
            raise Exception("Invalid board passed")
         return func(*args, **kwargs)
      return wrapper

   ## Public Methods
   @validate_board
   def get_score(self, board):
      score = {StoneEnum.WHITE: 0, StoneEnum.BLACK: 0}
      self._update_score_basic(board, score, StoneEnum.WHITE)
      self._update_score_basic(board, score, StoneEnum.BLACK)
      self._update_score_empty_stones(board, score)
      return score

   ## Private Methods
   def _update_score_basic(self, board, score, stone_type):
      score[stone_type] += len(board.get_points(stone_type))

   def _update_score_empty_stones(self, board, score):
      seen = {}
      points = board.get_points(None)
      for tupl in points:
         x, y = tupl
         if tupl not in seen:
            white_reachable = board.reachable(Point(x, y), StoneEnum.WHITE)
            black_reachable = board.reachable(Point(x, y), StoneEnum.BLACK)
            if white_reachable and not black_reachable:
               self._mark_adjacent(board, seen, tupl, StoneEnum.WHITE)
            elif black_reachable and not white_reachable:
               self._mark_adjacent(board, seen, tupl, StoneEnum.BLACK)
            else:
               self._mark_adjacent(board, seen, tupl, None)
      self._update_by_seen(score, seen)

   def _mark_adjacent(self, board, seen, tupl, stone_type):
      x, y = tupl
      if tupl not in seen:
         seen[(x,y)] = stone_type
         neighbors = board.get_neighbors(Point(x, y))
         neighbors = list(filter(lambda tupl: board.get_type(Point(tupl.x, tupl.y)) == None, neighbors))
         for adj_point in neighbors:
            self._mark_adjacent(board, seen, (adj_point.x, adj_point.y), stone_type)

   def _update_by_seen(self, score, seen):
      for key in seen: 
         val = seen[key]
         if val is not None:
            score[val] += 1

