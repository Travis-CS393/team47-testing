import sys, unittest
sys.path.append('../../../3/3.1/src/')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from output_formatter import format_board
from constants import BOARD_DIM
sys.path.append('../src')
from go_player_adv import GoPlayerAdv


class TestBoard(unittest.TestCase):

   def test_move_captures(self):
      board = get_empty_board(BOARD_DIM)
      player = init_player()
      self.assertFalse(player._move_captures(board, Point(1,0)))
      board.place_stone(StoneEnum.WHITE, Point(0, 0))
      board.place_stone(StoneEnum.BLACK, Point(0, 1))
      self.assertTrue(player._move_captures(board, Point(1,0)))

   def test_valid_moves(self):
      player = init_player(2)
      history = get_simple_history()
      moves = player._get_valid_moves(history, history[0])
      self.assertEqual({(0,0), (0,1), (2,0), (3,1), (2,2), (3,2), 
         (1,3), (2,3), (7, 3), (4, 8), (2, 8),(8, 0),(0, 7),(6, 2), 
         (1, 6),(3, 7),(2, 5),(8, 5),(5, 8),(4, 0),(6, 7),(5, 5),(7, 6), 
         (5, 0),(0, 4),(2, 6),(8, 2),(4, 5),(6, 0),(1, 4),(7, 5),(8, 7),(4, 2), 
         (6, 5),(5, 3),(7, 0),(6, 8),(0, 6),(1, 7),(3, 4),(7, 8),(2, 4),(8, 4),
         (4, 7),(6, 6),(5, 6),(7, 7),(5, 1),(7, 2),(8, 1),(4, 4),(6, 3),(1, 5), 
         (3, 6),(8, 6),(4, 1),(6, 4), (5, 4), (7, 1), (0, 5), (0, 8), (3, 5), (2, 7), 
         (8, 3), (4, 6), (6, 1), (5, 7), (3, 8), (1, 8),(7, 4),(8, 8),(4, 3),(5, 2)}, moves)
   
   def test_choose_move_base(self):
      player = init_player(2)
      history = get_simple_history_3()
      self.assertEqual(None, player._choose_move_base(history, history[0]))
   
   def test_choose1(self):
      player = init_player(2)
      history = get_simple_history()
      self.assertEqual((0,0), player.choose_move(history))

   def test_choose2(self):
      player = init_player(2)
      history = get_simple_history_2()
      self.assertEqual((0,4), player.choose_move(history))

   def test_choose3(self):
      player = init_player(1)
      history = get_simple_history_2()
      self.assertEqual((0,4), player.choose_move(history))

def init_player(n=1):
   player = GoPlayerAdv(n)
   player.register()
   player.receive_stone(StoneEnum.BLACK)
   return player

def get_simple_history():
   board1 =   [[" ", "W", " ", "B", " ", " ", " ", " ", " "],
               [" ", "B", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board2 =   [[" ", "W", " ", "B", " ", " ", " ", " ", " "],
               [" ", "B", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board3 =   [[" ", "W", " ", "B", " ", " ", " ", " ", " "],
               [" ", "B", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", "W", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 9), 9) for x in matrs]

def get_simple_history_2():
   board1 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board2 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board3 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 9), 9) for x in matrs]

def get_simple_history_3():
   board1 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board2 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

   board3 =   [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               ["B", " ", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", "B", " ", " ", " ", " ", " "],
               [" ", " ", " ", "W", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 9), 9) for x in matrs]

def stoneify_board(matr, n):
   return [[Stone(matr[i][j]) for i in range(n)] for j in range(n)]

def get_empty_board(n):
   return Board([[Stone(" ") for i in range(n)] for j in range(n)], n)

if __name__ == '__main__':
   unittest.main()
