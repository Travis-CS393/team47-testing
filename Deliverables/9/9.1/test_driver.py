import sys
import json
import socket
sys.path.append('../../3/3.1/src/')
from stone import StoneEnum
from point import Point, str_to_point
sys.path.append('../../4/4.1/src/')
sys.path.append('../../6/6.2/')
sys.path.append('../../8/8.1/')
sys.path.append('../../9/9.1/')
from go_referee import GoReferee
from go_admin import GoAdmin
from go_tournament_admin import GoTournAdmin

#player import
go_config = json.load(open('go.config'))
HOSTNAME = go_config['IP']
PORT = go_config['port']

#tournament import
tourney_details = sys.argv
print(tourney_details)
TOURNAMENT = tourney_details[1]
REMOTES = tourney_details[2]

if __name__ == "__main__":
	print("on")
	go_tournament_admin = GoTournAdmin(IP=HOSTNAME, port=PORT, tourney=TOURNAMENT, n=REMOTES)
	ranks = go_tournament_admin.run_tournament()
	print(ranks)