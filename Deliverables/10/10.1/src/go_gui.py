import sys, json, socket, threading
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
		self.move_referee = MoveReferee()
		
		# Creates self.root window
		self.root = Tk()
		self.root.title("Go Game GUI")
		self.root.resizable(0, 0)
		self.root.geometry('1000x1000') 

		# self.root.iconbitmap("path")

		#black_img = ImageTk.PhotoImage(Image.open("black_stone.png"))
		#white_img = ImageTk.PhotoImage(Image.open("white_stone.png"))

		self.e = Entry(self.root, width=35, borderwidth=5, bg="blue", fg="white")
		self.e.grid(row=0, column=0, columnspan=7)

		def myClick():
			hello = "Welcome to Go, " + self.e.get()
			myLabel = Label(self.root, text=hello)
			myLabel.grid(row=0, column=0, columnspan=9)
			button_register.configure(state=DISABLED)
			self.name = self.e.get()

		button_register = Button(self.root, text="Register", command=myClick)
		
		self.e1 = Entry(self.root, width=35, borderwidth=5, bg="blue", fg="white")
		self.e1.grid(row=10, column=0, columnspan=7)

		def myMove():
			self.click = self.e1.get()

		button_move = Button(self.root, text="Make Move", command=myMove)
		""""
		self.buttons = dict()
		for x in range(1, BOARD_DIM+1):
			for y in range(BOARD_DIM):
				button_num = "{}-{}".format(y+1,x)
				self.buttons["{}-{}".format(x,y)] = Button(self.self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click(button_num))
				self.buttons["{}-{}".format(x,y)].grid(row=x, column=y, columnspan=1)
		"""
		button_11 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-1"))
		button_21 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-1"))
		button_31 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-1"))
		button_41 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-1"))
		button_51 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-1"))
		button_61 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-1"))
		button_71 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-1"))
		button_81 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-1"))
		button_91 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-1"))
		 
		button_12 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-2"))
		button_22 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-2"))
		button_32 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-2"))
		button_42 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-2"))
		button_52 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-2"))
		button_62 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-2"))
		button_72 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-2"))
		button_82 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-2"))
		button_92 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-2"))

		button_13 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-3"))
		button_23 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-3"))
		button_33 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-3"))
		button_43 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-3"))
		button_53 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-3"))
		button_63 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-3"))
		button_73 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-3"))
		button_83 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-3"))
		button_93 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-3"))
		 
		button_14 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-4"))
		button_24 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-4"))
		button_34 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-4"))
		button_44 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-4"))
		button_54 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-4"))
		button_64 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-4"))
		button_74 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-4"))
		button_84 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-4"))
		button_94 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-4"))
		 
		button_15 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-5"))
		button_25 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-5"))
		button_35 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-5"))
		button_45 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-5"))
		button_55 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-5"))
		button_65 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-5"))
		button_75 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-5"))
		button_85 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-5"))
		button_95 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-5"))
		 
		button_16 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-6"))
		button_26 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-6"))
		button_36 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-6"))
		button_46 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-6"))
		button_56 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-6"))
		button_66 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-6"))
		button_76 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-6"))
		button_86 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-6"))
		button_96 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-6"))
		 
		button_17 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-7"))
		button_27 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-7"))
		button_37 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-7"))
		button_47 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-7"))
		button_57 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-7"))
		button_67 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-7"))
		button_77 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-7"))
		button_87 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-7"))
		button_97 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-7"))
		 
		button_18 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-8"))
		button_28 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-8"))
		button_38 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-8"))
		button_48 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-8"))
		button_58 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-8"))
		button_68 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-8"))
		button_78 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-8"))
		button_88 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-8"))
		button_98 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-8"))

		button_19 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("1-9"))
		button_29 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("2-9"))
		button_39 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("3-9"))
		button_49 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("4-9"))
		button_59 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("5-9"))
		button_69 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("6-9"))
		button_79 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("7-9"))
		button_89 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("8-9"))
		button_99 = Button(self.root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: self.button_click("9-9"))

		#button_quit = Button(self.root, text="Exit Program", command=self.root.quit)

		# Put buttons on the screen
		button_11.grid(row=1, column=0, columnspan=1)
		button_21.grid(row=1, column=1, columnspan=1)
		button_31.grid(row=1, column=2, columnspan=1)
		button_41.grid(row=1, column=3, columnspan=1)
		button_51.grid(row=1, column=4, columnspan=1)
		button_61.grid(row=1, column=5, columnspan=1)
		button_71.grid(row=1, column=6, columnspan=1)
		button_81.grid(row=1, column=7, columnspan=1)
		button_91.grid(row=1, column=8, columnspan=1)

		button_12.grid(row=2, column=0, columnspan=1)
		button_22.grid(row=2, column=1, columnspan=1)
		button_32.grid(row=2, column=2, columnspan=1)
		button_42.grid(row=2, column=3, columnspan=1)
		button_52.grid(row=2, column=4, columnspan=1)
		button_62.grid(row=2, column=5, columnspan=1)
		button_72.grid(row=2, column=6, columnspan=1)
		button_82.grid(row=2, column=7, columnspan=1)
		button_92.grid(row=2, column=8, columnspan=1)

		button_13.grid(row=3, column=0, columnspan=1)
		button_23.grid(row=3, column=1, columnspan=1)
		button_33.grid(row=3, column=2, columnspan=1)
		button_43.grid(row=3, column=3, columnspan=1)
		button_53.grid(row=3, column=4, columnspan=1)
		button_63.grid(row=3, column=5, columnspan=1)
		button_73.grid(row=3, column=6, columnspan=1)
		button_83.grid(row=3, column=7, columnspan=1)
		button_93.grid(row=3, column=8, columnspan=1)

		button_14.grid(row=4, column=0, columnspan=1)
		button_24.grid(row=4, column=1, columnspan=1)
		button_34.grid(row=4, column=2, columnspan=1)
		button_44.grid(row=4, column=3, columnspan=1)
		button_54.grid(row=4, column=4, columnspan=1)
		button_64.grid(row=4, column=5, columnspan=1)
		button_74.grid(row=4, column=6, columnspan=1)
		button_84.grid(row=4, column=7, columnspan=1)
		button_94.grid(row=4, column=8, columnspan=1)

		button_15.grid(row=5, column=0, columnspan=1)
		button_25.grid(row=5, column=1, columnspan=1)
		button_35.grid(row=5, column=2, columnspan=1)
		button_45.grid(row=5, column=3, columnspan=1)
		button_55.grid(row=5, column=4, columnspan=1)
		button_65.grid(row=5, column=5, columnspan=1)
		button_75.grid(row=5, column=6, columnspan=1)
		button_85.grid(row=5, column=7, columnspan=1)
		button_95.grid(row=5, column=8, columnspan=1)

		button_16.grid(row=6, column=0, columnspan=1)
		button_26.grid(row=6, column=1, columnspan=1)
		button_36.grid(row=6, column=2, columnspan=1)
		button_46.grid(row=6, column=3, columnspan=1)
		button_56.grid(row=6, column=4, columnspan=1)
		button_66.grid(row=6, column=5, columnspan=1)
		button_76.grid(row=6, column=6, columnspan=1)
		button_86.grid(row=6, column=7, columnspan=1)
		button_96.grid(row=6, column=8, columnspan=1)

		button_17.grid(row=7, column=0, columnspan=1)
		button_27.grid(row=7, column=1, columnspan=1)
		button_37.grid(row=7, column=2, columnspan=1)
		button_47.grid(row=7, column=3, columnspan=1)
		button_57.grid(row=7, column=4, columnspan=1)
		button_67.grid(row=7, column=5, columnspan=1)
		button_77.grid(row=7, column=6, columnspan=1)
		button_87.grid(row=7, column=7, columnspan=1)
		button_97.grid(row=7, column=8, columnspan=1)

		button_18.grid(row=8, column=0, columnspan=1)
		button_28.grid(row=8, column=1, columnspan=1)
		button_38.grid(row=8, column=2, columnspan=1)
		button_48.grid(row=8, column=3, columnspan=1)
		button_58.grid(row=8, column=4, columnspan=1)
		button_68.grid(row=8, column=5, columnspan=1)
		button_78.grid(row=8, column=6, columnspan=1)
		button_88.grid(row=8, column=7, columnspan=1)
		button_98.grid(row=8, column=8, columnspan=1)

		button_19.grid(row=9, column=0, columnspan=1)
		button_29.grid(row=9, column=1, columnspan=1)
		button_39.grid(row=9, column=2, columnspan=1)
		button_49.grid(row=9, column=3, columnspan=1)
		button_59.grid(row=9, column=4, columnspan=1)
		button_69.grid(row=9, column=5, columnspan=1)
		button_79.grid(row=9, column=6, columnspan=1)
		button_89.grid(row=9, column=7, columnspan=1)
		button_99.grid(row=9, column=8, columnspan=1)

		button_register.grid(row=0, column=8, columnspan=2)
		button_move.grid(row=10, column=8, columnspan=2)

		self.board_buttons = [button_11, button_21, button_31, button_41, button_51, button_61, button_71, button_81, button_91,
							button_12, button_22, button_32, button_42, button_52, button_62, button_72, button_82, button_92,
				button_13, button_23, button_33, button_43, button_53, button_63, button_73, button_83, button_93,
				button_14, button_24, button_34, button_44, button_54, button_64, button_74, button_84, button_94,
				button_15, button_25, button_35, button_45, button_55, button_65, button_75, button_85, button_95,
				button_16, button_26, button_36, button_46, button_56, button_66, button_76, button_86, button_96,
				button_17, button_27, button_37, button_47, button_57, button_67, button_77, button_87, button_97,
				button_18, button_28, button_38, button_48, button_58, button_68, button_78, button_88, button_98,
				button_19, button_29, button_39, button_49, button_59, button_69, button_79, button_89, button_99, 
				button_register]

		self.board_buttons_dict = dict()
		count = 0
		for x in range(1, BOARD_DIM+1):
			for y in range(1, BOARD_DIM+1):
				self.board_buttons_dict["{}-{}".format(y,x)] = self.board_buttons[count]
				count += 1
				print(count)

		self.click = None
		while True:
			#self.root.mainloop()
			self.root.update()

	def register(self):
		while not self.name:
			pass
		return self.name

	def receive_stone(self, stone_type):
		self.stone_type = stone_type

	def choose_move(self, boards):
		if not self.move_referee.valid_history(self.stone_type, boards):
			return "This history makes no sense!"
		else:
			while not self.click:
				pass
			return self.click


	def button_click(self, button_idx):
		self.click = button_idx

if __name__ == "__main__":

	# Main Event Loop
	root = GoGUIPlayer(BOARD_DIM)
	root.root.mainloop()

	
	


