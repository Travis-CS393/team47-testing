import sys, json, socket
sys.path.append('../src')
from go_admin import GoAdmin


go_config = json.load(open('go.config'))
#remote player import
HOSTNAME = go_config['IP']
PORT = go_config['port']
#local player import
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from go_player_base import GoPlayerBase


if __name__ == "__main__":
	go_admin = GoAdmin(IP=HOSTNAME, port=PORT, local_player=GoPlayerBase)
	winner = go_admin.run_game()
	print(winner)
