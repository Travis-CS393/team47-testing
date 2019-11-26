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
sys.path.append('../../8/8.1')
from go_referee import GoReferee
from remote_player_proxy import RemotePlayerProxy
from output_formatter import format_board

#import local player
go_config = json.load(open('go.config'))
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from constants import BOARD_DIM
from go_player_base import GoPlayerBase


class GoTournAdmin():

	def __init__(self, IP, port, tourney="-cup", n=1):
		self.num_cheaters = 0
		self.IP = IP
		self.port = port
		self.tourney = tourney
		self.n = n
		self.players = {}
		self.standings = {}
		self.beaten_opponents = {}
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
		count = 0 
		tries = 0
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, port))
		server_socket.listen(n)
		while count != n and tries < 10 * n:
			tries += 1
			client_socket, address = server_socket.accept()
			try:
				self.remote_player_registration(client_socket, IP, port)
				count += 1
			except:
				pass
		self.n = count


	def remote_player_registration(self, client_socket, IP, port):
		# Append all remote players, register names, and store client sockets 
		new_remote_player = RemotePlayerProxy(client_socket)
		player_name = new_remote_player.register()
		self.players[player_name] = new_remote_player


	def replace_cheaters(self, cheater):
		self.standings[cheater] = 0
		for opponent in self.beaten_opponents[cheater]:
			self.standings[opponent] += 1

		# Replace cheating players with default players 
		new_default_player = GoPlayerBase("cheater" + str(self.num_cheaters))
		self.players[new_default_player.name] = new_default_player


	def run_tournament(self):
		self.create_server(self.IP, self.port, self.n)

		defaults = self.get_num_default_players(self.n)
		# Append all default players and register their names 
		for i in range(len(defaults)):
			new_default_player = GoPlayerBase(name="defaults" + str(i))
			default_name = new_default_player.register()
			self.players[default_name] = new_default_player

		# Initialize tournament points 
		for element in self.players:
			self.standings[element] = 0
			self.beaten_opponents[element] = []

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
						self.beaten_opponents[winner].append[player2_name]
					else:
						all_players_names.remove(player1_name)
						self.beaten_opponents[winner].append[player1_name]
		elif self.tourney == "-league":
			all_players_names = []
			for player in self.players:
				all_players_names.append(player)
			RR_pairings = self.get_RR_pairings(all_players_names)
			for rr_round in range(len(RR_pairings)):
				for pair in range(len(RR_pairings[0])):
					player1_name = pair[0]
					player2_name = pair[1]
					winner = self.run_game(self.players[pair[0]], self.players[pair[1]])
					self.standings[winner] += 1
		else:
			raise Exception("Not a valid type of Go tournament.")

		standings = self.format_standings(self.standings)
		return standings

	def get_RR_pairings(self, players):
		total = len(players)
		pairs = total - 1
		mid = total / 2
		RR_pairings = []
		for pair in range(pairs):
			pairings = []
			for i in range(mid):
				pairings.append(players[i], players[count-i-1])
			players.insert(1, players.pop())
			RR_pairings.append(pairings)
		return RR_pairings

	def run_game(self, player1, player2):
		go_ref = GoReferee(board_size=BOARD_DIM, player1=player1, player2=player2)
		connected = True
		valid_response = True
		
		self.go_ref.players[StoneEnum.BLACK] = player1.name
		player1.receive_stone(StoneEnum.BLACK)
		
		self.go_ref.players[StoneEnum.WHITE] = player2_name
		player2.receive_stone(StoneEnum.WHITE)

		while not go_ref.game_over and connected and valid_response:
			try:
				self.go_ref.referee_game()
			except socket_error:
				connected = False
				break
			except TypeError:
				valid_response = False
				self.go_ref.winner = self.go_ref.players[get_other_type(self.current_player)]
				break

		# Validate game over over network

		if self.go_ref.game_over and connected and valid_response:
			winner = self.go_ref.get_winners()
		elif not connected or not valid_response:
			winner = self.go_ref.get_winners()
			self.num_cheaters += 1
			self.replace_cheaters(self.go_ref.players[self.current_player].name)
		else:
			raise Exception("Game ended unexpectedly.")

		return winner[0]

	def format_standings(self, standings):
		points_list = list(dict.fromkeys(standings.values()))
		by_points = {}
		for point in points_list:
			by_points[point] = []

		for player in standings:
			by_points[standings[player]].append(player)

		place = 1
		final_output = "_________Final Standings__________\n"
		for score in sorted(by_points.keys(), reverse=True):
			line = str(place) + ". " + self.list_players(by_points[score]) + "\n"
			final_output += line
			place += 1
		return final_output

	def list_players(self, players_arr):
		output = ""
		for i in range(len(players_arr)):
			if i == len(players_arr) - 1:
				output += str(players_arr[i])
			else:
				output += str(players_arr[i]) + ", "
		return output


