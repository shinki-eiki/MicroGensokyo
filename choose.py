from tkinter import *
from function import *
from time import sleep

class Choose():
	#imageLabel,text,tipLabel,frame,var,typeVar,name,player,image,res,confirm,exit,
	def __init__(self,grandpa,home):
		self.home=home
		self.father=grandpa
		father=self.vessel=Frame(grandpa,bg='lightgrey')
		self.imageLabel=LabelFrame(father,text='可选头像')
		self.label=[ ]
		self.imageVar=IntVar(value=-1)
		for i in range(9):
			self.label.append(Radiobutton(
				self.imageLabel,value=i,variable=self.imageVar,indicatoron=0))
			changeImageWithName(self.label[i],i,1)
			self.label[i].pack(side='left')
		self.var=IntVar(value=-1)
		t=self.typeVar=[]

		self.text=StringVar(value='请设置:')
		self.tipLabel = Label( father, textvariable=self.text, font=['黑体', 14, 'bold'] )
		text=['玩家名字','玩家头像','缺少的资源种类']
		res=['信仰','钱币','食物']
		width0=70
		f=self.frame=[]
		for i in range(3):
			self.frame.append(LabelFrame(father,text=text[i]))
		#
		self.name,self.player,self.image,self.res=[],[],[],[]
		for i in range(8):
			self.name.append( Entry(f[0]) )#,height=width0
			self.player.append(Radiobutton(f[1],width=70,height=70,bg='lightgrey'
				,indicatoron=0,text=str(i),value=i,variable=self.var,command=self.changeAva))
			changeImageWithName(self.player[i],i,1)
			self.typeVar.append(IntVar(value=0))
			self.res.append(Frame(f[2],width=3*width0,height=width0))
			for j in range(3):
				Radiobutton(self.res[i],text=res[j],height=2,
					value=j,variable=self.typeVar[i]).pack(side='left')#
		self.confirm=Button(f[1],text='确定',command=self.startGame)
		self.exit=Button(f[1],text='退出',command=self.cancel)

		self.imageLabel.place(relheight=0.15,relwidth=1)
		self.tipLabel.place(rely=0.155,relheight=0.1,relwidth=1)
		f[0].place(relx=0,rely=0.255,relwidth=0.3,relheight=0.7)
		f[1].place(relx=0.31,rely=0.255,relwidth=0.3,relheight=0.7)
		f[2].place(relx=0.62,rely=0.255,relwidth=0.37,relheight=0.7)
		self.confirm.place(rely=0.92,relwidth=0.48)
		self.exit.place(rely=0.92,relx=0.5,relwidth=0.48)

	def place(self,n):
		self.vessel.place(relx=0.2,rely=0,relheight=1,relwidth=0.6)
		self.num=n
		for i in range(n):
			self.name[i].pack(pady=28,fill=X)
			self.player[i].pack()#pady=5
			self.res[i].pack(pady=15)
	
	def place_forget(self):
		self.vessel.place_forget()
		for i in range(self.num):
			self.name[i].pack_forget()
			self.player[i].pack_forget()
			self.res[i].pack_forget()
	
	def changeAva(self):
		self.imageVar.set(-1)
		who=self.var.get()
		self.text.set('请选择上面的一张图片:')
		while True:
			sleep(0.2)
			self.tipLabel.update()
			no=self.imageVar.get()
			if no==-1:continue
			photo=self.label[no]
			photo=photo['image']
			changeImageWithPhoto(self.player[who],photo)
			self.text.set('请设置:')
			break
	
	def cancel(self):
		self.place_forget()
		self.home.place()
	
	def startGame(self):
		name,photo,res=[],[],[]
		for i in range(self.num):
			name.append(self.name[i].get())
			p=self.player[i]
			photo.append(p['image'])
			res.append(self.typeVar[i].get())
		self.home.startGame(name,photo,res)
		# print(name,res)