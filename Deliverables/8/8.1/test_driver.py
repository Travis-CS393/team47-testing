import sys
import json
import socket
sys.path.append('../../3/3.1/src/')
from stone import StoneEnum
from point import Point, str_to_point
sys.path.append('../../4/4.1/src/')
sys.path.append('../../6/6.2/')
sys.path.append('../../8/8.1/')
from go_referee import GoReferee
from go_admin import GoAdmin
from remote_player_proxy import RemotePlayerProxy

#remote player import
go_config = json.load(open('go.config'))
HOSTNAME = go_config['IP']
PORT = go_config['port']

if __name__ == "__main__":
	go_admin = GoAdmin(IP=HOSTNAME, port=PORT)
	winner = go_admin.run_game()
	print(winner)
