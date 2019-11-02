import json
from input_parser import InputParser
from json_parser import json_parse_stdin
from output_formatter import format_board, format_board_if_valid, format_points, format_pretty_json

def execute_input(input_array):
   input_parser = InputParser(input_array)
   board, statement = input_parser.get_board(), input_parser.get_statement()

   if statement == "occupied?":
      point = input_parser.get_point()
      return board.occupied(point)

   elif statement == "occupies?":
      stone_type, point = input_parser.get_stone_and_point()
      return board.occupies(stone_type, point)

   elif statement == "reachable?":
      point, stone_type = input_parser.get_point_and_stone()
      return board.reachable(point, stone_type)

   elif statement == "place":
      stone_type, point = input_parser.get_stone_and_point()
      return format_board_if_valid(board.place_stone(stone_type, point))

   elif statement == "remove":
      stone_type, point = input_parser.get_stone_and_point()
      return format_board_if_valid(board.remove_stone(stone_type, point))

   elif statement == "get-points":
      stone_type = input_parser.get_stone()
      return format_points(board.get_points(stone_type))

if __name__ == "__main__":
   objs = json_parse_stdin()
   output = list(map(execute_input, objs))
   print (format_pretty_json(output))