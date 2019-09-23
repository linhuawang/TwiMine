from tkinter import *
from twimine import *
import time
import os
from glob import glob
import sys
from PIL import ImageTk, Image

class GUI(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		#self.grid()

		self.usernameLabel = Label(master, text='Twitter Username', bg='white', fg = 'black',font='Helvetica 20 bold', highlightbackground='#3E4149')
		self.usernameLabel.place(relx=0.5, rely=0.2, anchor=CENTER)

		self.usernameEntry = StringVar()
		self.usernameEntry = Entry(textvariable=self.usernameEntry, bg='grey')
		self.usernameEntry.place(relx=0.5, rely=0.3, anchor=CENTER)

		self.displayLabel = Label(master, text = 'Display Option', bg='white', fg = 'black', font='Helvetica 20 bold', highlightbackground='#3E4149')
		self.displayLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

		self.displayEntry = StringVar()
		self.displayEntry = Entry(textvariable=self.displayEntry, bg='grey')
		self.displayEntry.place(relx=0.5, rely =0.5, anchor = CENTER)

		self.postUpperLabel = Label(master, text='Max #post',bg='white', fg = "black", font='Helvetica 20 bold', highlightbackground='#3E4149')
		self.postUpperLabel.place(relx=0.5, rely=0.6, anchor=CENTER)

		self.postUpperEntry = StringVar()
		self.postUpperEntry = Entry(textvariable=self.postUpperEntry, bg='grey')
		self.postUpperEntry.place(relx=0.5, rely=0.7, anchor=CENTER)



		def buttonClick():			
			twimine(self.usernameEntry.get(), self.displayEntry.get(), int(self.postUpperEntry.get()))
			with open('username.txt', 'wt') as f:
				f.write(self.usernameEntry.get())
			print("Start to display......")
			os.system('python display.py')

		self.enterButton = Button(master, font ='Helvetica 20 bold',highlightcolor='blue', bg = 'black', fg = 'green', command =buttonClick, text="Enter")
		self.enterButton.place(relx=0.3, rely = 0.8, anchor=CENTER)
		

		def quickClick():
			sys.exit(0)
		self.quickButton = Button(master, font = 'Helvetica 20 bold',  highlightcolor='red', bg='black', fg = 'red', command = quickClick, text = "Quit")
		self.quickButton.place(relx = 0.7, rely=0.8, anchor=CENTER)
		
if __name__ == "__main__":
	if os.path.exists("tmp/"):
		pngs = glob('tmp/*.png')
		for png in pngs:
			os.remove(png)

	master = Tk()
	master.title("TwiMine")
	master.geometry("1000x800")
	C = Canvas(master, bg="blue", height=1000, width=800)
	C.pack(expand=YES, fill=BOTH)
	img = ImageTk.PhotoImage(Image.open("keke4.jpg"))
	C.create_image(0, 0, image=img, anchor=NW)
	
	twimine_GUI = GUI(master)
	twimine_GUI.mainloop()





