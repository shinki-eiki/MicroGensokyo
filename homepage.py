from tkinter import *
from time import time
from choose import Choose
from tkinter import simpledialog
from function import *#changeImage,changeIma,changeIma2

class HomePage():
	#canvas,home,title,button,choose
	# def __init__(self,r):
	# 	self.canvas=Label(r,bg='grey')
	# 	changeIma(self.canvas,'homepage')
	# 	root=self.home=Label(self.canvas,bg='lightgrey')
	# 	root.place(relx=0.4,relwidth=0.2,relheight=1)
	# 	self.title=Label(root,text='Micro\nGensokyo',font='粗体 20')
	# 	self.button=[]
	# 	text=['新游戏','卡其脱离太','载入','退出']
	# 	fun=[self.newGame,self.quickGame,self.loadGame,r.quit]
	# 	for i in range(4):
	# 		self.button.append(Button(
	# 			root,font='粗体 14',text=text[i],command=fun[i]))
	# 		self.button[i].place(rely=0.5+i*0.105,relwidth=1,relheight=0.1)
	# 	self.title.place(rely=0.1,relheight=0.2,relwidth=1)
	# 	self.choose=Choose(self.canvas,self)
	# 	self.place()
	def __init__(self,r):
		self.canvas=Label(r,bg='grey')
		changeIma(self.canvas,'homepage')
		root=self.home=Label(self.canvas,bg='palegoldenrod')
		root.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.42)
		self.title=Label(self.canvas,text='Micro\nGensokyo',font='粗体 20')
		self.button=[]
		text=['新游戏','卡其脱离太','载入','退出']
		fun=[self.newGame,self.quickGame,self.loadGame,r.quit]
		for i in range(4):
			self.button.append(Button(
				root,font='粗体 14',text=text[i],command=fun[i]))
			self.button[i].place(rely=i*0.13,relwidth=1,relheight=0.12)
		self.title.place(relx=0.4,rely=0.1,relheight=0.2,relwidth=0.2)
		self.choose=Choose(self.canvas,self)
		# self.place()
	

	def newGame(self):
		n=simpledialog.askinteger('','How many players?')
		if not n:return
		self.home.place_forget()
		# self.chooseFrame.place(relx=0.2,rely=0.41,relheight=0.58,relwidth=0.5)
		self.choose.place(n)

	def place(self):
		self.canvas.place(relheight=1,relwidth=1)
		self.home.place(relx=0.4,relheight=1,relwidth=0.2)
	
	def place_forget(self):
		self.canvas.place_forget()
	
	# def cancel(self):
	# 	self.place()

	def quickGame(self):pass
	def startGame(self,n):
		print('start')
		res=['faith','money','rice']
		for i in range(n):
			t=typeVar[i].get()
			print(f'Player {i+1} has no {res[t]}.')
	
	def changeAva(self):
		print('avatar')
	
	def loadGame(self):
		print('loadGame')
if __name__ == "__main__":
	w,h=1280,800
	root=Tk()
	root.geometry("%dx%d+0+0" %(w,h))
	# root.attributes("-alpha", 0.9)
	root.title('Micro Gensokyo')
	h=HomePage(root)
	h.place()
	root.mainloop()
	# def text(*e):
		
	# root=Tk()

# t=['所有头像','玩家头像','缺少的资源种类']
# 		res=['faith','money','rice']
# 		f=self.frame=[]
# 		v=self.var=[]
# 		self.badiobutton=[]
# 		for i in range(3):
# 			f.append(LabelFrame(root,text=t[i]))
# 			v.append(IntVar(value=-1))
# 		for i in range(6):
# 			self.player.append(Radiobutton(
# 				f[1],width=width0,height=width0,value=i,variable=v[0],command=self.changeAva))
# 			self.typeVar.append(IntVar(value=0))
# 			self.res.append(Frame(
# 				f[2],width=1width0,height=width0))
# 			for j in range(3):
# 				self.radiobutton.append(Radiobutton(
# 					width=width0,height=width0,value=j,variable=self.typeVar[i]))
# 				self.radiobutton.pack()
# 		self.confirm=Button(root,text='comfirm',command=self.startGame)