import sys, json, socket
from socket import error as socket_error
sys.path.append('../../../3/3.1/src/')
from stone import StoneEnum
from point import Point, str_to_point
sys.path.append('../../../6/6.2/src/')
from go_referee import GoReferee
sys.path.append('../src')
from remote_player_proxy import RemotePlayerProxy


class GoAdmin():

	def __init__(self, IP, port, default_name="player1", local_player):
		"""
		This class implements a Go game administrator that will
		administer a game between a local player and a remote player
		where the admin listens at the address (IP, port) that
		the remote connects to via socket connection.
		"""
		self.IP = IP
		self.port = port
		self.default_name = default_name
		self.local_player = local_player
		self.remote_player = None
		self.go_ref = GoReferee()

	
	def create_server(self, IP, port):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, port))
		server_socket.listen()
		client_socket, address = server_socket.accept()
		return client_socket

	def run_game(self):
		connected = True
		valid_response = True
		
		#Set Player 1
		self.go_ref.players[StoneEnum.BLACK] = self.local_player
		player1_name = self.local_player.register()
		self.local_player.receive_stone(StoneEnum.BLACK)
		
		#Server Creation
		client_socket = self.create_server(self.IP, self.port)

		self.remote_player = RemotePlayerProxy(connection=client_socket)
		
		#Set Player 2
		self.go_ref.players[StoneEnum.WHITE] = self.remote_player
		player2_name = self.remote_player.register()
		self.remote_player.receive_stone(StoneEnum.WHITE)

		# Play game
		while not self.go_ref.game_over and connected and valid_response:
			try:
				self.go_ref.referee_game()
			except socket_error:
				connected = False
				break
			except TypeError:
				valid_response = False
				break

		if self.go_ref.game_over and connected and valid_response:
			winner = self.go_ref.get_winners()
		elif not connected or not valid_response:
			winner = [self.local_player.name]
		else:
			raise Exception("Game ended unexpectedly.")

		return winner

