import sys, socket, time, json
sys.path.append('./../../3/3.1/src/')
sys.path.append('./../../4/4.1/src/')
sys.path.append('./../../5/5.1/src/')
sys.path.append('./../../5/5.2/src/')
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from output_formatter import format_board
from obj_parser import parse_stone, parse_boards
from constants import WHITE_STONE, BLACK_STONE, REGISTER, RECEIVE, MOVE, GAME_OVER, GAME_OVER_RESPONSE
from go_player_base import GoPlayerBase
from go_player_adv import GoPlayerAdv


class GoRemotePlayer():

	def __init__(self, n=1):
		"""
		This class implements a Go remote player which
		sends along responses to Go gameplay commands
		to a socket listening at the same (IP, port) address.
		"""
		self.player = GoPlayerAdv(n)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.game_over = False

	def turn_on_socket(self, ip_and_port):
		self.socket.connect(ip_and_port)

	def work_with_socket(self):
		try:
			inpt = self.socket.recv(8192)
			output = self.work_JSON(json.loads(inpt.decode("utf-8")))
			if not output:
				pass
			else:
				self.socket.sendall(bytes(output, "utf-8"))
		except:
			return "Error: no connection established."

	def turn_off_socket(self):
		self.socket.close()

	def work_JSON(self, obj):
		if obj[0] == REGISTER:
			output = self.register()
		elif obj[0] == RECEIVE:
			if obj[1] == BLACK_STONE:
				stone_e = StoneEnum.BLACK
			elif obj[1] == WHITE_STONE:
				stone_e = StoneEnum.WHITE
			else:
				raise Exception("Invalid stone type.")
			self.receive_stone(stone_e)
			output = None
		elif obj[0] == MOVE:
			boards_obj = parse_boards(obj[1])
			output = self.make_a_move(boards_obj)
			if isinstance(output, tuple):
				output = get_raw(output)
		elif obj[0] == GAME_OVER:
			output = GAME_OVER_RESPONSE
		else:
			raise Exception("Invalid JSON input.")

		return output


	def register(self):
		return self.player.register()
			

	def receive_stone(self, stone_type):
		if isinstance(stone_type, StoneEnum):
			self.player.receive_stone(stone_type)
		else:
			raise Exception("Not a proper player stone.")


	def make_a_move(self, board_history):
		return self.player.choose_move(board_history)


if __name__ == "__main__":
	go_config = json.load(open('go.config'))
	HOSTNAME = go_config['IP']
	PORT = go_config['port']

	go_player_config = json.load(open('go-player.config'))
	N = go_player_config['depth']
	
	time.sleep(1)
	player = GoRemotePlayer(N)
	player.turn_on_socket((HOSTNAME, PORT))
	while not player.game_over:
		player.work_with_socket()
	player.turn_off_socket()
