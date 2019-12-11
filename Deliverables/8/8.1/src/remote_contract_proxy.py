import sys, socket, time, json
sys.path.append('../../../3/3.1/src')
from point import str_to_point
from stone import Stone, make_stone
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, PASS, GAME_OVER_RESPONSE
from remote_player_proxy import RemotePlayerProxy

class RemoteContractProxy():
	def __init__(self, connection):
		"""
		This class implements a remote player proxy contract which
		has the same interface as the player, but checks
		the sent and received messages for validity.
		"""
		self.name = None
      self.remoteplayerproxy = RemotePlayerProxy(connection)

	def register(self):
		p_name = self.remoteplayerproxy.register()
		if type(p_name) == str:
         return p_name
      else:
         raise TypeError("Invalid type: name must be a string")

	def receive_stone(self, stone_type):
		self.remoteplayerproxy.receive_stone(stone_type)

	def choose_move(self, boards):
		p_move = self.remoteplayerproxy.choose_move(boards)
      if p_move == "\"pass\"":
         return PASS
      else:
         move_point = str_to_point(p_move) # Exception will be here in point class
		   return (move_point.x, move_point.y)
		

	def game_over(self, end_tag):
		response = self.remoteplayerproxy.game_over(end_tag)
      if response == GAME_OVER_RESPONSE:
         return response
      else:
         raise ValueError("Invalid response to Game Over.")
