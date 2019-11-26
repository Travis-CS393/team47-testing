import sys
import json
import socket
import math 
import time
from socket import error as socket_error
from stone import StoneEnum, get_other_type
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

		self.client_sockets = []

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
			print(n, total_players)
			return int(total_players) - n


	def create_server(self, IP, port, n):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#server_socket.setblocking(0)
		server_socket.bind((IP, port))
		server_socket.listen(n)
		base_time = time.time()
		time_elapsed = 0
		#while count != n and tries < 10 * n:
		#while len(self.players.keys()) < n and time_elapsed < 15:
		while time_elapsed < 120:
			try:
				client_socket, address = server_socket.accept()
				print('adding')
				#server_socket.setblocking(0)
				#self.remote_player_registration(client_socket)
				self.client_sockets.append(client_socket)
				print("added")
			except:
				pass
			
			time_elapsed = time.time() - base_time
		#self.n = len(self.players.keys())
		self.n = len(self.client_sockets)
		"""
		while len(self.players.keys()) < n and time_elapsed < 120:
			try: 
				client_socket, address = server_socket.accept()
				self.remote_player_registration(client_socket)
			except:
				pass
			time_elapsed = time.time() - base_time
		self.n = len(self.players.keys())
	
		
		
		print("reached attempt")
		#for i in range(10 * n):
		while True:
			client_socket, address = server_socket.accept()
			try: 
				print("connection made" + str(count))
				self.remote_player_registration(client_socket)
				count += 1
			except:
				pass
		self.n = count
		"""


	def remote_player_registration(self, client_socket):
		# Append all remote players, register names, and store client sockets 
		new_remote_player = RemotePlayerProxy(client_socket)
		print('registering')
		player_name = new_remote_player.register()
		
		self.players[player_name] = new_remote_player
		print(len(self.players.keys()))

	def replace_cheaters(self, cheater):
		self.standings[cheater] = 0
		for opponent in self.beaten_opponents[cheater]:
			self.standings[opponent] += 1

		# Replace cheating players with default players 
		new_default_player = GoPlayerBase("cheater" + str(self.num_cheaters))
		self.players[new_default_player.name] = new_default_player


	def run_tournament(self):
		print("Creating Server")
		self.create_server(self.IP, self.port, self.n)
		print("Server Created")

		for i in range(len(self.client_sockets)):
			self.remote_player_registration(client_sockets[i])

		print("Remotes Registered")

		defaults = self.get_num_default_players(self.n)
		# Append all default players and register their names 
		for i in range(defaults):
			new_default_player = GoPlayerBase(name="defaults" + str(i))
			default_name = new_default_player.register()
			self.players[default_name] = new_default_player

		print("Defaults Registered")
		# Initialize tournament points 
		for element in self.players:
			self.standings[element] = 0
			self.beaten_opponents[element] = []

		print("Starting Tournament")
		if self.tourney == "-cup":
			all_players_names = []
			for player in self.players.keys():
				all_players_names.append(player)
			"""
			while len(all_players_names != 1):
				for i in range(len(all_players_names)-1):
					player1_name = all_players_names[i]
					player2_name = all_players_names[i + 1]
					winner = self.run_game(self.players[all_players_names[i]], self.players[all_players_names[i + 1]])
					self.standings[winner] += 1
					if winner == player1_name:
						all_players_names.remove(player2_name)
						self.beaten_opponents[winner].append[player2_name]
					else:
						all_players_names.remove(player1_name)
						self.beaten_opponents[winner].append[player1_name]
			"""
			"""
			while len(all_players_names != 1):
				i = 0
				player1_name = all_players_names[i]
				player2_name = all_players_names[i + 1]
				winner = self.run_game(self.players[all_players_names[i]], self.players[all_players_names[i + 1]])
				self.standings[winner] += 1
				if winner == player1_name:
					all_players_names.remove(player2_name)
					self.beaten_opponents[winner].append[player2_name]
				else:
					all_players_names.remove(player1_name)
					self.beaten_opponents[winner].append[player1_name]
			"""
			i = 0
			while len(all_players_names) != 1:
				player1_name = all_players_names[i]
				player2_name = all_players_names[i + 1]
				winner = self.run_game(self.players[all_players_names[i]], self.players[all_players_names[i+1]])
				self.standings[winner] += 1	
				if winner == player1_name:
					all_players_names.remove(player2_name)
					self.beaten_opponents[winner].append(player2_name)
				else:
					all_players_names.remove(player1_name)
					self.beaten_opponents[winner].append(player1_name)
				i += 1
				i = i % len(all_players_names)

		elif self.tourney == "-league":
			all_players_names = []
			for player in self.players.keys():
				all_players_names.append(player)
			RR_pairings = self.get_RR_pairings(all_players_names)
			for rr_round in RR_pairings:
				for pair in rr_round:
					player1_name = pair[0]
					player2_name = pair[1]
					winner = self.run_game(self.players[pair[0]], self.players[pair[1]])
					self.standings[winner] += 1
		else:
			raise Exception("Not a valid type of Go tournament.")

		print("Outputting Standings")
		standings = self.format_standings(self.standings)
		return standings

	def get_RR_pairings(self, players):
		total = len(players)
		pairs = total - 1
		mid = total // 2
		RR_pairings = []
		for pair in range(pairs):
			pairings = []
			for i in range(mid):
				pairings.append([players[i], players[total - i - 1]])
			players.insert(1, players.pop())
			RR_pairings.append(pairings)
		return RR_pairings

	def run_game(self, player1, player2):
		go_ref = GoReferee(player1=player1, player2=player2)
		connected = True
		valid_response = True
		
		go_ref.players[StoneEnum.BLACK] = player1
		player1.receive_stone(StoneEnum.BLACK)
		
		go_ref.players[StoneEnum.WHITE] = player2
		player2.receive_stone(StoneEnum.WHITE)

		while not go_ref.game_over and connected and valid_response:
			try:
				go_ref.referee_game()
			except socket_error:
				connected = False
				break
			except TypeError:
				valid_response = False
				go_ref.winner = get_other_type(go_ref.current_player)
				break

		# Validate Game Over for both players
		try:
			ack_1 = player1.game_over(["end-game"])
			if ack_1 != "OK":
				go_ref.winner = StoneEnum.WHITE
		except:
			go_ref.winner = StoneEnum.WHITE

		try: 
			ack_2 = player2.game_over(["end-game"])
			if ack_2 != "OK":
				go_ref.winner = StoneEnum.BLACK
		except:
			go_ref.winner = StoneEnum.BLACK

		if go_ref.game_over and connected and valid_response:
			winner = go_ref.get_winners()
		elif not connected or not valid_response:
			winner = go_ref.get_winners()
			self.num_cheaters += 1
			self.replace_cheaters(go_ref.players[go_ref.current_player].name)
		else:
			raise Exception("Game ended unexpectedly.")

		# Randomly break ties if two winners
		if len(winner) == 1:
			return winner[0]
		else:
			rand_idx = random.randInt(0, 1)
			return winner[rand_idx]

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


