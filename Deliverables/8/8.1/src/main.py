import sys, json, socket
sys.path.append('../../../3/3.1/src/')
from stone import StoneEnum
from point import Point, str_to_point
from output_formatter import format_board
sys.path.append('../../../6/6.2/src')
from go_referee import GoReferee
sys.path.append('../../../8/8.1/src')
from go_admin import GoAdmin
from remote_player_proxy import RemotePlayerProxy


#local player import
go_config = json.load(open('go.config'))
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from go_player_base import GoPlayerBase

#remote player import
go_config = json.load(open('go.config'))
HOSTNAME = go_config['IP']
PORT = go_config['port']

if __name__ == "__main__":
	go_admin = GoAdmin(IP=HOSTNAME, port=PORT, local_player=GoPlayerBase)
	winner = go_admin.run_game()
	print(winner)
