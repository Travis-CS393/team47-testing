import sys, json, time, multiprocessing
sys.path.append('../../3/3.1/src/')
from json_parser import json_parse_stdin
from referee_parser import is_board, is_move, parse_board, parse_move
from referee_formatter import format_score, format_pretty_json
from score_referee import ScoreReferee
from move_referee import MoveReferee

def execute_input(arr):
   if is_board(arr):
      referee = ScoreReferee()
      result = referee.get_score(parse_board(arr))
      return format_score(result)
   elif is_move(arr):
      referee = MoveReferee()
      stone_type, move = parse_move(arr)
      return referee.valid_play(stone_type, move)
   else:
      raise Exception("invalid input")

if __name__ == "__main__":
   objs = json_parse_stdin()
   p = multiprocessing.Pool(len(objs))
   output = list(p.map(execute_input, objs))
   print(format_pretty_json(output))