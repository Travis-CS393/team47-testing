import sys, socket, time, json
sys.path.append('./../../3/3.1/src')
from point import str_to_point, PointException
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
		self.remote_player_proxy = RemotePlayerProxy(connection)


	def register(self):
		p_name = self.remote_player_proxy.register()
		self.name = p_name
		return p_name


	def receive_stone(self, stone_type):
		self.remote_player_proxy.receive_stone(stone_type)
		

	def choose_move(self, boards):
		try:
			p_move = self.remote_player_proxy.choose_move(boards)
			p_move = p_move.replace("\"","")
			if p_move == PASS:
				return PASS
			else:
				move_point = str_to_point(p_move)
				return (move_point.x, move_point.y)
		except PointException:
			raise PointException("Invalid move.")


	def game_over(self, end_tag):
		try:
			response = self.remote_player_proxy.game_over(end_tag)
			response = response.replace("\"","")
			return (response == GAME_OVER_RESPONSE)
		except:
			return False
