import sys, multiprocessing, time, socket, json
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../4/4.1/src/')
sys.path.append('../../../8/8.1/src/')
sys.path.append('../src/')
from stone import Stone, make_stone
from json_parser import json_parse_stdin
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, BLACK_STONE, WHITE_STONE, GAME_OVER
from referee_formatter import format_pretty_json
from referee_parser import parse_board
from remote_contract_proxy import RemoteContractProxy


def valid_move_input(input):
   if len(input) != 2:
      return False
   if input[0] != MOVE:
      return False
   if len(input[1]) > 3 or len(input[1]) < 1:
      return False

   try:
      for board in input[1]:
         parse_board(board)
   except:
      return False
   
   return True 


if __name__ == "__main__":
   game_terminated = False
   registered = False
   received = False
   objs = json_parse_stdin()
   output = []

   go_config = json.load(open('go.config'))
   HOSTNAME = go_config['IP']
   PORT = go_config['port']
   print(HOSTNAME)
   print(PORT)

   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server_socket.bind((HOSTNAME, PORT))
   server_socket.listen()
   client_socket, address = server_socket.accept()

   remote_player = RemoteContractProxy(client_socket)

   if objs[0] != [REGISTER]:
      output.append("GO has gone crazy!")
      game_terminated = True
   else:
      registered = True
      output.append(remote_player.register())

   if (objs[1] != [RECEIVE, BLACK_STONE]) and (objs[1] != [RECEIVE, WHITE_STONE]) and not game_terminated:
      output.append("GO has gone crazy!")
      game_terminated = True
   else:
      received = True
      if registered:
         remote_player.receive_stone(Stone(objs[1][1]).get_type())

   for input in objs[2:]:
      if not game_terminated:
         if valid_move_input(input):
            move_response = remote_player.choose_move(input)
            if move_response == "default_player" or move_response == "None":
               output.append("GO has gone crazy!")
               break
            else:
               output.append(move_response)
         else:
            output.append("GO has gone crazy!")
            game_terminated = True
            break
      else:
         break

   remote_player.game_over([GAME_OVER])
   server_socket.close()

   ## Filter for nulls
   filtered = list(filter(lambda x: x, output))
   print(format_pretty_json(filtered))
