import sys, json
sys.path.append('../../9/9.1/')
from go_tournament_admin import GoTournAdmin

#player import
go_config = json.load(open('go.config'))
DEFAULT_PLAYER_PATH = go_config['default-player']
sys.path.append(DEFAULT_PLAYER_PATH)
from go_player_base import GoPlayerBase
HOSTNAME = go_config['IP']
PORT = go_config['port']

#tournament import
tourney_details = sys.argv
print(tourney_details)
TOURNAMENT = tourney_details[1]
REMOTES = tourney_details[2]

if __name__ == "__main__":
	go_tournament_admin = GoTournAdmin(default_player_type=GoPlayerBase, IP=HOSTNAME, port=PORT, tourney=TOURNAMENT, n=int(REMOTES))
	standings = go_tournament_admin.run_tournament()
	print(standings)