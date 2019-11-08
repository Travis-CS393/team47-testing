import sys
import socket
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from constants import EMPTY_STONE, WHITE_STONE, BLACK_STONE
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from obj_parser import parse_stone, parse_boards
from go_player_base import GoPlayerBase
from go_player_adv import GoPlayerAdv
from output_formatter import format_board
import json


class GoPlayerProxy():

	def __init__(self, n=1):
		self.player = GoPlayerAdv(n)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def turn_on_socket(self, ip_and_port:tuple):
		self.socket.connect(ip_and_port)

	def work_with_socket(self):
		try:
			inpt = self.socket.recv(4096)
			output = self.make_action_from_JSON(inpt)
			if output:
				self.socket.sendall(output)
		except:
			return "Error: no connection established"

	def turn_off_socket(self):
		self.socket.close()

	def work_JSON(self, input):
		obj, _ = json.JSONDecoder().raw_decode(input)
		if obj[0] == "register":
			output = self.register("no name")
		elif obj[0] == "receive-stones":
			if obj[1] == BLACK_STONE:
				stone_e = StoneEnum.BLACK
			elif obj[1] == WHITE_STONE:
				stone_e = StoneEnum.WHITE
			else:
				raise Exception("Invalid stone type")
			output = self.receive_stone(stone_e)
		elif obj[0] == "make-a-move":
			boards_obj = parse_boards(obj[1])
			output = self.make_a_move(boards_obj)
			if isinstance(output, tuple):
				output = get_raw(output)
		else:
			raise Exception("Invalid JSON input")

		if not output: 
			return output

		return json.JSONEncoder().encode(output)


	def register(self, name):
		if isinstance(name, str):
			return self.player.register(name)
		else:
			raise Exception("Not a proper player name.")
			
	def receive_stone(self, stone_type):
		if isinstance(stone_type, StoneEnum):
			self.player.receive_stone(stone_type)
		else:
			raise Exception("Not a proper player stone.")

	def make_a_move(self, board_history):
		return self.player.choose_move(board_history)


