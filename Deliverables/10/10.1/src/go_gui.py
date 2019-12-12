import sys, json, socket, threading
from tkinter import * 
from tkmacosx import Button
from PIL import ImageTk, Image
sys.path.append("../../../3/3.1/src/")
from point import str_to_point
sys.path.append("../../../4/4.1/src/")
from move_referee import MoveReferee
sys.path.append("../../../8/8.1/src/")
from go_admin import GoAdmin
from constants import BOARD_DIM, BLACK_STONE, WHITE_STONE, PASS
from stone import Stone, StoneEnum
from copy import deepcopy
go_config = json.load(open('go.config'))
#remote player import
HOSTNAME = go_config['IP']
PORT = go_config['port']
#local player import
default_player_path = go_config['default-player']
sys.path.append(default_player_path)
from go_player_base import GoPlayerBase


class GoGUIPlayer():
	## Decorators
	def valid_stone(func):
		def wrapper(*args, **kwargs):
			if not args[1] or not isinstance(args[1], StoneEnum):
				raise Exception("GPB: Invalid parameter, bad stone passed.")
				return func(*args, **kwargs)
			return wrapper

	def protocol_registered(func):
		def wrapper(*args, **kwargs):
			if not args[0].name:
				raise Exception("GPB: Invalid protocol, player must be registered first.")
				return func(*args, **kwargs)
			return wrapper

	def protocol_stone_set(func):
		def wrapper(*args, **kwargs):
			if not args[0].stone_type:
				raise Exception("GPB: Invalid protocol, stone must be received first.")
				return func(*args, **kwargs)
			return wrapper


	def __init__(self, name=None):
		self.name = name
		self.default_name = "Player 1"
		self.stone_type = None
		self.color = ""
		self.move_referee = MoveReferee()
		self.click = None
		
		# Creates self.root window
		self.root = Tk()
		self.root.title("Go Game GUI")
		self.root.resizable(0, 0)
		self.root.geometry('1000x1000') 

		self.e = Entry(self.root, text="ENTER YOUR NAME HERE", width=20, borderwidth=5, bg="yellow", fg="black")
		self.e.grid(row=0, column=0, columnspan=7)
		
		self.e1 = Entry(self.root, width=20, borderwidth=5, bg="yellow", fg="black")
		self.e1.grid(row=10, column=0, columnspan=7)

		self.button_register = Button(self.root, text="Register", command=self.myClick)
		self.button_move = Button(self.root, text="Make Move", command=self.myMove)
		self.pass_move = Button(self.root, text="Pass", command=self.Pass)
		self.button_register.grid(row=0, column=10, columnspan=1)
		self.button_move.grid(row=10, column=10, columnspan=1)
		self.pass_move.grid(row=9, column=10, columnspan=1)
		
		self.buttons = dict()
		for x in range(1, BOARD_DIM+1):
			for y in range(1, BOARD_DIM+1):
				button_num = "{}-{}".format(y,x)
				self.buttons["{}-{}".format(y,x)] = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda butt=button_num: self.button_click(butt))
				self.buttons["{}-{}".format(y,x)].grid(row=x, column=y, columnspan=1)


		


	def myClick(self):
		self.name = self.e.get()
		hello = "Welcome to Go, " + self.name
		myLabel = Label(self.root, text=hello)
		myLabel.grid(row=0, column=0, columnspan=3)
		self.button_register.configure(state=DISABLED)
		


	def myMove(self):
		if self.name:
			self.click = self.e1.get()
	
	def Pass(self):
		if self.name:
			self.click = "pass"


	def register(self):
		while not self.name:
			self.root.update()
			self.root.update_idletasks()
		return self.name

	def receive_stone(self, stone_type):
		self.stone_type = stone_type
		if stone_type == StoneEnum.BLACK:
			self.color = "black"
		else:
			self.color =  "white"

	def choose_move(self, boards):
		if not self.move_referee.valid_history(self.stone_type, boards):
			return "This history makes no sense!"
		else:
			board = boards[0]
			for x in range(len(board)):
				for y in range(len(board[0])):
					if board[x][y].get_raw() == WHITE_STONE:
						self.buttons["{}-{}".format(x+1,y+1)].configure(bg="white")
					elif board[x][y].get_raw() == BLACK_STONE:
						self.buttons["{}-{}".format(x+1,y+1)].configure(bg="black")
					else:
						self.buttons["{}-{}".format(x+1,y+1)].configure(bg="goldenrod")
						
			while not self.click:
				self.root.update()
				self.root.update_idletasks()
			if self.click == "pass":
				self.click = None
				return PASS
				
			ret = str_to_point(self.click)
			#if not self.move_referee.valid_move(stone_type=self.stone_type, point=ret, boards=boards, current_board=board):
			#	raise Exception("Invalid point.")
			self.click = None
			return (ret.x, ret.y)

	def button_click(self, button_idx):
		if self.name:
			self.click = button_idx
			self.buttons[self.click].configure(bg=self.color)



if __name__ == "__main__":

	# Main Event Loop
	root = GoGUIPlayer(BOARD_DIM)
	root.root.mainloop()
	
	
	


