import sys, socket, time, json
sys.path.append('../../../3/3.1/src')
from stone import Stone, make_stone
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE

class RemotePlayerProxy():
	def __init__(self, connection):
		"""
		This class implements a remote player proxy which
		has the same interface as the player, but performs
		the network send and receive of messages between
		client and server sockets.
		"""
		self.connection = connection
		self.name = None

	def register(self):
		self.connection.sendall(bytes(json.dumps([REGISTER]), "utf-8"))
		while True:
			try:
				player_name = self.connection.recv(8192)
				break
			except:
				pass
		self.name = player_name.decode("utf-8")
		return player_name.decode("utf-8") 

	def receive_stone(self, stone_type):
		self.connection.sendall(bytes(json.dumps([RECEIVE, make_stone(stone_type).get_raw()]), "utf-8"))

	def choose_move(self, boards):
		print("player making move?")
		self.connection.sendall(bytes(json.dumps([MOVE, format_board(boards)]), "utf-8"))
		print("player received board")
		while True:
			try:
				player_move = self.connection.recv(8192)
				break
			except:
				pass
		print(player_move.decode("utf-8"))
		return player_move.decode("utf-8")
		

	def game_over(self, end_tag):
		self.connection.sendall(bytes(json.dumps(end_tag), "utf-8"))
		while True:
			try:
				response = self.connection.recv(8192)
				break
			except:
				pass
		return response.decode("utf-8")

