import sys, json, socket, time, random
sys.path.append('../../../3/3.1/src/')
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from obj_parser import parse_stone, parse_boards
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, WHITE_STONE, BLACK_STONE
sys.path.append('../../../5/5.1/src/')
from go_player_base import GoPlayerBase


class GoPlayerProxy():

	def __init__(self, n=1):
		self.player = GoPlayerBase("default-player")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def turn_on_socket(self, ip_and_port):
		self.socket.connect(ip_and_port)

	def work_with_socket(self):
		try:
			inpt = self.socket.recv(8192)
			print(inpt.decode("utf-8"))
			if inpt.decode("utf-8") == "done":
				return "done"
			else:
				output = self.work_JSON(json.loads(inpt.decode("utf-8")))
				if output:
					self.socket.sendall(bytes(output, "utf-8"))
				return "not done"
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
			print("trying")
			x = random.randrange(1,9)
			y = random.randrange(1,9)
			output = (x, y)
			print("found one")
			if isinstance(output, tuple):
				output = get_raw(output)
		elif obj[0] == "end-game":
			output = "OK"
		else:
			raise Exception("Invalid JSON input.")

		if not output: 
			return output
		return output

	def register(self):
		return self.player.register(name)
			
	def receive_stone(self, stone_type):
		if isinstance(stone_type, StoneEnum):
			self.player.receive_stone(stone_type)
		else:
			raise Exception("Not a proper player stone.")

	def make_a_move(self, board_history):
		return self.player.choose_move(board_history)

if __name__ == "__main__":
	print("launched")
	go_config = json.load(open('go.config'))
	HOSTNAME = go_config['IP']
	PORT = go_config['port']
	
	time.sleep(1)
	print("running")
	player = GoPlayerProxy()
	player.turn_on_socket((HOSTNAME, PORT))
	done = "not done"
	while done != "done":
		done = player.work_with_socket()
	player.turn_off_socket()
