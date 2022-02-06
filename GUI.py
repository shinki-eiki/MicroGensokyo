from card import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook #,Treeview,Combobox
from tkinter import simpledialog,messagebox
from playerButton import PlayerButton
from cardButton import CardButton
from choose import Choose
from function import *
#changeImage,changeIma,changeImageWithPhoto
from random import randint #,shuffle
from time import sleep  # time,
# from json import loads

#from testTkinter import SmallTop,Top
#from player import *

# def findIndex(name,aim):
# 	for i in range(len(name)):
# 		if name[i]==aim:return i
# 	return None

class Basic():
	#explain,show,showText
	def __init__(self):
		self.card=[]
		for i in self.button:
			i.bind('<Enter>',self.explain)
	def explain(self,event):
		index=event.widget['value']
		c=self.card
		if(index>=len(c)):return
		Gui.explain(c[index])
	def show(self,cards,reset=True):
		self.card=cards
		n=len(self.card)
		if(n>8):n=8
		for i in range(n):
			self.text[i].set(self.showText(i))
		for i in range(n,9):
			self.text[i].set('')
			self.button[i].config(bg='grey')
	def showText(self,i):
		if (self.card==[]):return ''
		return self.card[i].name
	def append(self):
		n=len(self.card)-1
		if(n>8):return
		self.text[n].set(self.showText(n))

# 玩家信息以及游戏记录
class Other():
	place=('一般怪兽区','可捕获怪兽区','设施区',
		'手牌','迂返区','打出区')
	def __init__(self,father):
		ce=self.book=Notebook(father)
		f =self.frame=[]
		pageName=['记录','玩家']
		for i in range(2):
			f.append(Frame(ce, bg='grey', relief='sunken'))
			ce.add(f[i],text=pageName[i])
		self.message=ScrolledText(f[0],undo=True,fg='lightgreen',cursor='pencil',
			font='黑体 13',bg='grey')#,state='disabled
		ce.place(relwidth=1,relheight=0.9)
		self.message.place(relheight=1,relwidth=1)
		#
		#height=2,
		# sf=self.showFrame=Frame(f[1],bg='paleturquoise')
		# # self.showFrame.place(rely=0.55,relheight=0.5,relwidth=1)
		sn=self.showNum=[IntVar(value=-1) for i in range(3)]
		self.showVar=StringVar(value='一般怪兽区')
		self.var=IntVar(value=-1)
		self.button=[PlayerButton(f[1],'','黑体 15 bold',variable=self.var,value=i,
			indicatoron=0,anchor='nw',command=self.changePlayer) for i in range(8)]

		sb=self.showButton=OptionMenu(f[1],self.showVar,command=self.show,*Other.place)
		# sb.bind('<<ComboboxSelected>>',self.show)
		# sb['value']=Other.place
		nl=self.numLabel=Label(f[1],textvariable=sn[0],bg='lightgrey')
		sb.place(rely=0.92,relwidth=0.8,relheight=0.08)
		nl.place(relx=0.8,rely=0.92,relwidth=0.2,relheight=0.08)

		self.throw=Button(father,text='弃牌堆',bg='grey',anchor='w',command=self.showThrow)
		self.throw.place(rely=0.9,relwidth=0.4,relheight=0.1)
		self.deck =Button(father,text='卡组', bg='grey',anchor='w',command=self.showDeck)
		self.deck .place(relx=0.5,rely=0.9,relwidth=0.4,relheight=0.1)
		Label(father,textvariable=sn[1],bg='grey').place(relx=0.4,rely=0.9,relwidth=0.1,relheight=0.1)
		Label(father,textvariable=sn[2],bg='grey').place(relx=0.9,rely=0.9,relwidth=0.1,relheight=0.1)

	def show(self,event,show=True):
		who=self.var.get()
		name=self.showVar.get()
		place=Other.place.index(name)
		p=Player.player[who]
		if place==3:#手牌需要去掉空位
			card=[]
			for i in p.hand:
				if i !=None:card.append(i)
		else:
			card=p.guide[place]
		n=len(card)
		self.showNum[0].set(n)
		if show:
			Gui.askOne2(card,p.name,Other.place[place])
	def newMessage(self,text):
		self.message.insert(END,text)
		self.message.see(END)
	def showThrow(self):
		# return Player.cp.showThrow()
		who=self.var.get()
		p=Player.player[who]
		card=p.throw
		# Gui.isSpecial.set(false)
		Gui.askOne2(card,p.name,'弃牌堆')
		
	def showDeck(self):
		i=self.var.get()
		return Player.player[i].showDeck()

	def newPlayer(self,name,without,first):
		self.total=len(without)
		self.first=first
		b=self.button
		p=Player.player
		for i in range(self.total):
			t=''
			if i<first:t+=str(self.total-first+i+1)
			else:t+=str(i-first+1)
			t+=':'+name[i]+'\n'
			for j in range(3):
				if without[i]!=j:t+=Card.char[j]
			Gui.newMessage(t)
			b[i].setText(t)
			b[i].changeImageWithPhoto(p[i].image)
			b[i].place2(0.14*i)
			# b[i].pack(fill=X,pady=2)
		# father=self.frame[1]
		# t=self.tree=Treeview(father,columns=('1'))
		# t.heading('#0',text='name')
		# t.heading('#1',text='resource')
		# t.place(relheight=1,relwidth=1)
		# for i in range(self.total):
		# 	v=''
		# 	t.insert('',index=END,text=name[i],values=v)

	def changePlayer(self):
		who=self.var.get()
		name=self.showVar.get()
		place=Other.place.index(name)
		p=Player.player[who]
		n=len(p.guide[place])
		self.showNum[0].set(n)
		n=len(p.throw)
		self.showNum[1].set(n)
		n=len(p.deck)
		self.showNum[2].set(n)
	
	def next(self):
		self.var.set(Player.now)
		self.changePlayer()

	def showShuffle(self,n):
		self.showNum[1].set(0)
		self.showNum[2].set(n)

class Resource():
	"""docstring for ClassName"""
	def __init__(self,father):
		name=['信仰','钱币','食物']
		self.var=[IntVar() for i in range(6)]
		# self.label=[Label(father,font=['黑体',25],fg='lightgreen',
		# 	bg='darkcyan',text=name[x]) for x in range(9)]
		a=self.label=[Label(father,font=['黑体',14,'bold'],fg='lightgreen',
			bg='darkcyan',text=name[x]) for x in range(3)]
		b=self.resource=[Label(father,font=['黑体',16,'bold'],fg='lightgreen',
			bg='darkcyan',textvariable=self.var[x]) for x in range(3)]
		c=self.exResource=[Label(father,font=['黑体',16,'bold'],fg='lightgreen',
			bg='darkcyan',textvariable=self.var[x+3]) for x in range(3)]
		for i in range(3):
			a[i].place(relx=0.34*i,relheight=0.32,relwidth=0.32)
			b[i].place(relx=0.34*i,rely=0.335,relheight=0.32,relwidth=0.32)
			c[i].place(relx=0.34*i,rely=0.67,relheight=0.32,relwidth=0.32)
	
	def show(self,res):#
		for i in range(3):
			self.var[i].set(res[i])
	def showex(self):
		res=Player.exResource
		for i in range(3):
			self.var[i+3].set(res[i])

class Center(Basic):
	"""docstring for ClassName"""
	#button,text,var,people,card,cover
	placeName=['守矢神社','命莲寺','神灵庙','博丽神社','永远亭'
		,'白玉楼','魔法之森','地灵殿','红魔馆','兽道','人间之里']
	theEmpty=[10]
	def __init__(self, father,*exceptOne):
		# b=self.text=[]
		# a=self.label=[]
		# #Gui.newMessage(color)
		#Center.placeName.pop(exceptOne)

		c=self.button=[]
		self.var=IntVar(value=-1)
		self.remain=8
		self.coverImage=findCardImage('cover')#背面图片
		self.remainCard=[0]*9
		
		height0=-0.038 #0.1
		weight0=0.178
		for i in range(9):#a is text,c is image
			# b.append(StringVar())
			# a.append(Radiobutton(father,textvariable=b[i],font=['黑体',13],
			# 	indicatoron=0,variable=self.var,value=i,command=self.toGain))
			c.append(Radiobutton(father, #bg='grey, #justify='center',
				indicatoron=0,variable=self.var,value=i,command=self.toGain))
			if(i!=8):
				# a[i].place(relx=(i%4)*0.2,rely=0.02 if i<4 else 0.5
				# 	,relheight=height0,relwidth=0.19,)#relwidth=0.19,
				c[i].place(relx=(i%4)*0.2,rely=(0.05 if i<4 else (0.52-height0) )+height0,
					relwidth=weight0,relheight=0.42-height0)#width=160,height=160)#
		c[8].place(relx=0.8,rely=0.05+height0,relheight=0.42-height0,relwidth=weight0)#width=160,height=160,)
		for i in range(3):
			c.append(Radiobutton(father,command=self.toGain,#justify='center',
				indicatoron=0,variable=self.var,value=9+i))
			c[i+9].place(relx=0.8,rely=0.52+0.16*i,relwidth=weight0,relheight=0.16)		
			changeImageWithPhoto(c[i+9],findCardImage(f"10{i+6}"))
		Basic.__init__(self)
		# a[8].place(relx=0.8,rely=0.02,relheight=height0,relwidth=0.19)
		# for i in self.label:
		# 	i.bind('<Enter>',self.explain)

	def isOver(self,n):return self.remain<=7-n

	def newGame(self):
		Center.theEmpty=[10]
		exceptOne=randint(0,8)
		Gui.newMessage('被删除的牌堆为',Center.placeName[exceptOne])
		self.initCard(exceptOne)

		# Hand.pop(exceptOne)
		color=['green','orchid','palegoldenrod','crimson','paleturquoise',
		'pink','lightgrey','silver','orangered','lightgreen','burlywood']#
		color.pop(exceptOne)
		for i in range(9):
			# self.label[i].config(bg=color[i])
			self.button[i].config(bg=color[i])
			self.remainCard[i]=len(self.card[i])
	
	def initCard(self,exceptOne):			
		self.cover=[]
		self.card=[[] for s in range(13)]
		Card.newCenter(self.card,exceptOne)
		for i in range(12):#所有框设置图片,
			card=self.card[i].pop()
			self.cover.append(card)
			if i<9: changeImageWithCard(self.button[i],card)
			# if i<9:self.text[i].set(card.inCenter())
			
	def explain(self,event):
		var=event.widget['value']
		c=self.cover[var]
		if(c==None):return #Gui.explain('已拿空')
		else:
			t=str(c)
			if(var<9):t+=f'\n\t\t\t\t\t\t(还剩余{self.remainCard[var]}张)'
			Gui.explain(t)

	def next(self,no):
		if(no>8):return
		a=self.cover
		c=self.card[no]
		self.remainCard[no]-=1
		if(c==[]):#拿走最后一张,兽道不影响结束与否
			where=a[no].place
			if(no!=8):
				self.remain-=1
				Center.theEmpty.append(where)
			# self.text[no].set(Card.placeName[where])
			Gui.newMessage(f'{Center.placeName[where]}已拿空！')
			a[no]=None
			changeImageWithPhoto(self.button[no],self.coverImage)
		else:
			changeImageWithPhoto(self.button[no],self.coverImage)
			self.button[no].update()
			sleep(0.2)
			a[no]=c.pop()
			# self.text[no].set(a[no].inCenter())
			changeImageWithCard(self.button[no],a[no])
			self.button[no].update()
			if 5 in a[no].skill:
				Player.checkMiracle(a[no].name)

	def toGain(self):
		if(Gui.isSpecial):return
		v=self.var.get()
		c=self.cover[v]
		if(c==None):return #已经拿空了，无响应
		Player.cp.gain(v,c)
		self.var.set(-1)
	
	def checkMiracle(self):
		for i in range(8):
			if 5 in self.cover[i].skill:
				Player.checkMiracle(self.cover[i].name)

	def askEmpty(self):
		name=''
		for i in Center.theEmpty:
			name+=Center.placeName[i]+' '
		Gui.newMessage('已拿空:',name)
		return Center.theEmpty

	def sortThree(self,no):
		card=[]
		all=self.card[no]
		if len(all)>1:
			card.append(all.pop())
			card.append(all.pop())
		else:
			card=all
		cover=self.cover[no]
		card.append(cover)
		card=Gui.top.sort(card,'幽幽子的折扇')
		newCover=card.pop()
		self.cover[no]=newCover
		# self.text[no].set(newCover.inCenter())
		changeImageWithCard(self.button[no],newCover)
		self.button[no].update()
		if 5 in newCover.skill:
			Player.checkMiracle(newCover.name)
		all+=card

class Hand(Basic):
	color=['green','orchid','yellow','red','paleturquoise',
		'pink','lightgrey','silver','orangered','lightgreen','burlywood']
	# placeName=['守矢神社','命莲寺','神灵庙','博丽神社','永远亭'
	# 	,'白玉楼','魔法之森','地灵殿','红魔馆','兽道','人间之里']
	
	def __init__(self,father):
		self.num,self.max=0,0
		self.weight=0.14
		# t=self.text=[None]*35
		#self.index=[]#self.max=0
		#代表showing的数量
		self.var=IntVar(value=-1)
		a=self.button=[None]*35
		self.showing=[]
		self.card=[]
		for i in range(35):
			#self.index.append(i+1)
			# t[i]=StringVar()#justify='center',#command=self.toGain
			a[i]=CardButton(father,#['黑体',16],
				bg='darkcyan',indicatoron=0,variable=self.var,
				value=i,compound='bottom',command=self.use)
			a[i].bind(self.explain)
		#Basic.__init__(self)

	def pop(n):
		Hand.color.pop(n)
		Hand.placeName.pop(n)
	def use(self):
		if(Gui.isSpecial):return
		index=self.var.get()
		Player.cp.use(index)
		self.var.set(-1)
	def showText(self,i):
		c=self.card[i]
		#changeImageWithCard(self.button[i],c)#
		if c!= None:self.button[i].changeImageWithCard(c)
		if c==None:
			Gui.newMessage(f'第{i}张牌出错')
			return None
		return c.inHand()
	def show(self,card):
	#新玩家刷新手牌，
	#注意不要用列表做默认常数，不然是持续存在且可变的
		self.num=self.max=len(card)
		self.card=card
		self.place_forget()
		for i in range(self.num):
			self.button[i].changeImageWithCard(self.card[i])
		self.showing=self.button[0:self.num]
		self.rePlace()
			# t=self.showText(i)
			# if t!=None:self.text[i].set(t)
			# else:self.showing.pop(i)

	def append(self):#包括设置文本图片，以及放置
		#根据值找到新框并设置，然后加入showing		
		m=self.max
		b=self.button[m]
		card=self.card[-1]
		# if card==None:print(card)
		# else:self.text[m].set(card.inHand())
		b.changeImageWithCard(card)
		self.showing.append(b)
		self.max+=1
		self.num+=1
		if(self.num==7):self.rePlace()
		else:	 		self.place()
	
	def lost(self,no):
		s=self.showing
		i=0#先根据value来找到并隐藏
		for i in range(self.num):
			if(s[i].var==no):
				self.num-=1
				#self.text[i].set('')
				s[i].place_forget()
				s.pop(i)
				break		
		#再安置后面的卡牌
		n=self.num
		if  (n>6):#只要手牌多就必须重放
			self.rePlace()
		elif(n!=i):self.rePlace(i)
		#else#手牌少且刚好最后一张，无事发生
	
	def rePlace(self,first=0):
		# fix=0
		n=self.num
		if(n<8):x=self.weight
		else:   x=1/n
		for i in range(first,n):#
			self.showing[i].placeHand(x*i)
			# if self.card[i]!=None:
			# else:fix-=x
			#relx=,relwidth=0.15,relheight=1
	
	def place(self):
		n=self.num
		if(n<8):#手牌少时
			n-=1
			self.showing[n].placeHand(self.weight*n)
			#relx=0.15*n,relwidth=0.15,relheight=1
		else:#手牌多时，需要从头到尾重放
			x=1/n
			for i in range(1,n):
				self.showing[i].placeHand(x*i)
				#relx=x*i,relwidth=0.15,relheight=1
	
	def place_forget(self,*event):
		for i in self.showing: i.place_forget()

class Top():
	def __init__(self,father):
		a=self.top=Toplevel(father,bg='grey')
		a.protocol('WM_DELETE_WINDOW',self.canNotDelete)
		w = father.winfo_screenwidth()
		h = father.winfo_screenheight()
		a.geometry("%dx%d+%d+%d" %(1000,300,280,200))#w*0.8,h/2.5,w/5,h/4
		a.withdraw()
		self.tip=StringVar()
		self.tipLabel=Label(a,font=['黑体',15],bg='lightgrey',
			textvariable=self.tip)
		self.tipLabel.place(relx=0.1,relheight=0.1,relwidth=0.8)
		self.var=IntVar(value=-1)
		ce=self.center=Notebook(a)
		f=self.frame=[]
		for i in range(8):
			f.append(Frame(ce,bg='grey'))
			ce.add(f[i],text=f'第{i+1}页')
		ce.place(rely=0.1,relwidth=1,relheight=0.75)
		t=self.text=[]#[None]*25
		self.button=[]
		#self.frame=Frame(a,bg='grey')
		for i in range(48):
			t.append(StringVar(value=i))
			self.button.append(CardButton(f[i//6],#['黑体',12],
				indicatoron=0,value=i,bg='paleturquoise',variable=self.var))
			self.button[i].bind(self.explain)
		self.card=[]
		self.cancel=IntVar(value=-1)
		# self.confirmButton=Radiobutton(a,text='confirm',value=1,variable=self.cancel,indicatoron=0)
		# self.confirmButton.place(relx=0.35,rely=0.9,relwidth=0.15,relheight=0.1)
		self.cancelButton =Radiobutton(a,text='cancel', value=-2,variable=self.var,indicatoron=0)
		self.cancelButton .place(relx=0.4, rely=0.85,relwidth=0.15,relheight=0.15)
	def explain(self,event):
		index=event.widget['value']
		c=self.card
		if(index>=len(c)):return
		Gui.explain(c[index])
	def canNotDelete(self):
		oldText=self.tip.get()
		self.tip.set('Please do not delete!')
		self.top.update()
		sleep(1.5)
		self.tip.set(oldText)
	def place(self,n):
		for i in range(n):
			#self.button[i].pack(side='left')
			self.button[i].place(i%6*0.16,0)
	def place_forget(self,n):
		for i in range(n):
			self.button[i].place_forget()
	def show(self,page=1):
		for i in range(page*6+6):
			#self.button[i].pack(side='left')
			self.button[i].place(i%6*0.15,0)
	
	def askOne(self,card,inThrow,no,
		title='',tip='选一张放逐:'):
		self.top.title(title)
		n=len(no)
		tip+=f'。共{n}张,其中前{inThrow}张来自弃牌堆'
		self.tip.set(tip)
		self.card=card
		#self.top.geometry("%dx%d+%d+%d" %(300,n*70,600,400))
		for i in range(n):
			self.button[i].changeImageWithCard(card[i])
		self.place(n)
		self.top.deiconify()
		self.center.select(0)#
		self.var.set(-1)
		while(True):
			sleep(0.05)
			self.top.update()
			ask=self.var.get()
			if(ask!=-1):
				self.top.withdraw()
				self.place_forget(n)
				# if(ask==-2):
				# 	print('cancel!')
				# print('choose %d' %(ask))
				return ask

	def askOne2(self,card,title='',tip='选择一张:'):
		self.top.title(title)
		n=len(card)
		if n>48:n=48
		if tip!='':tip+='.'
		tip+=f'共{n}张'
		self.tip.set(tip)
		self.card=card
		#self.top.geometry("%dx%d+%d+%d" %(300,n*70,600,400))
		for i in range(n):
			# self.text[i].set(card[i].inHand())
			self.button[i].changeImageWithCard(card[i])
		self.place(n)
		self.top.deiconify()
		self.var.set(-1)
		self.center.select(0)#
		while(True):
			sleep(0.05)
			self.top.update()
			ask=self.var.get()
			if(ask!=-1):
				self.top.withdraw()
				self.place_forget(n)
				# if(ask==-2):
				# 	print('Cancel!')
				return ask

	def sort(self,card,title='',tip='请排序，先选择的在下:'):
		oldState=Gui.isSpecial
		Gui.isSpecial=True
		self.tip.set(tip)
		n=len(card)
		self.card=card
		for i in range(n):
			# self.text[i].set(str(i+1)+':'+card[i].inHand())
			self.button[i].changeImageWithCard(card[i])
		self.place(n)
		self.top.deiconify()
		self.var.set(-1)
		order=[]
		while(True):
			sleep(0.05)
			self.top.update()
			ask=self.var.get()
			if(ask>-1):
				order.append(card[ask])
				self.button[ask].place_forget()
				n-=1
				if n==0:
					self.top.withdraw()
					Gui.isSpecial=oldState
					return order
				self.var.set(-1)

class Fbutton(Basic):
	def __init__(self,father):
		a=self.button=[]
		b=self.text=[]
		self.var=IntVar(value=-1)
		self.state,self.over=[],[]
		for i in range(9):
			b.append(StringVar())
			a.append(Radiobutton(father,bg='grey',indicatoron=0,
				font=['黑体',12],fg='lightgreen',
				textvariable=b[i],variable=self.var,value=i,command=self.launch))
			a[i].place(rely=i*0.125,relwidth=0.98,relheight=0.125)
		Basic.__init__(self)
	def launch(self):
		if(Gui.isSpecial):return
		index=self.var.get()
		self.var.set(-1)
		b=self.button[index]
		name=b['text']
		if(b['bg']=='grey'):
			Gui.newMessage('Can not be launched !')
			return
		if Player.cp.launch(index):
			Gui.newMessage('发动被撤销。')
		else:
			if b['text']==name:
				b['bg']='grey'

	def launchOne(self,no):
		if no<9:
			self.var.set(no)
			self.launch()
		else:
			if no not in self.over:
				Player.cp.launch(no)
				self.over.append(no)
			else:
				Gui.newMessage('已经发动过了！')

	def launchAll(self,event):
		n=0
		for i in self.button:
			if i['bg']!='grey':
				self.var.set(n)
				self.launch()
			n+=1
	def show(self,cards):
		self.card=cards
		self.over=[]
		n=len(cards)
		if(n>8):n=8
		for i in range(n):
			self.text[i].set(self.showText(i))
		for i in range(n,9):
			self.text[i].set('')
			self.button[i].config(bg='grey')
	def showText(self,i):
		if self.card[i].canBeClick():
			self.button[i].config(bg='darkcyan')
		else:self.button[i].config(bg='grey')
		return self.card[i].name
	def hadLaunch(self,no):
		b=self.button[no]
		b['bg']='grey'
	def lost(self,no):
		l=len(self.card)
		b=self.button
		if(no>8) :return
		if(no!=l):#not the last one
			for i in range(no,l):
				self.text[i].set(self.card[i].name)
				nextbg=b[i+1]['bg']
				b[i].config(bg=nextbg)
		self.text[l].set('')	
		b[l].config(bg='grey')

	def record(self):
		self.state=[]
		for i in self.button:
			if i['bg']!='darkcyan':self.state.append(False)
			else:self.state.append(True)
	def reset(self,card):
		self.card=card
		n=len(card)
		if(n>8):n=8
		for i in range(n):
			if self.state[i]:self.button[i].config(bg='darkcyan')
			else:self.button[i].config(bg='grey')
			self.text[i].set(card[i].name)
		for i in range(n,9):
			self.text[i].set('')
			self.button[i].config(bg='grey')

class Mbutton(Basic):
	def __init__(self,father):
		a=self.button=[]
		b=self.text=[]
		self.var=IntVar(value=-1)
		for i in range(9):
			b.append(StringVar())
			a.append(Radiobutton(father,bg='grey',indicatoron=0,
				font=['黑体',12],fg='lightgreen',
				textvariable=b[i],variable=self.var,value=i,command=self.catch))
			a[i].place(rely=i*0.125,relwidth=0.98,relheight=0.125)
		Basic.__init__(self)

	def catch(self):
		if(Gui.isSpecial):return
		index=self.var.get()
		self.var.set(-1)
		if(Player.cp.catch(index)):self.lost(index)
	def lost(self,no):
		#note:pop firstly
		l=len(self.card)
		if(no!=l):
			for i in range(no,l):
				self.text[i].set(self.showText(i))
		self.text[l].set('')			

class Tip():
	def __init__(self,father,isCancel):
		self.var=isCancel#IntVar(value=0)
		f=self.frame=[ Frame(father) for i in range(2)]
		f[0].place(relx=0.1,relwidth=0.9,relheight=0.5)
		f[1].place(relx=0.1,rely=0.5,relwidth=0.9,relheight=0.5)
		names=['赛钱箱1','神子','洋馆','白莲','紫苑',
		#		  0	   1	  2	 3	  4 
		'女苑','御柱','阿哞','神奈子',
		# 5	   6	 7	 8
		'纳兹琳','赛钱箱2','芳香','蕾米','','走廊']
		#9		10		 11   12   13   14
		self.label=[Label(f[0],bg='paleturquoise',text=names[i]
			) for i in range(15)]
		self.showing=[]
		self.image=Label(father,bg='grey')
		self.image.place(relheight=1,relwidth=0.1)
		self.button=Button(f[1],text='结束',bg='grey',command=self.end)
		self.button.place(relx=0.9,relheight=1,relwidth=0.1)
		self.cancel=Button(f[1],text='取消',bg='grey',command=self.cancel)
		self.cancel.place(relx=0.8,relheight=1,relwidth=0.1)
		self.text=StringVar()
		self.tip=Label(f[1],textvariable=self.text,bg='lightgrey',font=['黑体',12])
		self.tip.place(relheight=1,relwidth=0.8)
	def end(self):
		Player.end()
	#def endEvent(self,)
	def setTip(self,text):
		self.text.set(text)
		self.tip.update()
	def cancel(self):
		self.var.set(True)

	def append(self,i):
		self.label[i].pack(fill=X,side='left')
		self.showing.append(i)
		if i==0:
			self.label[10].pack(side='left')
			self.showing.append(10)
	def lost(self,i):
		self.label[i].pack_forget()
		self.showing.remove(i)
		# if i==0:
		# 	self.label[10].pack_forget()
		# 	self.showing.remove(10)
	def flash(self,image,show=True):
		if show:
			for i in self.showing:
				self.label[i].pack_forget()
			n=0
			self.showing=[]
			for i in Player.buff:
				if i:
					self.label[n].pack(side='left',padx=2)
					self.showing.append(n)
				n+=1
		changeImageWithPhoto(self.image,image)

class SmallTop():
	char=['★','◎','♨']
	def __init__(self,father):
		a=self.top=Toplevel(father,bg='grey')
		a.protocol('WM_DELETE_WINDOW',self.canNotDelete)
		#a.geometry("%dx%d+%d+%d" %(60,100,w/2.5,h/2.5))
		a.withdraw()
		self.tip=StringVar()
		self.tipLabel = Label(
			a, bg='lightgrey', textvariable=self.tip, wraplength=300)  # font=['黑体',20],
		self.tipLabel.pack()
		t=self.text=[]
		b=self.button=[]
		self.var=IntVar(value=-1)
		self.cancel=Radiobutton(a,text='Cancel',
			variable=self.var,value=-2,indicatoron=0,)
		for i in range(10):
			t.append(StringVar())#justify='center',#command=self.toGain
			b.append(Radiobutton(a,textvariable=t[i],font=['黑体',16],
				bg='lightgrey',indicatoron=0,variable=self.var,
				value=i,compound='bottom')) 
	
	def cancelFun(self):self.var.set(-2)

	def pack_forget(self,n):
		for i in range(n):self.button[i].pack_forget()
		self.cancel.pack_forget()
	def askANumber(self,n=2,title='',tip=''):
		self.top.title(title)
		self.tip.set(tip)
		if n>6:n=6
		n += 1
		self.top.geometry("%dx%d+%d+%d" % (300, n*50, 600, 400))
		for i in range(n):
			self.text[i].set(i)
			self.button[i].pack(fill=X,ipadx=40)
		self.cancel.pack()
		self.top.deiconify()
		self.var.set(-1)
		while(True):
			sleep(0.2)
			self.top.update()
			ask=self.var.get()
			if(ask!=-1):
				self.pack_forget(n)
				self.top.withdraw()
				# if(ask==-2):
				# print('Be canceled!')
				return ask
				
	def askAType(self,moreThan3=[0,1,2],title='',tip='选择要消耗的资源:'):
		self.tip.set(tip)
		self.top.title(title)
		n=len(moreThan3)
		self.top.geometry("%dx%d+%d+%d" %(300,n*50,600,400))
		for i in moreThan3:
			self.text[i].set(SmallTop.char[i])
			self.button[i].pack(fill=X,ipadx=40)
		self.cancel.pack()
		self.top.deiconify()
		self.var.set(-1)
		while(True):
			sleep(0.2)
			self.top.update()
			ask=self.var.get()
			if(ask!=-1):
				self.pack_forget(3)
				self.top.withdraw()
				# if(ask==-2):
				# 	print('cancel!')
				return ask
				
	def canNotDelete(self):
		oldText=self.tip.get()
		self.tip.set('Please do not delete!')
		self.top.update()
		sleep(0.5)
		self.tip.set(oldText)

class HomePage():
	#canvas,home,title,button,choose
	def __init__(self,r):
		self.canvas=Label(r,bg='grey')
		changeImageWithName(self.canvas,'homepage')
		root=self.home=Label(self.canvas,bg='palegoldenrod')
		# root.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.42)
		self.title=Label(self.canvas,text='微型\n幻想乡',font='粗体 40 bold')
		self.button=[]
		text=['新游戏','快速开始','退出']
		fun=[self.newGame,self.quickGame,r.quit]#self.loadGame,
		for i in range(3):
			self.button.append(Button(
				root,font='粗体 14 bold',text=text[i],command=fun[i]))
			self.button[i].place(rely=i*0.33,relwidth=1,relheight=0.32)
		self.title.place(relx=0.4,rely=0.1,relheight=0.2,relwidth=0.2)
		self.choose=Choose(self.canvas,self)
		# self.place()
	
	def newGame(self):
		n=simpledialog.askinteger('','How many players?')
		if not n:return
		if n>9:n=9
		self.home.place_forget()
		# self.chooseFrame.place(relx=0.2,rely=0.41,relheight=0.58,relwidth=0.5)
		self.choose.place(n)

	def place(self):
		self.canvas.place(relheight=1,relwidth=1)
		self.home.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.3)
	
	def place_forget(self):
		self.canvas.place_forget()

	def quickGame(self):
		self.place_forget()
		Gui.gaming()
	def startGame(self,name,photo,res):
		# print('start')
		self.canvas.place_forget()
		Gui.gaming(name,photo,res)
		# res=['faith','money','rice']
		# for i in range(n):
		# 	t=typeVar[i].get()
		# 	print(f'Player {i+1} has no {res[t]}.')
	
	def changeAva(self):
		print('avatar')
	
	def loadGame(self):
		print('loadGame')

class Gui():

	"""docstring for Gui"""
	root =Tk()
	Card.createImage()
	Card.readData()
	haveInit=False
	isSpecial=False
	placeText=['中央牌堆','设施区','手牌']
	#frameList=[Frame(cls.root) for i in range(6)]

	def canNotDelete():
		if messagebox.askyesno('关闭游戏？','是否要关闭游戏？'):
			Gui.root.quit()
	
	def init():
		if (Gui.haveInit):return
		r1=Gui.root
		r1.protocol('WM_DELETE_WINDOW',Gui.canNotDelete)
		# r1.attributes("-alpha", 0.9)
		r1.title('微型幻想乡')#Micro Gensokyo
		w,h=1280,800
		#w = r.winfo_screenwidth()
		#h = r.winfo_screenheight()-100
		r1.geometry("%dx%d+0+0" %(w,h))
		r1.attributes("-topmost",False)
		r=Gui.gaimingPage=Frame(Gui.root,bg='grey')
		# r.place(relheight=1,relwidth=1)
		Gui.frameList=[Frame(r,bg='grey') for i in range(8)]
		#	  文本,资源,妖怪,设施, 中央， 其他，提示，手牌
		x=	 [0  ,0   ,0   ,0.1 ,0.2  ,0.8  ,0.2  ,0.2]
		y=	 [0  ,0.4 ,0.55,0.55,0	,0	,0.625,0.725]
		height=[0.4,0.15,0.45,0.45,0.625,0.725,0.1  ,0.275]
		width =[0.2,0.2 ,0.1 ,0.1 ,0.6  ,0.2  ,0.6  ,0.8]
		
		background=['grey','grey','grey','grey',"grey",
			'lightgrey',"grey","grey"]
		for i in range(8):
			a=Gui.frameList[i]
			a['bg']=background[i]
			a.place(relx=x[i],rely=y[i],
				relwidth=width[i],relheight=height[i])

		f=Gui.frameList
		Gui.explaintion=StringVar()
		Gui.isCancel=BooleanVar()
		Message(Gui.frameList[0],textvariable=Gui.explaintion,relief='sunken',
			bg='grey',anchor='nw',justify='left',fg='lawngreen',font=['黑体',12]
			).place(relwidth=1,relheight=1)#wraplength='400', 
		Gui.resource=Resource(f[1])
		Gui.other=Other(f[5])
		Gui.monster =Mbutton(f[2])
		Gui.facility=Fbutton(f[3])
		Gui.center  =Center(f[4])
		Gui.tip=Tip(f[6],Gui.isCancel)
		Gui.hand=Hand(f[7])
		Gui.smallTop=SmallTop(r)
		Gui.top=Top(r)
		Gui.homepage=HomePage(Gui.root)
		#0 cen,1 fac,2 hand
		Gui.var=[Gui.center.var,Gui.facility.var,
			Gui.hand.var]#Gui.monster.var,
		Gui.haveInit=True
		Player.bind()
		#Gui.avatar=Avatar(Gui.frameList[3])
		#Gui.root.bind('<KeyPress-1>',Player.useAll)
	def gaming(name=None,photo=None,res=None):
		Gui.center.newGame()
		Gui.gaimingPage.place(relheight=1,relwidth=1)
		Player.init(name,photo,res)

	def returnHome(event):
		if messagebox.askyesno('!','是否返回主界面'):
			Gui.center.remain=8
			Player.clear()
			Gui.gaimingPage.place_forget()
			Gui.homepage.place()
	def showHome():
		Gui.homepage.place()
	
	def askVar(no,tip=None):
		#no:center facility hand
		# oldState=Gui.isSpecial
		Gui.isSpecial=True
		Gui.var[no].set(-1)
		ask=-1
		if tip==None:
			Gui.setTip(f'请选择{Gui.placeText[no]}一张牌：')
		else:
			Gui.setTip(tip)
		Gui.isCancel.set(False)
		while True:
			sleep(0.05)
			Gui.root.update()
			if Gui.isCancel.get():
				ask=-2
				break
			ask=Gui.var[no].get()
			if(ask!=-1):
				Gui.var[no].set(-1)
				break
		Gui.isSpecial=False
		Gui.setTip('')
		return ask
	
	def nextCenter(no):
		Gui.center.next(no)
	def getCover(no):
		return Gui.center.cover[no]						
	def setTip(text):
		Gui.tip.text.set(text)
		Gui.root.update()
	def explain(text,*card):
		Gui.explaintion.set(text)
	def askAType(moreThan3=[0,1,2],title='',tip='选择资源种类'):
		Gui.isSpecial=True
		a=Gui.smallTop.askAType(moreThan3,title,tip)
		Gui.isSpecial=False
		return a
	def showResource(res):
		Gui.resource.show(res)

	def showexResource():
		Gui.resource.showex()

	def flash(p,reset=True):
		Gui.monster.show(p.monster)
		if reset:
			Gui.facility.show(p.facility)
			Gui.other.next()
		else:
			Gui.facility.reset(p.facility)
			# Gui.tip.flash(p.image,False)
		p.neatHand()
		Gui.hand.show(p.hand)
		Gui.tip.flash(p.image)
	def handAppend():
		Gui.hand.append()
	def handLost(n):
		Gui.hand.lost(n)
	def facilityAppend():
		Gui.facility.append()
	def facilityLost(n):
		Gui.facility.lost(n)
	def monsterAppend():
		Gui.monster.append()
	def monsterLost(no):
		Gui.monster.lost(no)
	def isGameOver(n):
		return Gui.center.isOver(n)
	def end(event):
		if not Player.haveInit:return 
		Player.end()
	def askOne(card,inThrow,no,title='',tip='选一张放逐'):
		oldState=Gui.isSpecial
		Gui.isSpecial=True
		r=Gui.top.askOne(card,inThrow,no,title,tip)
		Gui.isSpecial=oldState
		return r
	def askOne2(card,title='',tip=''):
		oldState=Gui.isSpecial
		Gui.isSpecial=True
		r=Gui.top.askOne2(card,title,tip)
		Gui.isSpecial=oldState
		return r
		
	def newMessage(*text):
		t='\n'
		for i in text:
			t+=str(i)
		Gui.other.newMessage(t)
	def checkMiracle():
		Gui.center.checkMiracle()

	def newPlayer(name,without):
		Gui.other.newPlayer(name,without)
	def askEmpty():return Gui.center.askEmpty()
	def record():Gui.facility.record()

	# def shuffleAndShow(cards):
	# 	name,num,no=[],[],0
	# 	for i in cards:
	# 		j=findIndex(name,i.name)
	# 		if  j!=None:
	# 			num[j]+=1
	# 		else:
	# 			name.append(i.name)
	# 			num.append(1)

	# 	text=''
	# 	for i in range(len(num)):
	# 		text+=f'{num[i]}x{name[i]}\n'
	# 	text=text[:-1]
	# 	Gui.newMessage(self.name,'的卡组:\n',text)

	def showShuffle(n):
		Gui.other.showShuffle(n)

	def changeColor(e):
		color=simpledialog.askstring(title='',prompt='')
		Gui.frameList[4]['bg']=color
	def launchOne(no):
		Gui.facility.launchOne(no)

	def beNormal(event):
		Gui.isSpecial=False

	def changeAlpha(event):
		no=simpledialog.askinteger('','请输入透明度（百分比%）')
		Gui.root.attributes("-alpha", no/100)		

from player import Player

if __name__ == "__main__":
	r1=Tk()
	# r1.protocol('WM_DELETE_WINDOW',canNotDelete)
	r1.attributes("-alpha", 0.95)
	r1.title('微型幻想乡')#Micro Gensokyo
	w,h=1280,800
	#w = r.winfo_screenwidth()
	#h = r.winfo_screenheight()-100
	r1.geometry("%dx%d+0+0" %(w,h))
	r1.attributes("-topmost",True)
	# r=Gui.gaimingPage=Frame(root,bg='grey')
	HomePage(r1).place()
	r1.mainloop()

