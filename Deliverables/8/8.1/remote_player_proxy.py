import sys 
import socket 
import time 
import json
sys.path.append('../../3/3.1/src')
sys.path.append('../../4/4.1/src')
sys.path.append('../../5/5.1/src')
sys.path.append('../../5/5.2/src')
from constants import BOARD_DIM, EMPTY_STONE, WHITE_STONE, BLACK_STONE
from stone import StoneEnum, Stone, make_stone
from point import get_raw, str_to_point
from obj_parser import parse_stone, parse_boards
from go_player_base import GoPlayerBase 
from go_player_adv import GoPlayerAdv 
from output_formatter import format_board

class RemotePlayerProxy():

	def __init__(self, connection):
		self.connection = connection

	def register(self):
		self.connection.sendall(bytes(json.dumps(["register"]), "utf-8"))
		player_name = self.connection.recv(8192)
		return player_name.decode("utf-8") 

	def receive_stone(self, stone_type):
		self.connection.sendall(bytes(json.dumps(["receive-stones", make_stone(stone_type).get_raw()]), "utf-8"))

	def choose_move(self, boards):
		self.connection.sendall(bytes(json.dumps(["make-a-move", format_board(boards)]), "utf-8"))
		player_move = self.connection.recv(8192)
		return player_move.decode("utf-8")


