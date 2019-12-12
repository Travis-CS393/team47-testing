import sys, json, socket, time, random
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../5/5.1/src/')
sys.path.append('../../../5/5.2/src/')
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from obj_parser import parse_stone, parse_boards
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, EMPTY_STONE, WHITE_STONE, BLACK_STONE, GAME_OVER, GAME_OVER_RESPONSE
from go_player_base import GoPlayerBase
from go_player_adv import GoPlayerAdv
from go_gui import GoGUIPlayer


class GoRemotePlayer():

   def __init__(self):
      self.player = GoGUIPlayer(name=None)
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.game_over = False

   def turn_on_socket(self, ip_and_port):
      self.socket.connect(ip_and_port)

   def work_with_socket(self):
      try:
         inpt = self.socket.recv(8192)
         print("received")
         print(inpt.decode("utf-8"))
         output = self.work_JSON(json.loads(inpt.decode("utf-8")))
         if not output:
            pass
         else:
            print('sending')
            print(output)
            self.socket.sendall(bytes(output, "utf-8"))
            print('sent')
      except:
         self.game_over = True
         print("Game is Over!")

   def turn_off_socket(self):
      self.socket.close()

   def work_JSON(self, input):
      obj = input
      print("working with socket")
      print(obj)
      if obj[0] == REGISTER:
         output = self.register()
      
      
      elif obj[0] == RECEIVE:
         if obj[1] == BLACK_STONE:
            stone_e = StoneEnum.BLACK
         elif obj[1] == WHITE_STONE:
            stone_e = StoneEnum.WHITE
         else:
            print("RC: Invalid stone type.")
            raise Exception()
         self.receive_stone(stone_e)
         output = None
         return output
      
      
      elif obj[0] == MOVE:
         boards_obj = parse_boards(obj[1])
         print("trying")
         output = self.make_a_move(boards_obj)
         print("found one")
         if isinstance(output, tuple):
            output = get_raw(output)
      
      
      elif obj[0] == GAME_OVER:
         output = GAME_OVER_RESPONSE
      
      else:
         print("RC: Invalid JSON input.")
         raise Exception()
      
      output = "\"" + output + "\""
      return output     

   def register(self):
      return self.player.register()

   def receive_stone(self, stone_type):
      if isinstance(stone_type, StoneEnum):
         self.player.receive_stone(stone_type)
      else:
         print("RC: Not a proper player stone.")
         raise Exception()

   def make_a_move(self, board_history):
      return self.player.choose_move(board_history)

if __name__ == "__main__":
   print("launched")
   go_config = json.load(open('go.config'))
   HOSTNAME = go_config['IP']
   PORT = go_config['port']
   
   time.sleep(1)
   print("running")
   player = GoRemotePlayer()
   player.turn_on_socket((HOSTNAME, PORT))
   while not player.game_over:
      player.work_with_socket()

   """
   done = 0
   while done != 0.05:
      player.work_with_socket()
      done += 1
   """

   player.turn_off_socket()