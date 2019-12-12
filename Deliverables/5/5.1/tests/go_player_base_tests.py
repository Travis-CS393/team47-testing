import sys, unittest
sys.path.append('../../../3/3.1/src/')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from output_formatter import format_board
sys.path.append('../../../4/4.1/src')
sys.path.append('../src')
from go_player_base import GoPlayerBase


class TestBoard(unittest.TestCase):
   # Comment out random epsilon in order to test 
   
   def test_register(self):
      player = GoPlayerBase()
      self.assertEqual("default_player", player.register())

   def test_receive_stone(self):
      player1 = GoPlayerBase("player1")
      player1.register()
      self.assertEqual(None, player1.stone_type)
      player1.receive_stone(StoneEnum.BLACK)
      self.assertEqual(StoneEnum.BLACK, player1.stone_type)

      player2 = GoPlayerBase("player2")
      player2.register()
      self.assertEqual(None, player2.stone_type)
      player2.receive_stone(StoneEnum.WHITE)
      self.assertEqual(StoneEnum.WHITE, player2.stone_type)

   def test_choose_move(self):
      player = init_player()
      history = get_simple_history_3()
      self.assertEqual((0,4), player.choose_move(history))

      history1 = get_simple_history()
      self.assertEqual((0,0), player.choose_move(history1))

   def test_game_over(self):
      player1 = init_player()
      player1.register()
      player1.receive_stone(StoneEnum.BLACK)
      self.assertTrue(player1.game_over(["end-game"]))

      player2 = init_player()
      player2.register()
      player2.receive_stone(StoneEnum.WHITE)
      self.assertFalse(player2.game_over(["game-over"]))

   def test_invalid_protocol(self):
      player1 = GoPlayerBase()
      self.assertRaisesAny(player1.receive_stone, StoneEnum.BLACK)

      player2 = GoPlayerBase()
      player2.register()
      history = get_simple_history_3()
      self.assertRaisesAny(player2.choose_move, history)

      player3 = GoPlayerBase()
      self.assertRaisesAny(player3.choose_move, history)

   def assertRaisesAny(self, func, arg):
      with self.assertRaises(Exception):
         func(arg)

def init_player():
   player = GoPlayerBase()
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

