import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from json_parser import json_parse_stdin
from point import get_raw
from referee_formatter import format_pretty_json
from obj_parser import parse_boards, parse_stone
from constants import REGISTER, RECEIVE, MOVE
from go_player_base import GoPlayerBase

def execute_input(play):
   pass

if __name__ == "__main__":
   player = GoPlayerBase()
   objs = json_parse_stdin()
   output = []
   #output = filter (lambda x: x, [execute_input(play) for obj in objs])
   print(format_pretty_json(list(output)))
