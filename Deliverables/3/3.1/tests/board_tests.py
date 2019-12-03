import unittest
import sys
sys.path.append('../src')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from output_formatter import format_points, format_board

class TestBoard(unittest.TestCase):

   def test_board_occupied_and_place(self):
      board = self._get_empty_board()
      point = str_to_point("2-3")
      stone_type = StoneEnum.WHITE
      self.assertFalse(board.occupied(point))
      board.place_stone(stone_type, point)
      self.assertTrue(board.occupied(point))
   
   def test_board_occupies(self):
      board = self._get_empty_board()
      point = str_to_point("2-3")
      stone_type = StoneEnum.WHITE
      test_type = StoneEnum.WHITE
      self.assertFalse(board.occupies(test_type, point))
      board.place_stone(stone_type, point)
      self.assertTrue(board.occupies(test_type, point))

   def test_board_place(self):
      board = self._get_empty_board()
      board.place_stone(StoneEnum.WHITE, Point(2, 0))
      self.assertEqual("W", board.board[2][0].get_raw())
      self.assertEqual("This seat is taken!", board.place_stone(StoneEnum.WHITE, Point(2, 0)))
   
   def test_board_remove(self):
      board = self._get_empty_board()
      self.assertEqual("I am just a board! I cannot remove what is not there!", \
          board.remove_stone(StoneEnum.WHITE, Point(2, 0)))
      board.place_stone(StoneEnum.WHITE, Point(2,0))
      self.assertEqual(None, board.remove_stone(StoneEnum.WHITE, Point(2,0))[2][0].get_type())
   
   """
   def test_board_get_points(self):
      board = self._get_empty_board()
      for i in range(19):
         board.place_stone(StoneEnum.WHITE, Point(0, i))
      points = format_points(board.get_points(StoneEnum.WHITE))
      self.assertEqual(points, ["1-1", "1-10", "1-11", "1-12", "1-13", "1-14", "1-15", \
       "1-16", "1-17", "1-18", "1-19", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9"])
   """
   
   def test_board_reachable(self):
      board = self._get_empty_board()
      for i in range(19):
         board.board[0][i] = make_stone(StoneEnum.WHITE)
         board.board[2][i] = make_stone(StoneEnum.BLACK)
      self.assertEqual(False, board.reachable(Point(0,0), StoneEnum.BLACK))		
      for i in range(19):
         board.board[1][i] = make_stone(StoneEnum.WHITE)
      self.assertEqual(True, board.reachable(Point(0,0), StoneEnum.BLACK))

   def test_board_liberties(self):
      board = self._get_empty_board()
      board.place_stone(StoneEnum.WHITE, Point(0,0))
      _, liberties = board.get_liberties(Point(0,0))
      self.assertTrue({(0,1), (1,0)} == liberties)

   def test_board_liberties_adv(self):
      board = self._get_empty_board()
      board.place_stone(StoneEnum.WHITE, Point(1,1))
      board.place_stone(StoneEnum.WHITE, Point(1,2))
      _, liberties = board.get_liberties(Point(1,2))
      self.assertTrue({(1,0), (0,1), (2,2), (0,2), (2, 1), (1,3)} == liberties)

   def _get_empty_board(self):
      return Board([[Stone(" ") for i in range(19)] for j in range(19)])

if __name__ == '__main__':
   unittest.main()