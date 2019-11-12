import sys, multiprocessing, time
import socket
import json
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from json_parser import json_parse_stdin
from constants import BOARD_DIM
from test_driver_base import execute_input
from referee_parser import parse_board
from referee_formatter import format_pretty_json
from go_player_adv import GoPlayerAdv
from remote_player import GoPlayerProxy

def valid_move_input(input):
   if len(input) != 2:
      return False
   if input[0] != "make-a-move":
      return False

   if len(input[1]) > 3 or len(input[1]) < 1:
      return False

   try:
      for board in input[1]:
         print(parse_board(board))
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

   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.bind((HOSTNAME, PORT))
      server_socket.listen()
      client_socket, address = server_socket.accept()
      with client_socket:
         if objs[0] != ["register"]:
            output.append("GO has gone crazy!")
            game_terminated = True
         else:
            registered = True
            client_socket.sendall(bytes(json.dumps(objs[0]), "utf-8"))
            data = client_socket.recv(8192)
            output.append(data.decode("utf-8"))

         if (objs[1] != ["receive-stones", "B"]) and (objs[1] != ["receive-stones", "W"]) and not game_terminated:
            output.append("GO has gone crazy!")
            game_terminated = True
         else:
            received = True
            if registered:
               client_socket.sendall(bytes(json.dumps(objs[1]), "utf-8"))
               data = client_socket.recv(8192)

         for input in objs[2:]:
            if not game_terminated:
               if valid_move_input(input):
                  client_socket.sendall(bytes(json.dumps(input), "utf-8"))
                  ret_val = client_socket.recv(8192)
                  if ret_val.decode("utf-8") == "no name" or ret_val.decode("utf-8") == "None":
                     output.append("GO has gone crazy!")
                     break
                  else:
                     output.append(ret_val.decode("utf-8"))
               else:
                  output.append("GO has gone crazy!")
                  game_terminated = True
                  break
            else:
               break

         client_socket.sendall(b'done')
      server_socket.close()



   """
   output = []
   if objs[0] != ["register"]:
      output.append("GO has gone crazy!")
      game_terminated = True
   else:
      registered = True
      output.append(json.JSONDecoder().decode(player.work_JSON(json.JSONEncoder().encode(objs[0]))))

   if (objs[1] != ["receive-stones", "B"]) and (objs[1] != ["receive-stones", "W"]) and not game_terminated:
      output.append("GO has gone crazy!")
      game_terminated = True 
   else:
      if registered:
         output.append(player.work_JSON(json.JSONEncoder().encode(objs[1])))

   for input in objs[2:]:
      if not game_terminated:
         ret_val = json.JSONDecoder().decode(player.work_JSON(json.JSONEncoder().encode(input)))
         if ret_val == "no name" or not ret_val:
            output.append("GO has gone crazy!")
            break
         else:
            output.append(ret_val)
      else:
         break
      """
   ## Filter for nulls
   filtered = list(filter(lambda x: x, output))
   print(format_pretty_json(filtered))
   #print(filtered)