import sys, multiprocessing, time
sys.path.append('../../3/3.1/src/')
sys.path.append('../../5/5.1/src/')
from json_parser import json_parse_stdin
from test_driver_base import execute_input
from referee_formatter import format_pretty_json
from go_player_adv import GoPlayerAdv

if __name__ == "__main__":
   def call_exec(obj):
      return execute_input(player, obj)
   player = GoPlayerAdv()
   objs = json_parse_stdin()

   ## First recieve stone, then use threading
   output = list(map(call_exec, objs[0:2]))
   p = multiprocessing.Pool(len(objs) - 2)
   output += list(map(call_exec, objs[2:]))

   ## Filter for nulls
   filtered = filter(lambda x: x, output)
   print (format_pretty_json(list(filtered)))