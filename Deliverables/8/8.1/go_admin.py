import sys
import json
import socket
from socket import error as socket_error
from stone import StoneEnum
from point import Point, str_to_point
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../6/6.2/src/')
sys.path.append('../../7/7.1/src/')
from go_referee import GoReferee

#import local player
go_config = json.load(open('go.config'))
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from go_player_base import GoPlayerBase

from output_formatter import format_board

class GoAdmin():

	def __init__(self, IP, port, default_name="player1"):
		self.IP = IP
		self.port = port
		self.default_name = default_name
		self.local_player = GoPlayerBase()
		self.go_ref = GoReferee(board_size=9)

	
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
		player1_name = self.local_player.register(self.default_name)
		self.go_ref.players[StoneEnum.BLACK] = player1_name
		self.local_player.receive_stone(StoneEnum.BLACK)
		
		#Server Creation
		#client_socket = self.create_server(self.IP, self.port)
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((self.IP, self.port))
		server_socket.listen()
		client_socket, address = server_socket.accept()
		
		#Set Player 2
		client_socket.sendall(bytes(json.dumps(["register"]), "utf-8"))
		player2_name = client_socket.recv(8192)
		self.go_ref.players[StoneEnum.WHITE] = player2_name.decode("utf-8")
		client_socket.sendall(bytes(json.dumps(["receive-stones, W"]), "utf-8"))
		print("received and registered")

		# Play game
		while not self.go_ref.game_over and connected and valid_response:
			print(format_board(self.go_ref.board_history))
			self.play_black_move()
			
			if self.go_ref.game_over: break

			try:
				#self.play_white_move(client_socket)
				client_socket.sendall(bytes(json.dumps(["make-a-move", format_board(self.go_ref.board_history)]), "utf-8"))
				p2_move = client_socket.recv(8192)
				if p2_move.decode("utf-8") != "This history makes no sense!" and p2_move.decode("utf-8") != "GO has gone crazy!" and p2_move.decode("utf-8") != "pass":
					self.go_ref.execute_move(str_to_point(p2_move.decode("utf-8")))
				elif p2_move.decode("utf-8") == "pass":
					self.go_ref.execute_move(p2_move.decode("utf-8"))
				else:
					valid_response = False
					break
			except socket_error:
				connected = False
				break
			#except TypeError:
			#	valid_response = False
			#	break

		if self.go_ref.game_over and connected and valid_response:
			winner = self.go_ref.get_winners()
		elif not connected or not valid_response:
			winner = [self.local_player.name]
		else:
			raise Exception("Game ended unexpectedly.")

		return winner



	def play_black_move(self):
		# Default Player makes a move
		p = self.local_player.choose_move(self.go_ref.board_history)
		self.go_ref.execute_move(Point(p[0], p[1]))


	def play_white_move(self, client_socket):
		# Get next move from Remote Player
		client_socket.sendall(bytes(json.dumps(["make-a-move", format_board(self.go_ref.board_history)]), "utf-8"))
		p2_move = client_socket.recv(8192)
		if p2_move.decode("utf-8") != "This history makes no sense!" and p2_move.decode("utf-8") != "GO has gone crazy!" and p2_move.decode("utf-8") != "pass":
			self.go_ref.execute_move(str_to_point(p2_move.decode("utf-8")))
		elif p2_move.decode("utf-8") == "pass":
			self.go_ref.execute_move(p2_move.decode("utf-8"))
		else:
			valid_response = False

