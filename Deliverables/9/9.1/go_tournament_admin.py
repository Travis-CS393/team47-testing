import sys
import json
import socket
import math 
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

class GoTournAdmin():

	def __init__(self, IP, port, tourney="-cup", n=1):
		self.IP = IP
		self.port = port
		self.tourney = tourney
		self.n = n

	# Tournaments must have number of total players as powers of 2
	def get_num_default_players(self, n):
		if n < 0:
			raise Exception("Number of remote players must be nonnegative")
		elif n == 0:
			return 2
		elif n == 1:
			return 1
		elif ((math.log(n, 2) - math.floor(math.log(n, 2))) == 0):
			return 0
		else:
			total_players = math.pow(2, math.ceil(math.log(n, 2)))
			return total_players - n

	def create_server(self, IP, port):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, port))
		server_socket.listen()
		client_socket, address = server_socket.accept()
		return client_socket

	def run_tournament():
		client_socket = self.create_server(self.IP, self.port)
		defaults = self.get_num_default_players(self.n)

		# Append all default players and register their names 
		all_players = []
		for i in range(len(defaults)):
			default_name = 
			all_players.append()

		# Append all remote players, register names, and store client sockets 

		if self.tourney == "-cup":
			all_players_names = []
			for player in all_players:
				all_players_names.append(player.name)
			while len(all_players_names != 1):
				for i in range(len(all_players_names)-1):
					player1_name = all_players_names[i]
					player2_name = all_players_names[i + 1]
					winner = self.run_game(all_players[i], all_players[i + 1])
					if winner == player1_name:
						#remove player2 from array
					else:
						#remove player1 from array 
			#player that won tournament is the only name left in all_players_names
			#print to stdout 
		elif self.tourney == "-league":
			# run round robin 
		else:
			raise Exception("Not a valid type of Go tournament.")

	# REFACTOR TO TAKE IN TWO PLAYERS INSTEAD OF PLAYER NAME
	# REFACTOR REFERRE TO TAKE IN TWO PLAYERS
	# IMPLEMENT PLAYER PROXY PATTERN
	def run_game(self, player1, player2):
		go_ref = GoReferee()
		connected = True
		valid_response = True
		
		#Set Player 1 if default 
		player1_name = self.player1.register()
		go_ref.players[StoneEnum.BLACK] = player1_name
		player1.receive_stone(StoneEnum.BLACK)
		
		#Set Player 2 if remote
		client_socket.sendall(bytes(json.dumps(["register"]), "utf-8"))
		player2_name = client_socket.recv(8192)
		self.go_ref.players[StoneEnum.WHITE] = player2_name.decode("utf-8")
		client_socket.sendall(bytes(json.dumps(["receive-stones, W"]), "utf-8"))
		print("received and registered")

		# Play game
		while not go_ref.game_over and connected and valid_response:
			self.play_black_move()
			
			if go_ref.game_over: break

			try:
				client_socket.sendall(bytes(json.dumps(["make-a-move", format_board(self.go_ref.board_history)]), "utf-8"))
				p2_move = client_socket.recv(8192)
				check_response = p2_move.decode("utf-8")
				if check_response == "pass":
					self.go_ref.execute_move(check_response)
				else:
					check_response_tmp = check_response.split("-")
					if len(check_response_tmp) != 2:
						valid_response = False
						break
					elif int(check_response_tmp[0]) < 1 or int(check_response_tmp[0]) > 9:
						valid_response = False
						break
					elif int(check_response_tmp[0]) < 1 or int(check_response_tmp[0]) > 9:
						valid_response = False
						break
					else:
						self.go_ref.execute_move(str_to_point(check_response))


			except socket_error:
				connected = False
				break

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

