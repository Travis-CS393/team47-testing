import sys, socket, math, time, random

sys.path.append('../../3/3.1/src/')
from stone import StoneEnum, get_other_type
from point import Point, str_to_point
from output_formatter import format_board
from constants import REGISTER_TIMEOUT

sys.path.append('../../6/6.2')
from go_referee import GoReferee

sys.path.append('../../8/8.1')
from remote_player_proxy import RemotePlayerProxy


class GoTournAdmin():

	def __init__(self, default_player_type, IP, port, tourney, n):
		self.default_player_type = default_player_type
		self.IP = IP
		self.port = port
		self.tourney = tourney
		self.n = n

		self.players = {}
		self.standings = {}
		self.beaten_opponents = {}


	# Number of total players in tournament must be power of 2
	# Total = Remotes + Defaults
	def get_num_default_players(self, n):
		if n < 0:
			raise Exception("Number of remote players must be nonnegative.")
		elif n == 0:
			return 2
		elif n == 1:
			# Assume no default wins 
			return 1
		elif ((math.log(n, 2) - math.floor(math.log(n, 2))) == 0):
			return 0
		else:
			total_players = int(math.pow(2, math.ceil(math.log(n, 2))))
			return total_players - len(self.players.keys())


	def create_server(self, IP, port, n):
		print("Creating Server")
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.setblocking(0)
		server_socket.bind((IP, port))
		server_socket.listen(n)
		print("Server Created")
		
		base_time = time.time()
		time_elapsed = 0
		while len(self.players.keys()) < n and time_elapsed < REGISTER_TIMEOUT:
			try:
				client_socket, address = server_socket.accept()
				self.remote_player_registration(client_socket)
				print("Added Remote {}".format(len(self.players.keys())))
			except:
				pass
			time_elapsed = time.time() - base_time

		print("Remote Players Registered")

		return server_socket


	def remote_player_registration(self, client_socket):
		# Append all remote players, register names, and store client sockets 
		new_remote_player = RemotePlayerProxy(client_socket)
		player_name = new_remote_player.register()
		self.players[player_name] = new_remote_player
		self.standings[player_name] = 0
		self.beaten_opponents[player_name] = []


	def default_player_registration(self, name):
		new_default_player = self.default_player_type(name=name)
		default_name = new_default_player.register()
		self.players[default_name] = new_default_player
		self.standings[default_name] = 0
		self.beaten_opponents[default_name] = []


	def penalize_cheaters(self, cheater):
		self.standings[cheater] = 0


	def run_round_robin(self):
		print("Running Round Robin")
		all_players_names = list(self.players.keys())
		for i in range(len(all_players_names) - 1):
			for j in range(i + 1, len(all_players_names)):
				player1_name = all_players_names[i]
				player2_name = all_players_names[j]
				print(player1_name + " v.s " + player2_name)
				winner, cheater = self.run_game(self.players[all_players_names[i]], self.players[all_players_names[j]])
				if cheater:
					print(cheater + " cheated :(")
					self.penalize_cheaters(cheater)
					replacement_name = "cheater-replacement-{}".format(cheater)
					self.default_player_registration(name=replacement_name)
					if cheater == player1_name:
						all_players_names[i] = replacement_name
					elif cheater == player2_name:
						all_players_names[j] = replacement_name
				print(winner + " wins!")
				self.standings[winner] += 1
				if winner == player1_name:
					self.beaten_opponents[winner].append(player2_name)
				else:
					self.beaten_opponents[winner].append(player1_name)

	def run_single_elimination(self):
		print("Running Single Elimination")
		all_players_names = list(self.players.keys())
		i = 0
		while len(all_players_names) != 1:
			player1_name = all_players_names[i]
			player2_name = all_players_names[i + 1]
			print(player1_name + " v.s. " + player2_name)
			winner, cheater = self.run_game(self.players[all_players_names[i]], self.players[all_players_names[i + 1]])
			if cheater:
				print(cheater + " cheated :(")
				self.penalize_cheaters(cheater)
			print(winner + " wins!")
			self.standings[winner] += 1
			if winner == player1_name:
				all_players_names.remove(player2_name)
				self.beaten_opponents[winner].append(player2_name)
			else:
				all_players_names.remove(player1_name)
				self.beaten_opponents[winner].append(player1_name)
			i += 1
			i = i % len(all_players_names)

	def run_game(self, player1, player2):
		go_ref = GoReferee(player1=player1, player2=player2)
		connected = True
		valid_response = True
		cheater = None
		
		
		go_ref.players[StoneEnum.BLACK] = player1
		try:
			player1.receive_stone(StoneEnum.BLACK)
		except:
			go_ref.winner = StoneEnum.WHITE
			valid_response = False
		
		go_ref.players[StoneEnum.WHITE] = player2
		try:
			player2.receive_stone(StoneEnum.WHITE)
		except:
			go_ref.winner = StoneEnum.BLACK
			valid_response = False

		
		while not go_ref.game_over and connected and valid_response:
			try:
				go_ref.referee_game()
			except OSError:
				go_ref.game_over = True
				connected = False
				cheater = go_ref.players[go_ref.current_player].name
				go_ref.winner = get_other_type(go_ref.current_player)
				break
			except TypeError:
				go_ref.game_over = True
				valid_response = False
				cheater = go_ref.players[go_ref.current_player].name
				go_ref.winner = get_other_type(go_ref.current_player)
				break

		# Validate Game Over for both players
		if (go_ref.game_over and connected and valid_response) or not valid_response:
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
			
			winner = go_ref.get_winners()
		elif not connected:
			winner = go_ref.get_winners()
		else:
			raise Exception("Game ended unexpectedly.")

		# Randomly break ties if two winners
		if len(winner) == 1:
			return winner[0], cheater
		else:
			rand_idx = random.randint(0, 1)
			return winner[rand_idx], cheater


	def run_tournament(self):
		print("Tournament SetUp")
		server_socket = self.create_server(self.IP, self.port, self.n)

		num_defaults = self.get_num_default_players(self.n)
		for i in range(num_defaults):
			self.default_player_registration("default-player-{}".format(i))
		print("Default Players Registered")
		
		print("Starting Tournament")
		if self.tourney == "--league":
			self.run_round_robin()
		elif self.tourney == "--cup":
			self.run_single_elimination()
		else:
			raise Exception("Not a valid type of Go Tournament.")
		print("Tournament Over")
		
		server_socket.close()
		
		print(self.standings)
		print("Outputting Standings")
		standings = self.format_standings(self.standings)		
		return standings


	def format_standings(self, standings):
		points_list = list(dict.fromkeys(standings.values()))
		by_points = {}
		for point in points_list:
			by_points[point] = []

		for player in standings:
			by_points[standings[player]].append(player)

		place = 1
		final_output = "_____________________Final Standings____________________\n"
		for score in sorted(by_points.keys(), reverse=True):
			final_output += "{}. {}\n".format(place, self.list_players(by_points[score]))
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


