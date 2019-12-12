import sys, json, socket
from socket import error as socket_error
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../6/6.2/src/')
sys.path.append('../src')
from stone import StoneEnum
from point import Point, str_to_point, PointException
from go_referee import GoReferee
from remote_contract_proxy import RemoteContractProxy


class GoAdmin():

	def __init__(self, IP, port, local_player, default_name="player1"):
		"""
		This class implements a Go game administrator that will
		administer a game between a local player and a remote player
		where the admin listens at the address (IP, port) that
		the remote connects to via socket connection.
		"""
		self.IP = IP
		self.port = port
		self.default_name = default_name
		self.local_player = local_player()
		self.remote_player = None

	
	def create_server(self, IP, port):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, port))
		server_socket.listen()
		client_socket, address = server_socket.accept()
		return client_socket


	def run_game(self):
		
		#Set Player 2
		client_socket = self.create_server(self.IP, self.port)
		self.remote_player = RemoteContractProxy(connection=client_socket)
		player2_name = self.remote_player.register()
		self.remote_player.receive_stone(StoneEnum.WHITE)

		#Set Player 1
		player1_name = self.local_player.register()
		self.local_player.receive_stone(StoneEnum.BLACK)
	
		# Pass to Referee to start game
		go_ref = GoReferee(player1=self.local_player, player2=self.remote_player)
		connected = True
		valid_response = True

		# Play game
		while not go_ref.game_over and connected and valid_response:
			try:
				go_ref.referee_game()
			except socket_error:
				connected = False
				break
			except PointException:
				valid_response = False
				break

		if go_ref.game_over and connected and valid_response:
			winner = go_ref.get_winners()
		elif not connected or not valid_response:
			winner = [self.local_player.name]
		else:
			raise Exception("GO ADMIN: Game ended unexpectedly.")

		return winner


