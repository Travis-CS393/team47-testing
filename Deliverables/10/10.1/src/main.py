import sys, json, socket
from tkinter import * 
from tkmacosx import Button
from PIL import ImageTk, Image
sys.path.append("../../../3/3.1/src/")
sys.path.append("../../../4/4.1/src/")
from move_referee import MoveReferee
sys.path.append("../../../8/8.1/src/")
from go_admin import GoAdmin
from constants import BOARD_DIM

go_config = json.load(open('go.config'))
#remote player import
HOSTNAME = go_config['IP']
PORT = go_config['port']
#local player import
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from go_player_base import GoPlayerBase
from go_gui import GoGUIPlayer

if __name__ == "__main__":
	go_admin = GoAdmin(IP=HOSTNAME, port=PORT, local_player=GoGUIPlayer)
	winner = go_admin.run_game()
	print(winner)
	
	


