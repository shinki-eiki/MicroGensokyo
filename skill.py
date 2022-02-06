from GUI import Gui
from time import time,sleep
from random import shuffle,randint
from tkinter import simpledialog
from tkinter import messagebox
#exile，放逐，res，resour的缩写，char，character的缩写

def resourceChange(a,b,lost=-3,gain=2):
	if(Player.resource[a]<-lost):
		Gui.newMessage('资源不足!')
		return 1
	gainResource(a,lost)
	gainResource(b,gain)

def appendBuff():
	name=Skill.card.name
	Player.appendBuff(name)

def gainChangeabledRes(t=[0,1,2],n=1):
	theType=Gui.askAType(t,f'请选择想要获得的资源种类,数量为{n}')
	if(theType==-2):return 1
	gainResource(theType,n)

def lostHand():
	if Player.cp.handNumber()==0:return 0
	while True:
		no=Gui.askVar(2,'可以弃一张牌，然后获得资源：')
		if(no==-2):return 0
		else:
			card=Player.cp.hand[no]
			if card.name!=Skill.card.name:
				Player.cp.lost(no)
				break

def copyEffect(card,coper):
	Gui.newMessage(f'复制了{card.name}的效果')
	Player.cp.gainResourse(card)
	Skill.spell0(card)
	# if 3 in card.skill:
	# 	c=coper
	# 	s=c.skill
	# 	s[0]+=card.skill[0]
	# 	s.append(3)
	# 	c.gain=card.gain
	# 	return 0
	
def copyChar(faith=False):
	card=[]
	coper=Skill.card
	findUsedChar(card,faith)
	if(card==[]):
		Gui.newMessage('没有卡可以复制!')
		return
	r=Gui.askOne2(card,Skill.card.name,
		'选择一张复制其效果：')
	if(r==-2):return 1
	else:
		return copyEffect(card[r],coper)
		# Player.cp.gainResourse(card[r])
		# Skill.spell0(card[r])
		# if 3 in card[r].skill:
		# 	c=coper
		# 	s=c.skill
		# 	s[0]+=card[r].skill[0]
		# 	s.append(3)
		# 	c.gain=card[r].gain
		# 	return 0
def findUsedChar(card,faith):
	for i in Player.used:
		if(i.category()==0):
			if(faith and not i.isFaith()):continue
			card.append(i)

def selfDestory():
	p=Player.cp
	name=Skill.card.name
	return p.selfDestory(name)

def gainCenter(cost=15,category=[0,1,2]):
	while True:
		t='选择中央牌堆一张'
		typeList=['角色','设施','妖怪']
		for i in category:
			t+=typeList[i]+'/'
		t+=f'（费用不高于{cost}）'
		no=Gui.askVar(0,t)
		if no==-2:return 1
		card=Gui.getCover(no)
		if card.category() in category and card.totalCost()<=cost:
			p=Player.cp
			p.obtain(card,no)
			return
		else:
			Gui.setTip('不满足条件！')
			#Gui.root.update()
			sleep(2)

def gainResource(t,n=1):
	if(n==0):return
	r=Player.resource
	r[t]+=n
	Gui.resource.var[t].set(r[t])		
	
def tongNian():
	if(not Player.faithCard):return 0#通念
def qiaoShou():
	if(len(Player.cp.facility)<2):return 0		#巧手

def draw2():Player.drawP(2)
def draw3():Player.drawP(3)

def exileHand():
	p=Player.cp
	while True:
		no=Gui.askVar(2,'可以放逐一张手牌')
		if(no==-2):#不放逐
			# print('cancel.')
			return 0
		else:
			card=p.hand[no]
			if card.name!=Skill.card.name:
				p.hand[no]=None
				Gui.handLost(no)
				Player.exileAdd(card)
				return
def justExileCenter(category=[0,1,2]):
	while True:
		Gui.setTip('可以放逐中央牌堆顶一张牌.')
		no=Gui.askVar(0)
		if no>8:
			Gui.newMessage('除了人间之里！')
			continue
		elif(no==-2):return 0
		else:
			card=Gui.getCover(no)
			if(card!=None and card.category() in category and card.name!='毛玉王'):
				Gui.center.next(no)
				Player.exileAdd(card)
				return
def exileCenter():
	while True:
		Gui.setTip('可以放逐中央牌堆顶一张牌.')
		no=Gui.askVar(0)
		if no>8:
			Gui.setTip('除了人间之里！')
			sleep(2)
			continue
		elif (no==-2):return None
		else:
			card=Gui.getCover(no)
			if card.name!='毛玉王':
				Player.exileAdd(card)
				Gui.center.next(no)
				return card
#---------------|basic function|-----------------------
class Skill():
	card=None
	no=[]
	end=[]#karma,sakuya
	cardTemp=[]
	def checkEnd():
		if Skill.end==[]:return 
		if 0 in Skill.end:#karma
			where=[]
			total=len(Skill.no)
			p=Player.cp
			allCard=[p.throw,p.deck,p.hand,p.facility,p.repeat]
			w=0
			no,c=Skill.no,Skill.cardTemp
			player=Player.player
			#
			for i in allCard:#找牌，删牌,i是牌堆位置
				o=0
				for card in i:
					if card==None:continue
					name=card.name
					if name in c:
						# print(o,':',name)
						index=c.index(name)
						#return
						who=no.pop(index)
						c.pop(index)
						player[who].throw.append(card)
						i[o]=None
						Gui.newMessage(name,'已返还.')
						where.append(w)
						total-=1
						if total==0:break
					o+=1
				if total==0:break
				w+=1
			for i in where:
				allCard[i].remove(None)
			
		if 1 in Skill.end:#sakuya
			Player.now-=1
			Gui.newMessage('The World!')
		Skill.end=[]

	def spellAny(event):
		no=simpledialog.askinteger('','请输入技能序号：')
		if no==None or no>53:return
		Skill.function[no]()
	def init():
		Skill.function=(getFaith,#0一点信仰
			getMoney,#1一点钱币
			getRice,#2一点粮食
			Player.drawP#3抓一张牌
			,draw2			#4抓2张牌
			,draw3			#5抓3张牌
			,Player.exileOneP#6放逐手牌或弃牌堆一张
			,tongNian				#7通念判断
			,qiaoShou			#8巧手判断
			,appendBuff	#9,增加buff，对于角色，在【】内+9，对于设施，在【】外+1
			,selfDestory			#10摧毁自己
			,sanae			#11早苗
			,suwako		#12诹访子
			,hugeSnake			#13巨蛇
			,minamitsu		#14船长
			,syou			#15寅丸星
			,xiangzi			#16幽谷响子
			,ichirin			#17一轮
			,detector			#18金属探测器
			,reel			#19魔界卷轴
			,karma			#20业障化身
			,futo	#21物部布都
			,zombieSymbol			#22僵尸符
			,reimu			#23灵梦
			,kasen			#24华扇
			,flagon			#25萃香的酒壶
			,reisen			#26铃仙
			,kaguya			#27辉夜
			,gainChangeabledRes			#28玉枝
			,roukangen			#29楼观剑
			,foldingFan			#30折扇
			,lostHand			#31弃一张手牌
			,exileHand			#32放逐一张手牌
			,stray			#33迷途之灵
			,saigyouyou			#34西行妖
			,alice			#35爱丽丝
			,marisa			#36魔理沙
			,eightTrigrams			#37八卦炉
			,evilSpirit			#38恶鬼
			,fireSpectre			#39染火的怨灵
			,satori			#40觉
			,koishi			#41恋
			,rin			#42燐
			,utsuho			#43空
			,nuclearFurnace			#44核熔炉
			,flandre			#45芙兰
			,pachouli			#46帕琪
			,sakuya			#47咲夜
			,koakuma			#48小恶魔
			,gungnier		#49冈格尼尔
			,mouse#50贪吃老鼠
			,gainCenter #51毛玉王
			,library#52图书馆
			,Skill.fadeAway#53消逝
		)

	def fadeAway():
		Player.exileAdd(Skill.card)
		Skill.card=None
	# def check(skill,timing):
	# 	pass
	def spell1(card):#退治妖怪，设施buff
		Skill.card=card
		skill=card.skill
		if len(skill)<2:return
		try:
			for s in skill[1]:#发动一个效果
				result=Skill.function[s]()
				if(result!=None):return result
		except  Exception as inst:
			# print(type(inst))	# the exception instance
			# print(inst.args)	 # arguments stored in .args
			Gui.newMessage(inst)		  # __str__ allows args to be printed directly,
			# Gui.newMessage("Unexpected error.")
			return None

	def spell0(card):#打出角色，发动设施，捕获妖怪
		Skill.card=card
		skill=card.skill
		if len(skill)==0:return
		try:
			for s in skill[0]:#发动一个效果
				result=Skill.function[s]()
				if(result!=None):return result
		except  Exception as inst:
			Gui.newMessage(inst)		  # __str__ allows args to be printed directly,
			return None
		

	def checkMiracle(name):
		if   name=='云居一轮&云山':miracleShuffle()
		elif name=='激光宝塔':miracleRebuild()		
		elif name=='物部布都':miracleExile()
		elif name=='因幡帝':miracleDraw()
		elif name=='西行妖':saigyouyou()
		elif name=='神奈子的御柱':miracleMissionary()

	def checkRetreat(cost):
		if not Player.timing[2]:return
		b=Player.buff
		if b[10] and Player.cp.haveFacility('赛钱箱'):
			Gui.newMessage('赛钱箱生效。')
			getMoney()
			Player.lostBuff(10)
		if b[11]:
			Gui.newMessage('宫古芳香生效。')
			Player.drawP(1)
			Player.lostBuff(11)
		if b[12]:
			Gui.newMessage('蕾米莉亚 斯卡雷特生效。')
			gainCenter(cost,[0,1])

	def checkBeforeGain(card):
		if not Player.timing[0]:return Skill.canGain(card.cost)
		if Player.buff[2] and card.category()==1 and Player.cp.haveFacility('洋馆'):
			getMoney()
			if Skill.checkBeforeGain2(card.cost):
				Gui.newMessage('洋馆生效。')
				Player.lostBuff(2)
				if card.cost[1]==0:getMoney(-1)
				return True
			else:
				getMoney(-1)
				return False
		else:return Skill.checkBeforeGain2(card.cost)
		
	def checkBeforeGain2(cost):
		res=Player.resource
		b=Player.buff
		result=[res[i]-cost[i] for i in range(3)]
		source=[None]*3
		# print(result)
		if b[3]:source[1],source[2]=0,0
		if b[4]:source[0]=1
		if b[5]:source[1]=0
		if not (b[3] or b[4] or b[5]):return Skill.canGain(cost)
		for i in range(3):
			if result[i]<0:#找到一个资源不足的点
				if source[i]==None:#无来源时
					return False
				else:#检查来源能否补给
					s=source[i]
					result[s]+=result[i]
					if result[s]<0:return False
					else:
						result[i]=0
		for i in range(3):
			res[i]=cost[i]+result[i]
		return True
		
	def canGain(cost):
		r=Player.resource
		for i in range(3):
			if r[i]<cost[i]:return False
		return True

#---------------|machining function|-----------------
def miracleDraw():#抽一
	n,show=Player.now,False
	Gui.newMessage('所有玩家抓一张牌。')
	for i in range(Player.total):
		if i==n:show=True
		else:show=False
		Player.player[i].draw(1,show)
def miracleShuffle():#洗回
	Gui.newMessage('所有玩家将弃牌堆洗回卡组。')
	for i in Player.player:
		i.deck+=i.throw
		shuffle(i.deck)
		i.throw=[]
def miracleExile():#放逐，
	Gui.newMessage('所有玩家可以放逐一张牌。')
	Player.cp.exileOne()
	Gui.record()
	now=Player.now
	player=Player.player
	for cur in range(Player.total):
		if cur==now:continue
		Gui.flash(player[cur])
		player[cur].exileOne()
	Gui.flash(Player.cp,False)
def miracleRebuild():#重建
	Gui.newMessage('所有玩家可以将一张弃牌堆中的设施牌加入手卡。')
	Player.cp.rebuild()
	now=Player.now
	Gui.record()
	player=Player.player
	for cur in range(Player.total):
		if cur==now:continue
		card,no,n=[],[],-1
		for i in player[cur].throw:
			n+=1
			if(i.category()==1):
				card.append(i)
				no.append(n)
		if(no==[]):
			Gui.newMessage(
				f'{player[cur].name}弃牌堆中没有设施牌!')
			cur+=1
			continue
		elif len(no)==1:
			r=0
		else:
			Gui.flash(player[cur])
			r=Gui.askOne2(card)
			if(r==-2):
				cur+=1
				continue
		#上手
		player[cur].hand.append(card[r])
		player[cur].throw.pop(no[r])
		Gui.newMessage(f'{player[cur].name}将{card[r].name}加入手卡.')
	Gui.flash(Player.cp,False)
def miracleMissionary():#传教
	Gui.newMessage('所有玩家可以从中央牌堆将一张教徒放置在牌堆顶。')
	now,total=Player.now,Player.total
	card=Gui.getCover(9)
	player=Player.player
	put=messagebox.askyesno('神奈子的御柱'
			,'是否将一张 教徒 放置在你的牌堆顶？')
	if put:
		Gui.newMessage(player[now].name+" 选择获得一张教徒")
		player[now].deck.append(card)
	Gui.record()
	for cur in range(total):
		if cur==now:continue
		Gui.flash(player[cur])
		put=messagebox.askyesno('神奈子的御柱'
			,'是否将一张 信徒 放置在你的牌堆顶？')
		if put:
			Gui.newMessage(player[cur].name+" 选择获得一张教徒")
			player[cur].deck.append(card)
	Gui.flash(Player.cp,False)

def evilSpirit():
	ask=messagebox.askyesno('恶鬼','是否放弃摧毁设施，改为获得3点钱币？')
	if ask:
		getMoney(3)
		return
	Gui.record()
	now,total=Player.now,Player.total
	player=Player.player
	r=-2
	for cur in range(total):
		if cur==now:continue
		l=len(player[cur].facility)
		if(l==0):
			Gui.newMessage(
				f'{player[cur].name}的设施区没有设施!')
		elif l==1:
			player[cur].destory(0,False)
		else:
			Gui.flash(player[cur])
			while True:
				r=Gui.askVar(1,'选择设施区内一张设施保留,然后摧毁其他设施：')
				if (r!=-2):break
			f=player[cur].facility
			remain=f.pop(r)
			player[cur].throw+=f
			f=[]
			f.append(remain)
			player[cur].facility=f
			Gui.newMessage(f'{player[cur].name}保留了{remain.name}')
			# for i in len(f):
			# 	player[cur].destory(0,False)
	Gui.flash(Player.cp,False)
def mouse():
	now,total=Player.now,Player.total
	player=Player.player
	Gui.record()
	for cur in range(total):
		if cur==now:continue
		l=len(player[cur].facility)
		if l==0:
			Gui.newMessage(
				f'{player[cur].name}的设施区没有设施!')
			continue
		elif l==1:
			r=0
		else:
			Gui.flash(player[cur])
			while True:
				r=Gui.askVar(1,'选择设施区内一张设施摧毁：')
				if(r!=-2):break
		# f=player[cur].facility.pop(r)
		# Gui.facilityLost(r)
		player[cur].destory(r,False)
		# Gui.newMessage(f' 摧毁了{player[cur].name}的{f.name}.')
	Gui.flash(Player.cp,False)
def flagon():return resourceChange(2,1)#萃香的酒壶
def kasen() :return gainChangeabledRes([0,1],3)#茨木华扇
def reimu() :return gainCenter(20,[2])

def zombieSymbol():#僵尸符
	return resourceChange(2,0)
def futo():#物部布都
	p=Player.cp
	first=False
	while True:
		no=Gui.askVar(2,'弃两张牌或者一张信仰牌')
		if(no==-2):continue
		p.lost(no)
		card=p.throw[-1]
		# if card.name==Skill.card.name:continue
		if(card.isFaith() or first):
			return
		else:first=True
def reel():#魔界卷轴
	if(Player.faithCard>1):
		return Player.cp.rebuild()
	else:
		Gui.newMessage('条件不满足!')
		return 1
def detector():#金属探测器
	p=Player.cp
	if p.checkDeck():return 1
	else:
		card=p.deck[-1]
		Gui.explain(str(card))
		if(card.category()==1):
			gain=messagebox.askyesno(
				'金属探测器',f'获得{card.name}?')
			if(gain):p.draw(1)
		else:#not facility
			throw=messagebox.askyesno(
				'金属探测器',f'丢弃{card.name}?')
			if(throw):
				p.throw.append(p.deck.pop())
				Gui.newMessage(f'{p.name}丢弃了{card.name}')
def minamitsu():#村纱
	p=Player.cp
	f=p.facility
	l,n=len(f),0
	if l==0:return
	while True:
		no=Gui.askVar(1,'摧毁任意张设施，摸等量的牌（按 取消 键结束选择：')
		if no ==-2:break
		elif no<l:
			p.destory(no)
			n+=1
			l-=1
			if l==0:break
	if n!=0:
		p.draw(n)
	else:return 

def xiangzi():#响子
	return copyChar(True)
def ichirin():#一轮
	card=exileCenter()
	if card==1:return 1
	if card.category()==1:
		getFaith(3)
def kaguya():
	p=Player.cp
	if len(p.deck)<5:
		shuffle(p.throw)
		p.deck+=p.throw
		p.throw=[]
	n=len(p.deck)
	if n>5:n=5
	card=p.deck[-n:]
	card=Gui.top.sort(card,'蓬莱山辉夜',
		'先选择一张加入手牌或放逐，其余排序后放回，先选择的在下：')
	choose=card.pop(0)
	add=messagebox.askyesno('蓬莱山辉夜',
		f'是否将{choose.name}加入手卡？\n若否，则将其放逐。')
	if add:
		Gui.newMessage(f'{choose.name}加入手卡')
		p.hand.append(choose)
		Gui.handAppend()
	else:
		Player.exileAdd(choose)
	p.deck.pop()
	p.deck[1-n:]=card
def karma():#end add 0
	ask=messagebox.askyesno('业障化身','是否放弃获得其他人手牌，改为获得3点任意相同种类资源？')
	if ask:
		t=Gui.askAType([0,1,2],'业障化身')
		gainResource(t,3)
		return
	p=Player.player
	card=None
	h=Player.cp.hand
	for i in range(Player.total):
		if i==Player.now:continue
		p[i].neatHand()
		l=len(p[i].hand)
		if l==0:
			Gui.newMessage(f'{p[i].name}没有手牌.')# has no hand
			continue
		else :
			while True:
				no=randint(0,l-1)
				if p[i].hand[no] != None:
					#失去手牌
					card=p[i].hand[no]
					p[i].hand[no]=None
					Gui.newMessage(
						f'获得了{p[i].name}的{card.name}')
					#记录卡片及玩家
					Skill.no.append(i)
					Skill.cardTemp.append(card.name)
					#标记被拿走卡牌
					# card.skill.append(10)
					h.append(card)
					Gui.handAppend()
					break
	if card != None:Skill.end.append(0)

def foldingFan():
	no=0
	while True:
		no=Gui.askVar(0,'选择一个中央牌堆，对其最上面三张排序')
		if no==-2:return 1
		elif no<9:break
	Gui.center.sortThree(no)
	# return
	# c=Gui.center.card
	# card=c[no][-2:]
	# for i in range(2):c.pop()
	# card.append(Gui.center.cover[no])
	# card=Gui.top.sort(card,'幽幽子的折扇')
	# Gui.center.cover[no]=card.pop()
	# c[no]+=card
	# Gui.nextCenter(no)

def saigyouyou():
	Gui.newMessage('无事发生')
	return
def alice():return
def roukangen():#楼观剑
	if Player.cp.haveFacility('白楼剑'):
		getRice()
	else:return 1
def stray():#迷途之灵
	Player.exileOneP()
	justExileCenter()
def library():return gainChangeabledRes([1,2])

def eightTrigrams():
	Player.exileOneP()
	justExileCenter([2])

def fireSpectre():
	n=0
	for i in Player.cp.monster2:
		if(i.name=='染火的怨灵'):n+=1
	getMoney(n)
def satori():
	player=Player.player
	card,who=[],[]
	for i in range(Player.total):
		if not player[i].checkDeck():
			c=player[i].deck[-1]
			Gui.newMessage(f'{player[i].name}的牌堆顶是{c.name}.')
			if c.category()==0:
				card.append(c)
				who.append(i)
	if card==[]:return
	no=Gui.askOne2(card,'satori','选择一张复制其效果：')
	if no ==-2:return
	# Player.cp.gainResourse(card[no])
	# Skill.spell0(card[no])
	copyEffect(card[no],Skill.card)
	throw=messagebox.askyesno('satori','是否将其丢弃？')
	if throw:
		i=who[no]
		Gui.newMessage(f'丢弃了{player[i].name}的{card[no].name}')
		player[i].throw.append(player[i].deck.pop())
def koishi():
	while True:
		no=Gui.askVar(0)#'选择中央牌堆一张牌'
		if no==-2:return 1
		elif no<9:break
	card=Gui.getCover(no)
	if card==None:return 1
	if randint(0,1):
		#Gui.newMessage('放逐了 古明地恋')
		Skill.fadeAway()
		Gui.newMessage(f'获得了{card.name}')
		Player.cp.throw.append(card)
	else:
		Player.exileAdd(card)
		Player.cp.throw.append(Skill.card)
		Skill.card=None
	Gui.nextCenter(no)
def rin():
	p=Player.cp
	n=-1
	card,no,name=[],[],[]
	for i in p.throw:
		n+=1
		if i.category()==0 and i.name not in name:
			card.append(i)
			no.append(n)
			name.append(i.name)
	if(card==[]):return 1
	r=Gui.askOne2(card,'rin','选一张放逐或置于牌堆顶：')
	if r==-2:return 1
	throw=messagebox.askyesno('rin',f'是否将{name[r]}放逐？\n若否，则将其置于牌堆顶。')
	if throw:
		p.throw.pop(no[r])
		Player.exileAdd(card[r])
	else:
		p.deck.append(p.throw.pop(no[r]))
def nuclearFurnace():
	n=len(Player.cp.facility)
	getMoney(n)
def utsuho():
	n=0
	for i in range(2):
		if(exileHand()!=0):n+=1
		else:
			break
	getRice(2*n)

def sakuya():#end add 1
	money=Gui.smallTop.askANumber(3,'sakuya:',
		'请选择你想得到的钱币的数量（最多为3），剩余的将会变为食物：')
	if money==-2:return 1
	getMoney(money)
	getRice(3-money)
	if qiaoShou()==0:return 0
	if messagebox.askyesno('sakuya:',
		'是否放逐此卡，然后在回合结束后在进行一个额外回合'):
		Skill.end.append(1)
		Skill.fadeAway()
	# else:return 0
		# p.hand
def pachouli():
	if qiaoShou()==None:
		t=Gui.askAType([0,1,2],'pachouli','可以将一张人间之里牌加入手卡：')
		if t==-2:return
		card=Gui.getCover(t+9)
		Player.cp.hand.append(card)
		Gui.newMessage(f'{Player.cp.name}将{card.name}加入手卡.')
		Gui.handAppend()
def koakuma():
	t=Gui.askAType([0,1,2],'koakuma','可以获得一张人间之里牌：')
	if t==-2:return
	card=Gui.getCover(t+9)
	Player.cp.obtain(card)
	# Gui.handAppend()throw.append(card)
def gungnier():
	card,name,indexs=[],[],[]
	index=0
	for i in Player.exile:
		if i.category()==2 and i.name not in name:
			card.append(i)
			name.append(i.name)
			indexs.append(index)
		index+=1
	if name==[]:
		Gui.newMessage('放逐区无妖怪!')
		return 1
	no=Gui.askOne2(card)
	if no==-2:return 1
	c=Skill.card
	Player.cp.obtain(card[no])
	Player.exile.pop(indexs[no])
	Skill.card=c

def syou():#tiger
	if len(Player.cp.facility)==0:
		return 0
	no=Gui.askVar(1,'摧毁设施区一张设施，获得2枚钱币')
	if(no==-2):return 0
	return Player.cp.destory(no)

def reisen():return copyChar()

def hugeSnake():
	p=Player.cp
	card=Gui.getCover(9)
	for i in range(2):
		if Player.exileOneP()==-2:
			return 
		p.deck.append(card)

def sanae():
	p=Player.cp
	if(p.checkDeck()):return 1
	name=simpledialog.askstring(title='Sanae'
		,prompt='请输入你宣言的卡名:')
	Gui.newMessage(f'宣言了{name}')
	p.draw()
	card=p.hand[-1]
	Gui.newMessage(f'抽到的卡为{card.name}')
	if(card!=None and card.name==name):
		Gui.newMessage('宣言正确，获得两点信仰。')
		getFaith(2)
	else:Gui.newMessage('宣言错误。')

def suwako():
	while True:
		no=Gui.askVar(0,'请选择中央牌堆一张信仰牌：')
		if no==-2:return 1
		card=Gui.getCover(no)
		if (card.isFaith()  and card.category() in [0,1]):
			p=Player.cp
			if tongNian()==None:
				inTop=messagebox.askyesnocancel(
					'suwako',f'是否将{card.name}放置在你的牌堆顶?')
				if(inTop):
					p.deck.append(card)
					if Player.timing[1]:#
						for i in range(6,9):
							if Player.buff[i]:
								Player.lostBuff(i)
					Gui.nextCenter(no)
					return
				elif(inTop==None):
					return 1
			p.obtain(card,no)
			return
def marisa() :return gainCenter(3,[0,2])
def flandre():return gainCenter(4,[1,2])

def getFaith(n=1):
	gainResource(0,n)
def getMoney(n=1):
	gainResource(1,n)
def getRice(n=1):
	gainResource(2,n)

from player import Player

