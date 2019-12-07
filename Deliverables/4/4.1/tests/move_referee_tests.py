import sys, unittest
sys.path.append('../../../3/3.1/src/')
from stone import StoneEnum, Stone
from board import Board
from point import Point
from constants import BOARD_DIM, PASS, EMPTY_STONE, BLACK_STONE, WHITE_STONE
sys.path.append('../src')
from move_referee import MoveReferee

class TestBoard(unittest.TestCase):

   def _get_empty_board(self):
      return Board([[Stone(EMPTY_STONE) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

   def test_valid_play(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      self.assertTrue(move_ref.valid_play(StoneEnum.BLACK, PASS))
      self.assertTrue(move_ref.valid_play(StoneEnum.BLACK, [Point(1, 1), [board]]))
      board_prev = board
      board_prev.place_stone(StoneEnum.BLACK, Point(0, 0))
      self.assertFalse(move_ref.valid_play(StoneEnum.BLACK,[Point(0, 0), [board_prev, board]]))

   def test_valid_move(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      self.assertTrue(move_ref.valid_move(StoneEnum.BLACK, Point(0, 0), [board], board))
      board_prev = board
      board_prev.place_stone(StoneEnum.BLACK, Point(0, 0))
      self.assertFalse(move_ref.valid_move(StoneEnum.WHITE, Point(0,0), [board_prev, board], board_prev))

   def test_valid_history(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      board_history = [board]
      # Beginning Game
      self.assertTrue(move_ref.valid_history(StoneEnum.BLACK, board_history))
      self.assertFalse(move_ref.valid_history(StoneEnum.WHITE, board_history))
      board_history1 = [board, board]
      self.assertFalse(move_ref.valid_history(StoneEnum.BLACK, board_history1))
      self.assertTrue(move_ref.valid_history(StoneEnum.WHITE, board_history1))
      board_history2 = [board, board, board]
      # End Game
      self.assertFalse(move_ref.valid_history(StoneEnum.BLACK, board_history2))
      self.assertFalse(move_ref.valid_history(StoneEnum.WHITE, board_history2))

   def test_check_valid_point(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      self.assertTrue(move_ref._check_valid_point(board, Point(0, 0)))
      board.place_stone(StoneEnum.BLACK, Point(0, 0))
      self.assertFalse(move_ref._check_valid_point(board, Point(0, 0)))

   def test_check_ko(self):
      pass

   def test_check_will_suicide(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      board.place_stone(StoneEnum.BLACK, Point(0,1))
      board.place_stone(StoneEnum.BLACK, Point(1,0))
      board.place_stone(StoneEnum.BLACK, Point(1,2))
      board.place_stone(StoneEnum.BLACK, Point(2,1))
      self.assertTrue(move_ref._check_will_suicide(board, StoneEnum.BLACK, Point(0,0)))

   def test_check_history_states(self):
      move_ref = MoveReferee()
      board1 = self._get_empty_board()
      board2 = self._get_empty_board()
      board3 = self._get_empty_board()
      self.assertTrue(move_ref._check_history_states([board3, board2, board1]))

   def test_check_history_prog(self):
      board1 = self._get_empty_board()
      move_ref = MoveReferee()
      board1.place_stone(StoneEnum.BLACK, Point(0,0))

      board2 = self._get_empty_board()
      board2.place_stone(StoneEnum.BLACK, Point(0,0))
      board2.place_stone(StoneEnum.BLACK, Point(5,5))
      
      board3 = self._get_empty_board()
      board3.place_stone(StoneEnum.BLACK, Point(0,0))
      board3.place_stone(StoneEnum.BLACK, Point(0,1))
      board3.place_stone(StoneEnum.BLACK, Point(0,2))
      self.assertFalse(move_ref._check_history_prog([board3, board2, board1], StoneEnum.WHITE))

   def test_valid_start(self):
      board = self._get_empty_board()
      move_ref = MoveReferee()
      self.assertFalse(move_ref._valid_start([board], StoneEnum.WHITE))
      self.assertFalse(move_ref._valid_start([board, board], StoneEnum.BLACK))

   def test_get_history_mover(self):
      move_ref = MoveReferee()
      self.assertEqual(StoneEnum.WHITE, move_ref._get_history_mover(1, StoneEnum.BLACK))
      self.assertEqual(StoneEnum.BLACK, move_ref._get_history_mover(2, StoneEnum.BLACK))
      self.assertEqual(StoneEnum.BLACK, move_ref._get_history_mover(1, StoneEnum.WHITE))
      self.assertEqual(StoneEnum.WHITE, move_ref._get_history_mover(2, StoneEnum.WHITE))

   def test_valid_step(self):
      move_ref = MoveReferee()
      curr_board = self._get_empty_board()
      curr_board.place_stone(StoneEnum.BLACK, Point(0,0))
      next_board = self._get_empty_board()
      next_board.place_stone(StoneEnum.BLACK, Point(0,0))
      next_board.place_stone(StoneEnum.WHITE, Point(0,2))
      self.assertTrue(move_ref._valid_step(curr_board, StoneEnum.WHITE, next_board))

      ahead_board = self._get_empty_board()
      ahead_board.place_stone(StoneEnum.BLACK, Point(0,0))
      ahead_board.place_stone(StoneEnum.WHITE, Point(0,2))
      ahead_board.place_stone(StoneEnum.BLACK, Point(1,1))
      ahead_board.place_stone(StoneEnum.BLACK, Point(1, 2))
      self.assertFalse(move_ref._valid_step(next_board, StoneEnum.WHITE, ahead_board))


if __name__ == '__main__':
   unittest.main()
