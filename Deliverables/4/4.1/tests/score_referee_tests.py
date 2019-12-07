import sys, unittest
sys.path.append('../../../3/3.1/src/')
from stone import StoneEnum, Stone
from board import Board
from point import Point
from constants import BOARD_DIM, PASS, EMPTY_STONE, BLACK_STONE, WHITE_STONE
sys.path.append('../src')
from score_referee import ScoreReferee

class TestBoard(unittest.TestCase):

   def _get_empty_board(self):
      return Board([[Stone(EMPTY_STONE) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

   def test_get_score(self):
      score_ref = ScoreReferee()
      board = self._get_empty_board()
      self.assertEqual({StoneEnum.WHITE: 0, StoneEnum.BLACK: 0}, score_ref.get_score(board))

   def test_update_score_basic(self):
      score_ref = ScoreReferee()
      board = self._get_empty_board()
      score = {StoneEnum.WHITE: 0, StoneEnum.BLACK: 0}
      self.assertEqual(score, score_ref.get_score(board))
      board.place_stone(StoneEnum.BLACK, Point(0, 0))
      score_ref._update_score_basic(board, score, StoneEnum.BLACK)
      self.assertEqual({StoneEnum.WHITE: 0, StoneEnum.BLACK: 361}, score_ref.get_score(board))
      board.place_stone(StoneEnum.WHITE, Point(0, 1))
      score_ref._update_score_basic(board, score, StoneEnum.WHITE)
      self.assertEqual({StoneEnum.WHITE: 1, StoneEnum.BLACK: 1}, score_ref.get_score(board))

   def test_update_score_empty_stones(self):
      score_ref = ScoreReferee()
      board = self._get_empty_board()
      pass

   def test_mark_adjacent(self):
      score_ref = ScoreReferee()
      board = self._get_empty_board()
      pass

   def test_update_by_seen(self):
      score_ref = ScoreReferee()
      board = self._get_empty_board()
      pass

if __name__ == '__main__':
   unittest.main()
