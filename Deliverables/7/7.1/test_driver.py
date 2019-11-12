import sys, multiprocessing, time
import socket
import json
sys.path.append('../../3/3.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
from json_parser import json_parse_stdin
from test_driver_base import execute_input
from referee_formatter import format_pretty_json
from go_player_adv import GoPlayerAdv
from remote_player import GoPlayerProxy

if __name__ == "__main__":
   game_terminated = False
   registered = False
   received = False
   objs = json_parse_stdin()
   output = []

   go_config = json.load(open('go.config'))
   HOSTNAME = go_config['IP']
   PORT = go_config['port']

   # NEED FUNCTIONS TO CONFIGURE SERVER SIDE SOCKET 
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.bind((HOSTNAME, PORT))
      server_socket.listen()
      print("running")
      client_socket, address = server_socket.accept()
      while True:
         print("connected")
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
                  #output.append(data.decode("utf-8"))

            for input in objs[2:]:
               if not game_terminated:
                  client_socket.sendall(bytes(json.dumps(input), "utf-8"))
                  ret_val = client_socket.recv(8192)
                  if ret_val.decode("utf-8") == "no name" or ret_val.decode("utf-8") == "None":
                     output.append("GO has gone crazy!")
                     break
                  else:
                     output.append(ret_val.decode("utf-8"))
               else:
                  break

            client_socket.sendall(b'done')
            break
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