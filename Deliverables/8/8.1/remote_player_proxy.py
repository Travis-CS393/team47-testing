import sys, socket, time, json
sys.path.append('../../3/3.1/src')
from stone import Stone, make_stone
from output_formatter import format_board

class RemotePlayerProxy():
	def __init__(self, connection):
		self.connection = connection
		self.name = None

	def register(self):
		self.connection.sendall(bytes(json.dumps(["register"]), "utf-8"))
		time.sleep(.01)
		player_name = self.connection.recv(8192)
		self.name = player_name.decode("utf-8")
		return player_name.decode("utf-8") 

	def receive_stone(self, stone_type):
		self.connection.sendall(bytes(json.dumps(["receive-stones", make_stone(stone_type).get_raw()]), "utf-8"))

	def choose_move(self, boards):
		self.connection.sendall(bytes(json.dumps(["make-a-move", format_board(boards)]), "utf-8"))
		time.sleep(.01)
		player_move = self.connection.recv(8192)
		return player_move.decode("utf-8")
		

	def game_over(self, end_tag):
		self.connection.sendall(bytes(json.dumps(end_tag), "utf-8"))
		time.sleep(.01)
		response = self.connection.recv(8192)
		return response.decode("utf-8")

