import sys, multiprocessing, time
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
   player = GoPlayerProxy()
   objs = json_parse_stdin()
   game_terminated = False

   output = []
   if objs[0] != ["register"]:
      output.append("GO has gone crazy!")
      game_terminated = True
   else:
      output.append(player.work_JSON(json.dumps(objs[0])))

   if (objs[1] != ["receive-stones", "B"]) and (objs[1] != "receive-stones", "W") and not game_terminated:
      output.append("GO has gone crazy!")
      game_terminated = True 

   for input in objs[2:]:
      if not game_terminated:
         ret_val = player.work_JSON(json.dumps(input))
         if json.JSONDecoder.encode(ret_val) == "no name" or not json.JSONDecoder.encode(ret_val):
            output.append("GO has gone crazy!")
            game_terminated = True
         else:
            output.append(ret_val)
      else:
         break
   ## Filter for nulls
   filtered = list(filter(lambda x: x, output))
   print(format_pretty_json(filtered))