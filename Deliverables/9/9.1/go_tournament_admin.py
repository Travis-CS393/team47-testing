import sys
import json
import socket
import traceback
import math 
from socket import error as socket_error
from stone import StoneEnum
from point import Point, str_to_point
from threading import Thread
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
		self.players = {}
		self.standings = {}
		self.threads = []

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

	def create_server(self, IP, port, n):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, port))
		server_socket.listen(n)
		while True:
			client_socket, address = server_socket.accept()
			try:
				#Thread(target=remote_player_registration, args=(client_socket, IP, port)).start()
				new_thread = Thread(target=remote_player_registration, args=(client_socket, IP, port))
				self.threads.append(new_thread)
				new_thread.start()
			except:
				print("Failed to start thread")

	def remote_player_registration(self, client_socket, IP, port):
		# Append all remote players, register names, and store client sockets 
		new_remote_player = RemotePlayerProxy(client_socket)
		player_name = new_remote_player.register()
		self.players[player_name] = new_remote_player

	
	def run_tournament(self):
		self.create_server(self.IP, self.port, self.n)
		defaults = self.get_num_default_players(self.n)

		# Append all default players and register their names 
		for i in range(len(defaults)):
			new_default_player = GoPlayerBase(name="defaults")
			default_name = new_default_player.register()
			self.players[default_name] = new_default_player

		# Initialize tournament points 
		for element in self.players:
			self.standings[element] = 0

		if self.tourney == "-cup":
			all_players_names = []
			for player in self.players:
				all_players_names.append(player)
			while len(all_players_names != 1):
				for i in range(len(all_players_names)-1):
					player1_name = all_players_names[i]
					player2_name = all_players_names[i + 1]
					winner = self.run_game(self.players[all_players[i]], self.players[all_players[i + 1]])
					self.standings[winner] += 1
					if winner == player1_name:
						all_players_names.remove(player2_name)
					else:
						all_players_names.remove(player1_name)
			return all_players_names[0]
		elif self.tourney == "-league":
			# run round robin 
			print("oops")
		else:
			raise Exception("Not a valid type of Go tournament.")

	def run_game(self, player1, player2):
		go_ref = GoReferee(player1=player1, player2=player2)
		connected = True
		valid_response = True
		
		self.go_ref.players[StoneEnum.BLACK] = player1.name
		player1.receive_stone(StoneEnum.BLACK)
		
		self.go_ref.players[StoneEnum.WHITE] = player2_name
		player2.receive_stone(StoneEnum.WHITE)

		# Play game
		while not go_ref.game_over and connected and valid_response:
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

		return winner[0]

	def format_standings(self, standings):
		pass