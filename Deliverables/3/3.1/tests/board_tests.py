import sys, unittest
sys.path.append('../src')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from constants import BOARD_DIM, BLACK_STONE, WHITE_STONE, EMPTY_STONE
from output_formatter import format_points, format_board

class TestBoard(unittest.TestCase):

   def test_board_init(self):
      board = self._get_empty_board()
      board_obj = Board(board, BOARD_DIM)
      self.assertTrue(board, board_obj.board)
      self.assertTrue(BOARD_DIM, board_obj.board_dim)
      self.assertTrue({StoneEnum.WHITE: set(), StoneEnum.BLACK: set(), None: set()}, board_obj.points)
   
   def test_board_getitem(self):
      board = self._get_empty_board()
      board_obj = Board(board, BOARD_DIM)
      self.assertTrue(Stone(EMPTY_STONE), board_obj[0][0])

   def test_board_setitem(self):
      board = self._get_empty_board()
      board_obj = Board(board, BOARD_DIM)
      board_obj[0][0] = Stone(BLACK_STONE)
      self.assertTrue(Stone(BLACK_STONE), board_obj[0][0])
      board_obj[0][0] = Stone(WHITE_STONE)
      self.assertTrue(Stone(WHITE_STONE), board_obj[0][0])

   def test_board_len(self):
      board = self._get_empty_board()
      board_obj = Board(board, BOARD_DIM)
      self.assertTrue(BOARD_DIM, len(board_obj))

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
   
   # For when BOARD_DIM = 19 
   """ 
   def test_board_get_points_19(self):
      board = self._get_empty_board()
      for i in range(19):
         board.place_stone(StoneEnum.WHITE, Point(0, i))
      points = format_points(board.get_points(StoneEnum.WHITE))
      self.assertEqual(points, ["1-1", "1-10", "1-11", "1-12", "1-13", "1-14", "1-15", \
       "1-16", "1-17", "1-18", "1-19", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9"])
   """

   def test_board_get_points(self):
      board = self._get_empty_board()
      for i in range(BOARD_DIM):
         board.place_stone(StoneEnum.WHITE, Point(0, i))
      points = format_points(board.get_points(StoneEnum.WHITE))
      manual_points = []
      for i in range(1,BOARD_DIM + 1):
         point = "1-" + str(i)
         manual_points.append(point)
      self.assertEqual(points, manual_points)
   
   def test_board_reachable(self):
      board = self._get_empty_board()
      for i in range(BOARD_DIM):
         board.board[0][i] = make_stone(StoneEnum.WHITE)
         board.board[2][i] = make_stone(StoneEnum.BLACK)
      self.assertEqual(False, board.reachable(Point(0,0), StoneEnum.BLACK))		
      for i in range(BOARD_DIM):
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
      return Board([[Stone(" ") for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

if __name__ == '__main__':
   unittest.main()