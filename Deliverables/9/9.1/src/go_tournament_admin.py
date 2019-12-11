import sys, socket, math, time, random
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../4/4.1/src/')
sys.path.append('../../../5/5.1/src/')
sys.path.append('../../../6/6.2/src')
sys.path.append('../../../8/8.1/src')
from stone import StoneEnum, get_other_type
from point import Point, str_to_point, PointException
from output_formatter import format_board
from constants import REGISTER_TIMEOUT, GAME_OVER, LEAGUE, CUP
from go_referee import GoReferee
from remote_contract_proxy import RemoteContractProxy


class GoTournamentAdmin():

	def __init__(self, default_player_type, IP, port, tournament_type, n):
		"""
		This class implements a Go tournament administration
		that can run a round robin or single elimination tournament
		with total number of players being a power of two where n
		players are remote players and the rest are local default
		players. It outputs tournament standings after run.
		"""
		self.default_player_type = default_player_type
		self.IP = IP
		self.port = port
		self.tournament_type = tournament_type
		self.n = n

		"""
		The following dictionaries map player names to their corresponding
		- player object, 
		- number of wins in the current tournament, 
		- a list of the opponents they have beaten so far. 
		"""
		self.players = {}
		self.win_count = {}
		self.beaten_opponents = {}

		"""
		Keep list of all players that cheated/were eliminated in tournament.
		"""
		self.eliminated = []



	def run_tournament(self):
		print("Tournament SetUp")
		server_socket = self.create_server(self.IP, self.port, self.n)

		num_defaults = self.get_num_default_players(self.n)
		for i in range(num_defaults):
			self.default_player_registration("default-player-{}".format(i))
			print("Registered Local #{}".format(len(self.players.keys())))
		print("Default Players Registered\n")
		
		print("Starting Tournament\n")
		if self.tournament_type == LEAGUE:
			self.run_round_robin()
		elif self.tournament_type == CUP:
			self.run_single_elimination()
		else:
			raise Exception("Not a valid type of Go Tournament.")
		print("Tournament Over\n")
		
		server_socket.close()
		
		print(self.win_count)
		print("Outputting Standings\n")
		standings = self.format_standings(self.win_count)		
		return standings



	def create_server(self, IP, port, n):
		print("Creating Server")
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.setblocking(0)
		server_socket.bind((IP, port))
		server_socket.listen()
		print("Server Created\n")
		
		base_time = time.time()
		time_elapsed = 0
		while len(self.players.keys()) < n and time_elapsed < REGISTER_TIMEOUT:
			try:
				client_socket, address = server_socket.accept()
				print("Accepting Remote Player Connection")
				self.remote_player_registration(client_socket)
				print("Registered Remote #{}".format(len(self.players.keys())))
			except:
				pass
			time_elapsed = time.time() - base_time

		print("Remote Players Registered\n")

		return server_socket



	def remote_player_registration(self, client_socket):
		# Store client socket, register remote, append to tournament players
		new_remote_player = RemoteContractProxy(client_socket)
		player_name = new_remote_player.register()
		print(player_name + " registered")
		self.players[player_name] = new_remote_player
		self.win_count[player_name] = 0
		self.beaten_opponents[player_name] = []



	# Number of total players in tournament must be power of 2
	# Total Players = Remotes Players + Defaults Players
	# EX: n = 2, 2 is a power of 2,  logbase 2 of 2 is 1, an integer, add 0 defaults
	#.    n = 3, 3 not a power of 2, logbase 2 of 3 is 1.584962500721156, add 1 defaults 
	def get_num_default_players(self, n):
		if n < 0:
			raise Exception("GO TOURNAMENT ADMIN: Number of remote players must be nonnegative.")
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



	def default_player_registration(self, name):
		new_default_player = self.default_player_type(name=name)
		default_name = new_default_player.register()
		print(default_name + " registered")
		self.players[default_name] = new_default_player
		self.win_count[default_name] = 0
		self.beaten_opponents[default_name] = []



	# Round Robin: All players play everyone else once
	# EX: [a, b, c, d, e, f, g, h]
	#      a plays b, c, d, e, f, g, h
	#      b plays c, d, e, f, g, h
	#      c plays d, e, f, g, h
	#      d plays e, f, g, h
	#      e plays f, g, h
	#      f plays g, h
	#      g plays h 
	def run_round_robin(self):
		print("Running Round Robin\n")
		all_players_names = list(self.players.keys())
		
		for i in range(len(all_players_names) - 1):
			for j in range(i + 1, len(all_players_names)):
				player1_name = all_players_names[i]
				player2_name = all_players_names[j]
				print(player1_name + " v.s " + player2_name)
				
				winner, cheater = self.run_game(self.players[player1_name], self.players[player2_name])
				
				if cheater:
					print(cheater + " cheated :(")
					self.penalize_cheaters(cheater)
					replacement_name = "cheater-replacement-{}".format(cheater)
					self.default_player_registration(name=replacement_name)
					if cheater == player1_name:
						all_players_names[i] = replacement_name
					elif cheater == player2_name:
						all_players_names[j] = replacement_name
					print("Replaced cheater {} with {}".format(cheater, replacement_name))
				
				print(winner + " wins!\n")
				self.win_count[winner] += 1
				if winner == player1_name:
					self.beaten_opponents[winner].append(player2_name)
				else:
					self.beaten_opponents[winner].append(player1_name)



	def penalize_cheaters(self, cheater):
		# Cheaters always have 0 points.  
		self.win_count[cheater] = 0
		self.eliminated.append(cheater)

		# Return points to legal players they beat.
		if self.tournament_type == LEAGUE:
			for opponent in self.beaten_opponents[cheater]:
				if opponent not in self.eliminated:
					self.win_count[opponent] += 1

	
	
	# Single Elimination: Player eliminated from tournament upon losing
	# EX: [a, b, c, d, e, f, g, h]
	#      a plays b, a wins
	#      c plays d, c wins
	#      e plays f, f wins
	#      g plays h, h wins
	#     [a, c, f, h]
	#      a plays c, c wins
	#      f plays h, h wins
	#.    [c, h]
	#      c plays h, h wins 
	def run_single_elimination(self):
		print("Running Single Elimination\n")
		all_players_names = list(self.players.keys())
		
		i = 0
		while len(all_players_names) != 1:
			player1_name = all_players_names[i]
			player2_name = all_players_names[i + 1]
			print(player1_name + " v.s. " + player2_name)
			
			winner, cheater = self.run_game(self.players[player1_name], self.players[player2_name])
			
			if cheater:
				print(cheater + " cheated :(")
				self.penalize_cheaters(cheater)
			
			print(winner + " wins!")
			self.win_count[winner] += 1
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
		
		# Distribute Stones Before Game
		player1_received = False
		try:
			player1.receive_stone(StoneEnum.BLACK)
			player1_received = True
		except:
			go_ref.winner = StoneEnum.WHITE
			connected = False
		if player1_received:
			try:
				player2.receive_stone(StoneEnum.WHITE)
			except:
				go_ref.winner = StoneEnum.BLACK
				connected = False
		
		# Referee game and check for cheating condition
		# - Game over via breaking the rules. 
		# - Invalid responses during game. 
		# - Disconnecting during game. 
		while not go_ref.game_over and connected and valid_response:
			try:
				go_ref.referee_game()
			except OSError:
				go_ref.game_over = True
				connected = False
				cheater = go_ref.players[go_ref.current_player].name
				print("Player {} disconnected.".format(cheater))
				go_ref.winner = get_other_type(go_ref.current_player)
				break
			except PointException:
				go_ref.game_over = True
				valid_response = False
				cheater = go_ref.players[go_ref.current_player].name
				print("Invalid response from player {}.".format(cheater))
				go_ref.winner = get_other_type(go_ref.current_player)
				break

		if go_ref.broke_rules:
			cheater = go_ref.players[go_ref.broke_rules].name
			print("Player {} broke the rules.".format(cheater))

		# Validate Game Over for both players
		if (go_ref.game_over and connected and valid_response) or not valid_response:
			if not player1.game_over([GAME_OVER]):
				print("Did not receive game_over from Player {}".format(player1.name))
				go_ref.winner = StoneEnum.WHITE
			else:
				if not player2.game_over([GAME_OVER]):
					print("Did not receive game_over from Player {}".format(player2.name))
					go_ref.winner = StoneEnum.BLACK
			winner = go_ref.get_winners()
		elif not connected:
			winner = go_ref.get_winners()
		else:
			raise Exception("GO TOURNAMENT ADMIN: Game ended unexpectedly.")

		# Randomly break ties if two winners
		if len(winner) == 1:
			return winner[0], cheater
		else:
			rand_idx = random.randint(0, 1)
			return winner[rand_idx], cheater



	#################################################
	### Helper Functions: Tournament Status Updates
	#################################################
	def get_tournament_status(self):
		pass


	def get_active_players(self):
		active = []
		for player in list(self.players.keys()):
			if player not in self.eliminated:
				active.append(player)
		return active


	def format_standings(self, win_count):
		points_list = list(dict.fromkeys(win_count.values()))
		by_points = {}
		for point in points_list:
			by_points[point] = []

		for player in win_count:
			by_points[win_count[player]].append(player)

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


