from tkinter import * 
from tkmacosx import Button
from PIL import ImageTk, Image

# Creates root window
root = Tk()
root.title("Go Game GUI")
root.resizable(0, 0)
root.geometry('782x454') 

# root.iconbitmap("path")

#black_img = ImageTk.PhotoImage(Image.open("black_stone.png"))
#white_img = ImageTk.PhotoImage(Image.open("white_stone.png"))

e = Entry(root, width=35, borderwidth=5, bg="blue", fg="white")
e.grid(row=0, column=0, columnspan=9)

""""
def myClick():
	hello = "Welcome to Go, " + e.get()
	myLabel = Label(root, text=hello)
	myLabel.pack()
"""
def button_click(button_idx):
	board_buttons[button_idx].configure(bg="black")
	#current = e.get()
	#e.delete(0, END)
	#e.insert(0, str(current) + str(number))

# Define buttons
button_11 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(0))
button_21 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(1))
button_31 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(2))
button_41 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(3))
button_51 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(4))
button_61 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(5))
button_71 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(6))
button_81 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(7))
button_91 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(8))
 
button_12 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(9))
button_22 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(10))
button_32 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(11))
button_42 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(12))
button_52 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(13))
button_62 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(14))
button_72 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(15))
button_82 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(16))
button_92 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(17))

button_13 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(18))
button_23 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(19))
button_33 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(20))
button_43 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(21))
button_53 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(22))
button_63 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(23))
button_73 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(24))
button_83 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(25))
button_93 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(26))
 
button_14 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(27))
button_24 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(28))
button_34 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(29))
button_44 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(30))
button_54 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(31))
button_64 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(32))
button_74 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(33))
button_84 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(34))
button_94 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(35))
 
button_15 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(36))
button_25 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(37))
button_35 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(38))
button_45 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(39))
button_55 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(40))
button_65 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(41))
button_75 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(42))
button_85 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(43))
button_95 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(44))
 
button_16 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(45))
button_26 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(46))
button_36 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(47))
button_46 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(48))
button_56 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(49))
button_66 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(50))
button_76 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(51))
button_86 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(52))
button_96 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(53))
 
button_17 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(54))
button_27 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(55))
button_37 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(56))
button_47 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(57))
button_57 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(58))
button_67 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(59))
button_77 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(60))
button_87 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(61))
button_97 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(62))
 
button_18 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(63))
button_28 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(64))
button_38 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(65))
button_48 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(66))
button_58 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(67))
button_68 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(68))
button_78 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(69))
button_88 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(70))
button_98 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(71))

button_19 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(72))
button_29 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(73))
button_39 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(74))
button_49 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(75))
button_59 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(76))
button_69 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(77))
button_79 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(78))
button_89 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(79))
button_99 = Button(root, text=" ", bg="goldenrod", padx=0.0, pady=20, command=lambda: button_click(80))

#button_quit = Button(root, text="Exit Program", command=root.quit)

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

button_17.grid(row=6, column=0, columnspan=1)
button_27.grid(row=6, column=1, columnspan=1)
button_37.grid(row=6, column=2, columnspan=1)
button_47.grid(row=6, column=3, columnspan=1)
button_57.grid(row=6, column=4, columnspan=1)
button_67.grid(row=6, column=5, columnspan=1)
button_77.grid(row=6, column=6, columnspan=1)
button_87.grid(row=6, column=7, columnspan=1)
button_97.grid(row=6, column=8, columnspan=1)

button_18.grid(row=6, column=0, columnspan=1)
button_28.grid(row=6, column=1, columnspan=1)
button_38.grid(row=6, column=2, columnspan=1)
button_48.grid(row=6, column=3, columnspan=1)
button_58.grid(row=6, column=4, columnspan=1)
button_68.grid(row=6, column=5, columnspan=1)
button_78.grid(row=6, column=6, columnspan=1)
button_88.grid(row=6, column=7, columnspan=1)
button_98.grid(row=6, column=8, columnspan=1)

button_19.grid(row=7, column=0, columnspan=1)
button_29.grid(row=7, column=1, columnspan=1)
button_39.grid(row=7, column=2, columnspan=1)
button_49.grid(row=7, column=3, columnspan=1)
button_59.grid(row=7, column=4, columnspan=1)
button_69.grid(row=7, column=5, columnspan=1)
button_79.grid(row=7, column=6, columnspan=1)
button_89.grid(row=7, column=7, columnspan=1)
button_99.grid(row=7, column=8, columnspan=1)

board_buttons = [button_11, button_21, button_31, button_41, button_51, button_61, button_71, button_81, button_91,
				button_12, button_22, button_32, button_42, button_52, button_62, button_72, button_82, button_92,
				button_13, button_23, button_33, button_43, button_53, button_63, button_73, button_83, button_93,
				button_14, button_24, button_34, button_44, button_54, button_64, button_74, button_84, button_94,
				button_15, button_25, button_35, button_45, button_55, button_65, button_75, button_85, button_95,
				button_16, button_26, button_36, button_46, button_56, button_66, button_76, button_86, button_96,
				button_17, button_27, button_37, button_47, button_57, button_67, button_77, button_87, button_97,
				button_18, button_28, button_38, button_48, button_58, button_68, button_78, button_88, button_98,
				button_19, button_29, button_39, button_49, button_59, button_69, button_79, button_89, button_99]

# Creating widgets
#myLabel1 = Label(root, text="Welcome to a game of GO!")
#myLabel2 = Label(root, text="Welcome to a game of GO!")
# fg -> fore font, bg -> background
#myButton = Button(root, text="Enter your name.", command=myClick)

# Placing widgets on screen 
#myButton.pack()
#myButton.grid()
#myLabel.pack()
#myLabel1.grid(row= 0, column=0)
#myLabel2.grid(row= 1, column=1)


# Main Event Loop
root.mainloop()


