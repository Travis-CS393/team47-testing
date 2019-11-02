import unittest
import sys
sys.path.append('./src')
sys.path.append('../../3/3.1/src/')
from go_player_adv import GoPlayerAdv
from output_formatter import format_board
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone

class TestBoard(unittest.TestCase):

   def test_move_captures(self):
      board = get_empty_board(5)
      player = init_player()
      self.assertFalse(player._move_captures(board, Point(1,0)))
      board.place_stone(StoneEnum.WHITE, Point(0, 0))
      board.place_stone(StoneEnum.BLACK, Point(0, 1))
      self.assertTrue(player._move_captures(board, Point(1,0)))

   def test_valid_moves(self):
      player = init_player(2)
      history = get_simple_history()
      moves = player._get_valid_moves(history, history[0])
      self.assertEqual({(0,0), (0,1), (2,0), (3,1), (2,2), (3,2), (1,3), (2,3)}, moves)
   
   def test_choose_move_base(self):
      player = init_player(2)
      history = get_simple_history_3()
      self.assertEqual((2,3), player._choose_move_base(history, history[0]))
   
   def test_recursive(self):
      player = init_player(2)
      history = get_simple_history()
      self.assertEqual((0,0), player.choose_move(history))
   
   def test_recursive_2(self):
      player = init_player(2)
      history = get_simple_history_2()
      self.assertEqual((1,1), player.choose_move(history))

def init_player(n=1):
   player = GoPlayerAdv(n)
   player.register()
   player.receive_stone(StoneEnum.BLACK)
   return player

def get_simple_history():
   board1 =   [[" ", "W", " ", "B"],
               [" ", "B", "B", " "],
               ["B", "B", " ", " "],
               ["B", " ", " ", "W"]]

   board2 =   [[" ", "W", " ", "B"],
               [" ", "B", "B", " "],
               ["B", "B", " ", " "],
               ["B", " ", " ", "W"]]

   board3 =   [[" ", "W", " ", "B"],
               [" ", "B", "B", " "],
               ["B", "B", " ", " "],
               [" ", " ", " ", "W"]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 4), 4) for x in matrs]

def get_simple_history_2():
   board1 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", " "],
               ["B", " ", " ", "W"]]

   board2 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", " "],
               ["B", " ", " ", "W"]]

   board3 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", " "],
               [" ", " ", " ", "W"]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 4), 4) for x in matrs]

def get_simple_history_3():
   board1 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", "B"],
               ["B", " ", " ", "W"]]

   board2 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", "B"],
               ["B", " ", " ", "W"]]

   board3 =   [["B", "W", " ", "B"],
               ["B", " ", "B", " "],
               ["B", "B", " ", "B"],
               [" ", " ", " ", "W"]]
   
   matrs = [board1, board2, board3]
   return [Board(stoneify_board(x, 4), 4) for x in matrs]

def stoneify_board(matr, n):
   return [[Stone(matr[i][j]) for i in range(n)] for j in range(n)]

def get_empty_board(n):
   return Board([[Stone(" ") for i in range(n)] for j in range(n)], n)

if __name__ == '__main__':
   unittest.main()
