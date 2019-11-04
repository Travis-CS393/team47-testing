import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from json_parser import json_parse_stdin
from point import get_raw
from referee_formatter import format_pretty_json
from obj_parser import parse_boards, parse_stone
from constants import REGISTER, RECEIVE, MOVE, PASS, BLACK_STONE, WHITE_STONE
from play_parser import format_input
from output_formatter import format_board_if_valid
from go_referee import GoReferee

def execute_input(play, referee):
	input_play = format_input(play)
	return referee.execute_move(input_play)



if __name__ == "__main__":
	objs = json_parse_stdin()
	output = []
	referee = GoReferee(player1=objs[0], player2=objs[1])
	output.append(BLACK_STONE)
	output.append(WHITE_STONE)
	hello = []
	for obj in objs[2:]:

		raw_out = execute_input(obj, referee)
		output.append(raw_out)

		if referee.game_over:
			if (not referee.winner_declared):
				output.append(referee.get_winners())
				referee.winner_declared = True
			else:
				break

	output = list(filter(None, output))

	formatted_output = []
	for item in output:
		formatted_output.append(format_board_if_valid(item))

	print(format_pretty_json(formatted_output))
