import sys, json, socket, time, random

sys.path.append('../../3/3.1/src/')
from constants import EMPTY_STONE, WHITE_STONE, BLACK_STONE
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from obj_parser import parse_stone, parse_boards
from output_formatter import format_board

sys.path.append('../../5/5.1/src/')
from go_player_base import GoPlayerBase

sys.path.append('../../5/5.2/src/')
from go_player_adv import GoPlayerAdv


class GoPlayerProxy():

	def __init__(self, n=1):
		self.player = GoPlayerBase("player-no{}".format(random.randint(0, 750)))
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def turn_on_socket(self, ip_and_port):
		self.socket.connect(ip_and_port)


	def work_with_socket(self):
		try:
			inpt = self.socket.recv(8192)
			print(inpt)
			if inpt.decode("utf-8") == "done":
				return "done"
			else:
				output = self.work_JSON(json.loads(inpt.decode("utf-8")))
				if not output:
					pass
				else:
					print('sending')
					print(output)
					self.socket.sendall(bytes(output, "utf-8"))
					print('sent')
				return "not done"
		except:
			return "Error: no connection established"



	def turn_off_socket(self):
		self.socket.close()

	def work_JSON(self, input):
		obj = input
		print("working with socket")
		if obj[0] == 'register':
			output = self.register("no name")
		
		elif obj[0] == 'receive-stones':
			if obj[1] == BLACK_STONE:
				stone_e = StoneEnum.BLACK
			elif obj[1] == WHITE_STONE:
				stone_e = StoneEnum.WHITE
			else:
				raise Exception("Invalid stone type")
			self.receive_stone(stone_e)
			output = None
		
		elif obj[0] == "make-a-move":
			boards_obj = parse_boards(obj[1])
			print("trying")
			#output = self.make_a_move(boards_obj)
			x = random.randrange(1,9)
			y = random.randrange(1,9)
			output = (x, y)
			print("found one")
			output = get_raw(output)
		else:
			raise Exception("Invalid JSON input")
		return output		


	def register(self, name):
		if isinstance(name, str):
			return self.player.register()
		else:
			raise Exception("Not a proper player name.")
			
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

	#go_player_config = json.load(open('go-player.config'))
	#N = go_player_config['depth']
	
	time.sleep(1)
	print("running")
	player = GoPlayerProxy()
	player.turn_on_socket((HOSTNAME, PORT))
	done = "not done"
	while done != "done":
		done = player.work_with_socket()
	player.turn_off_socket()