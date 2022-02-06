from time import time
timeCount=time() 
from GUI import Gui
# from player import Player
# from skill import Skill
# def __main__:	

Gui.init()
print(time()-timeCount)
Gui.root.mainloop()
# fun=[evilSpirit,mouse,karma,gungnier]
#恶鬼，贪吃老鼠，业障化身，西行妖
#-----------快捷键----------
# Gui.root.bind('<KeyPress-1>',Player.useAll)

#快捷键：一次性使用所有手牌，前期随便用，中期开始就要考虑牌序了
#Gui.root.bind('<Control-l>',Gui.facility.launchAll)
#
# Gui.root.bind('<KeyPress-2>',Gui.end)

#快捷键：回合结束，按界面的end按钮比较好
#快捷键：回到主界面，可以重开游戏
#---------快捷键
# Gui.root.bind('<KeyPress-3>',doFun)
# Gui.root.bind('<KeyPress-4>',doFun)
# Gui.root.bind('<KeyPress-5>',doFun)
# Gui.root.bind('<KeyPress-6>',Gui.changeColor)

# Gui.root.bind('<space>',Player.useAll)
# Gui.root.bind('<Control-e>',Gui.end)
# Gui.root.bind('<Control-r>',Gui.returnHome)
# Gui.root.bind('<Control-s>',Skill.spellAny)
# Gui.root.bind('<Control-f>',Player.launchOne)
# Gui.root.bind('<Control-q>',beNormal)


# def test(event):
# 	Playere(empty=[2,3,4,10])
# def doFun(event):
# 	i=int(event.char)-3
# 	fun[i]()
# def theWorld(e):
# 	Skill.end.append(1)

# def f(cost):
# 	res=Player.resource
# 	b=Player.buff
# 	result=[res[i]-cost[i] for i in range(3)]
# 	source=[None]*3
# 	if b[3]:source[1],source[2]=0,0
# 	if b[4]:source[0]=1
# 	if b[5]:source[1]=0
# 	for i in range(3):
# 		if result[i]<0:#
# 			if source[i]==None:return False
# 			else:#
# 				s=source[i]
# 				result[s]+=result[i]
# 				if result[s]<0:return False
# 				else:
# 					result[i]=0
# 	for i in range(3):
# 		res[i]=cost[i]+result[i]
