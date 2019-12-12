import sys, unittest
sys.path.append('../../../3/3.1/src/')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from output_formatter import format_board
sys.path.append('../../../4/4.1/src')
sys.path.append('../../../5/5.1/src/')
from go_player_base import GoPlayerBase
sys.path.append('../src')
from go_referee import GoReferee



class TestReferee(unittest.TestCase):

   def test_make_move(self):
      go_ref = init_referee()
      go_ref.board_history = get_simple_history()
      new_board = [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               [" ", "B", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
      self.assertTrue(Board(stoneify_board(new_board, 9), 9).equal(go_ref.make_move(StoneEnum.BLACK, Point(0, 0))))

   def test_update_history(self):
      go_ref = init_referee()
      go_ref.board_history = get_simple_history()
      new_board = [["B", "W", " ", "B", " ", " ", " ", " ", " "],
               [" ", "B", "B", " ", " ", " ", " ", " ", " "],
               ["B", "B", " ", " ", " ", " ", " ", " ", " "],
               ["B", " ", " ", "W", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
               [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
      go_ref.update_history(Board(stoneify_board(new_board, 9), 9))
      self.assertTrue(Board(stoneify_board(new_board,9),9).equal(go_ref.board_history[0]))

   def test_get_winners(self):
      go_ref = init_referee()
      self.assertEqual(["player1", "player2"], go_ref.get_winners())
      go_ref.winner = StoneEnum.BLACK
      self.assertEqual(["player1"], go_ref.get_winners())

   def test_play_black(self):
      go_ref = init_referee()
      pass

   def test_play_white(self):
      go_ref = init_referee()
      pass

   def test_execute_move(self):
      go_ref = init_referee()
      pass

def init_referee():
   go_ref = GoReferee(player1=GoPlayerBase("player1"), player2=GoPlayerBase("player2"))
   return go_ref

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
