import sys, json
sys.path.append('./src')
from go_tournament_admin import GoTournamentAdmin

## FINAL CODEWALK NOTES:
# Jenny Lam IP: "10.105.46.243"
# Daniel Bang IP: 

#player import
go_config = json.load(open('go.config'))
HOSTNAME = go_config['IP']
PORT = go_config['port']
DEFAULT_PLAYER_PATH = go_config['default-player']
sys.path.append(DEFAULT_PLAYER_PATH)
from go_player_base import GoPlayerBase


#tournament import
tournament_details = sys.argv
print(tournament_details)
TOURNAMENT = tournament_details[1]
NUM_REMOTES = tournament_details[2]


if __name__ == "__main__":
	go_tournament_admin = GoTournamentAdmin(default_player_type=GoPlayerBase, IP=HOSTNAME, port=PORT, tournament_type=TOURNAMENT, n=int(NUM_REMOTES))
	standings = go_tournament_admin.run_tournament()
	print(standings)