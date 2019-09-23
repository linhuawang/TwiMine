from tkinter import *
from twimine import *
from glob import glob 
from PIL import Image, ImageTk
from os import system
from os.path import exists
import sys

with open("username.txt", 'rt') as f:
	username = f.readline().split("\n")[0]

if not exists("tmp/"):
	sys.exit("No results available!")

img_fns = glob("tmp/{}_*.png".format(username))


root = Tk()
root.title("TwiMine Results")


img = ImageTk.PhotoImage(Image.open(img_fns[0]))
panel = Label(root, image=img)
# panel.pack(side="bottom", fill="both", expand="yes")
panel.grid(row=1, column=1)

current = 0

def forward():
	global current
	if current < len(img_fns):
		current += 1
		try:
			img2 = ImageTk.PhotoImage(Image.open(img_fns[current]))
			panel.configure(image=img2)
			panel.image = img2
			root.update_idletasks()
		except:
			pass

def backward():
	global current
	if current > 0:
		current -= 1
		try:
			img_back = ImageTk.PhotoImage(Image.open(img_fns[current]))
			panel.configure(image=img_back)
			panel.image = img_back
			root.update_idletasks()
		except:
			pass

forward_button = Button(root, command=forward, text = 'Next', bd=5, fg='green', highlightbackground='#3E4149', width=10)
forward_button.grid(row=0, column=2)

backward_button = Button(root, command=backward, text = 'Previous', bd=5, fg='blue',  highlightbackground='#3E4149', width=10)
backward_button.grid(row=0, column=0)


# quit_button = Button(root, command=sys.exit, text='Quit', bd=5, fg='red', width=10)
# quit_button.grid(row=2, column=1)

root.mainloop()