import sys, unittest
sys.path.append('../../../3/3.1/src/')
from board import Board
from point import Point, str_to_point
from stone import Stone, StoneEnum, make_stone
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, PASS, BLACK_STONE, WHITE_STONE
sys.path.append('../../../5/5.2/src/')
from go_player_adv import GoPlayerAdv
sys.path.append('../src')
from remote_player import GoRemotePlayer


class TestBoard(unittest.TestCase):

	def test_work_JSON_Register(self):
		remote_player = GoRemotePlayer(n=2)
		output = remote_player.work_JSON([REGISTER])
		remote_player.turn_off_socket()
		self.assertEqual("default_player", output)

	def test_work_JSON_Receive(self):
		remote_player = GoRemotePlayer(n=2)
		remote_player.work_JSON([REGISTER])
		output = remote_player.work_JSON([RECEIVE, BLACK_STONE])
		remote_player.turn_off_socket()
		self.assertEqual(None, output)

	def test_work_JSON_Move(self):
		remote_player = GoRemotePlayer(n=2)
		remote_player.work_JSON([REGISTER])
		remote_player.work_JSON([RECEIVE, BLACK_STONE])
		board_history = get_simple_history()
		output = remote_player.work_JSON([MOVE, board_history])
		remote_player.turn_off_socket()
		self.assertEqual("1-5", output)

	def test_invalid_protocol(self):
		remote_player = GoRemotePlayer(n=2)
		remote_player.turn_off_socket()
		self.assertRaisesAny(remote_player.work_JSON,[RECEIVE, BLACK_STONE])
		
		remote_player1 = GoRemotePlayer(n=2)
		remote_player1.work_JSON([REGISTER])
		board_history = get_simple_history()
		self.assertRaisesAny(remote_player1.work_JSON,[MOVE, board_history])
		remote_player1.turn_off_socket()

		remote_player2 = GoRemotePlayer(n=2)
		board_history = get_simple_history()
		self.assertRaisesAny(remote_player2.work_JSON,[MOVE, board_history])
		remote_player2.turn_off_socket()

	def assertRaisesAny(self, func, arg):
		with self.assertRaises(Exception):
			func(arg)

def get_simple_history():
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

   return [board1, board2, board3]

if __name__ == '__main__':
   unittest.main()
