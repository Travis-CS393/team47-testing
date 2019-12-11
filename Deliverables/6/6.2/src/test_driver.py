import sys
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../4/4.1/src/')
sys.path.append('../../../5/5.1/src/')
from stone import StoneEnum
from json_parser import json_parse_stdin
from output_formatter import format_board_if_valid
from constants import BLACK_STONE, WHITE_STONE
from referee_formatter import format_pretty_json
from go_referee import GoReferee
from play_parser import format_input
from go_player_base import GoPlayerBase

def execute_input(play, referee):
	input_play = format_input(play)
	return referee.execute_move(input_play)

if __name__ == "__main__":
	objs = json_parse_stdin()
	output = []
	referee = GoReferee(player1=GoPlayerBase(objs[0]), player2=GoPlayerBase(objs[1]))
	referee.players[StoneEnum.BLACK] = referee.player1
	referee.players[StoneEnum.WHITE] = referee.player2
	output.append(BLACK_STONE)
	output.append(WHITE_STONE)

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
