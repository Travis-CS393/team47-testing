import sys
sys.path.append('./../../3/3.1/src/')
sys.path.append('./../../4/4.1/src/')
from point import get_raw
from json_parser import json_parse_stdin
from obj_parser import parse_boards, parse_stone
from constants import REGISTER, RECEIVE, MOVE
from referee_formatter import format_pretty_json
from go_player_base import GoPlayerBase

def execute_input(player, arr):
   if arr[0] == REGISTER:
      return player.register()
   elif arr[0] == RECEIVE:
      stone = parse_stone(arr[1])
      player.receive_stone(stone.get_type())
   elif arr[0] == MOVE:
      boards = parse_boards(arr[1])
      output = player.choose_move(boards)
      if isinstance(output, str):
         return output
      return get_raw(output)
   else:
      raise Exception("Invalid name given to execute input")

if __name__ == "__main__":
   player = GoPlayerBase()
   objs = json_parse_stdin()
   output = filter (lambda x: x, [execute_input(player, obj) for obj in objs])
   print(format_pretty_json(list(output)))
