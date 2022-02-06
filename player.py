from GUI import Gui
from tkinter import messagebox
from function import findHeadImage
from time import time,sleep
from random import shuffle,randint
from card import *

def findIndex(name,aim):
    for i in range(len(name)):
        if name[i]==aim:return i
    return -1
    
class Player():
    now,total,first=0,0,0
    turnsCount=1
    player=[]
    resource  =[0,0,0]
    exResource=[0,0,0]
    skill,used,exile=[],[],[]
    faithCard,faithChar=0,0
    cardTemp=None
    haveInit=False
    names =['赛钱箱','丰聪耳神子','洋馆','圣白莲','依神紫苑',
        #   0         1          2       3      4 
        '依神女苑','神奈子的御柱','高丽野阿哞','八坂神奈子',
        # 5         6          7             8
        '纳兹琳','赛钱箱','宫古芳香','蕾米莉亚 斯卡雷特',None,'月之走廊']
        #9       10         11        12               13    14
    buff  =[False]*15
    timing=[0]*5
    #       0        1    2      3    4
    #      before gain,retreat, exile,use                 
    #        4    4     3+1      2    1
    def __init__(self,no,name,photo):
        self.deck=[]
        self.throw=[]
        self.hand=[]
        self.repeat=[]
        self.facility=[]
        self.monster=[]
        self.monster2=[]
        self.no=no
        self.name=name
        if photo==None:
            self.image=findHeadImage(no)
        else:self.image=photo
        self.guide=[self.monster2,self.monster,self.facility,self.hand,self.repeat,Player.used,self.deck,self.throw]
        #               0              1            2            #3          4             5         6        7
    @classmethod
    def clear(cls):
        for p in cls.player:
            # del p.image
            for i in range(7):
                 p.guide[i]=[]
        cls.player,cls.exile=[],[]
        cls.haveInit=False


    @classmethod
    def countScore(cls,empty):
        allCard=[]
        card=None
        for p in cls.player:
            cardNum,score,library=0,0,False
            Gui.newMessage(f'-----{p.name}:')
            allCard=[p.monster2,p.monster,p.facility,p.hand,
                p.deck,p.throw,p.repeat]
            for i in p.monster:
                score+=i.score
            for i in p.monster2:
                score+=i.score
            for i in range(2,7):
                cards=allCard[i]
                for j in cards:
                    if j!=None and j.place in empty:
                        score+=j.score
            for i in allCard:
                cardNum+=len(i)
            Gui.newMessage('score',score)
            Gui.newMessage('Number of cards:',cardNum)
    
    def checkMiracle(name):
        Gui.newMessage(f'奇迹:{name}')
        Skill.checkMiracle(name)
    
    @classmethod
    def exileAdd(cls,card):
        Gui.newMessage(f'放逐了{card.name}')
        if cls.timing[3] and cls.buff[14] and card.category()==0 and Player.cp.haveFacility('月之走廊'):
            # cls.timing[3]-=1
            # cls.buff[14]=False
            Player.resource[0]+=1
            Gui.showResource(cls.resource)
            cls.lostBuff(14)
        cls.exile.append(card)
    
    @classmethod
    def appendBuff(cls,name):
        i=Player.names.index(name)
        Player.buff[i]=True
        if i==0:
            Player.buff[10]=True
            Player.timing[2]+=1
        Player.timing[(i-2)//4]+=1
        Gui.tip.append(i)
        Gui.newMessage(f'获得增益：{name}')
    
    @classmethod
    def lostBuff(cls,i):#,cut=True
        Player.buff[i]=False
        Player.timing[(i-2)//4]-=1#if cut:
        Gui.tip.lost(i)
        Gui.newMessage(f'失去增益：{Player.names[i]}')
    
    @classmethod
    def exileOneP(cls):
        return cls.cp.exileOne()
    
    @classmethod
    def init(cls,name,photo,without):
        if without==None:
            n=3
            without=[randint(0,2) for i in range(n)]
            photo=[None]*n
            name=['灵梦','魔理沙','爱丽丝','早苗']#'神绮','摩多罗','幽香',
        else:n=len(name)
        init=['',[[]],10,0]
        rice = Card('仆役',[0,0,0],[0,0,1],*init,2)#★','◎','♨
        money= Card('茶商',[0,0,0],[0,1,0],*init,1)
        faith= Card('信徒',[0,0,0],[1,0,0],*init,0)
        c=[[faith]*5,[money]*5,[rice]*5]
        # for j in range(3):
        #     for i in range(4):
        #         c[j].append(c[j][0])
        for i in range(n):#i代表第几位玩家
            cls.player.append(Player(i,name[i],photo[i]))
            for x in range(3):#x代表第几位资源
                if x!=without[i]:
                    cls.player[i].deck+=c[x]
            shuffle(cls.player[i].deck)
            cls.player[i].draw(5,False)
        cls.haveInit=True
        cls.first=randint(0,n-1)
        cls.total=n
        cls.now=cls.first-1
        Gui.newMessage(f'从{cls.player[cls.first].name}开始.')
        cls.turnsCount=0
        cls.next()
        Gui.other.newPlayer(name,without,cls.first)
        Gui.checkMiracle()

        #cls.cp=cls.player[cls.now]     
    
    def end():
        p=Player.cp
        for i in Player.used:
            if(3 not in i.skill):#迂返
                p.throw.append(i)
            else:p.repeat.append(i)
        for i in p.hand:
            if(i!=None):p.throw.append(i)
        p.hand=[]
        # Player.resource,Player.exResource=[0,0,0],[0,0,0]
        #Player.showThrow()
        p.draw(5,False)
        Skill.checkEnd()
        Player.next()
    
    @classmethod
    def next(cls):
        cls.now+=1
        if(cls.now==cls.total):cls.now=0
        if(cls.now==cls.first):
            cls.turnsCount+=1
            Gui.newMessage(f'----第{cls.turnsCount}轮：')# player 
            if Gui.isGameOver(Player.total):
                Gui.newMessage('游戏结束!')
                empty=Gui.askEmpty()
                Player.countScore(empty)
                return
        cls.used=[]#cls.skill=[]
        cls.buff=[False]*15
        cls.timing=[0]*5
        cls.faithChar=cls.faithCard=0
        cls.cp=cls.player[cls.now]
        p=cls.cp
        Gui.newMessage(f'----{p.name}的回合：')# player 
        p.gainFromFacility()
        p.gainFromMonster()
        #check begin,restraint
        Gui.flash(p)#include hand,facility,monster
        n=-1
        for i in p.hand:
            n+=1
            if i==None:continue
            if 4 in i.skill:#'克制'
                if messagebox.askyesno('克制',f'是否丢弃{i.name}，然后抽一张卡？'):
                    p.lost(n)
                    p.draw(1)
        p.repeatCard()
    
    def gainFromFacility(self):
        Player.resource=[0,0,0]
        for i in self.facility:
            if 1 in i.skill:#check buff
                Player.appendBuff(i.name)
            for j in range(3):#gain
                Player.resource[j]+=i.gain[j]
        Gui.showResource(Player.resource)
    
    def gainFromMonster(self):
        Player.exResource=[0,0,0]
        for i in self.monster:
            r=i.skill[0]
            for j in r:
                if j<3:Player.exResource[j]+=1
        Gui.showexResource()
    
    def launch(self,no):
        card=self.facility[no]
        Gui.newMessage(f'发动了{card.name}')
        return Skill.spell0(card)

    def launchOne(event):
        p=Player.cp
        ask=Gui.askOne2(p.facility,p.name,'选择一张发动:')
        if ask==-2:return
        else: Gui.launchOne(ask)
    @classmethod
    def drawP(cls,n=1):
        cls.cp.draw(n)
  
    
    def useAll(*event):
        if not Player.haveInit:return 
        p=Player.cp
        n=len(p.hand)
        for i in range(n):
            if(p.hand[n-i-1]!=None):p.use(n-i-1)
            #n+=1
    
    def launchAll(*event):
        p=Player.cp
        n=len(p.hand)
        for i in range(n):
            if(p.hand[n-i-1]!=None):p.use(n-i-1)
            
    def checkDeck(self):#if can draw
        if self.deck==[]:
            Gui.newMessage(f'{self.name}洗牌.')
            self.deck,self.throw=self.throw,[]
            if(self.deck==[]):
                Gui.newMessage('已无卡可抽!')
                return True
            shuffle(self.deck)
            Gui.showShuffle(len(self.deck))
        return False
    
    def draw(self,n=1,show=True):#抽卡
        for i in range(n):
            if(self.checkDeck()):
                n-=i
                break
            card=self.deck.pop()
            if card!=None:self.hand.append(card)
            else:
                n-=1
                continue
            if(show):Gui.handAppend()
        Gui.newMessage(f'{self.name}抽了{n}张牌')
    
    def gainResourse(self,card):
        if(card.gain!=[0,0,0]):
            for i in range(3):
                # if card.gain[i]:
                Player.resource[i]+=card.gain[i]
            Gui.showResource(Player.resource)
    
    def canGain(self,card):
        if card.place==10 :return True
        if card.name!='博丽灵梦':
            return Skill.checkBeforeGain(card)
        else:
            return Player.resource[0]+Player.resource[1]>5

    def cost(self,card,no):#利用资源获取卡牌
        if card.place!=10:
            if card.name!='博丽灵梦':
                for i in range(3):
                    Player.resource[i]-=card.cost[i]
            else:
                res=Player.resource
                n=Gui.smallTop.askANumber(res[0],
                    '博丽灵梦','选择要消耗的信仰数量：')
                money=6-n
                if money<=res[1]:
                    res[0]-=n
                    res[1]-=money
        else:#人间之里
            if self.gainPeople(card):return False
        return self.obtain(card,no)
 
    def gainPeople(self,people):
        moreThan3=[]
        for i in range(3):
            if(Player.resource[i]>2):
                moreThan3.append(i)
        length=len(moreThan3)
        if(length==0):return True#true will disturb
        elif(length==1):
            theType=moreThan3[0]
        else:
            theType=Gui.askAType(moreThan3,'获得人间之里升级牌'
                ,'选择要消耗的资源：')
        if(theType==None):return True
        Player.resource[theType]-=3
    
    def gain(self,no,card):
        if(self.canGain(card)):
            if(self.cost(card,no)):return
        Gui.newMessage('资源不足!')
    
    def use(self,no):
        card=self.hand[no]
        c=card.category()
        had=False
        Gui.newMessage(f'使用了{card.name}')
        self.hand[no]=None
        Gui.handLost(no)
        if c==0:#角色
            # Player.cardTemp=card
            Skill.spell0(card)
            # if Skill.spell0(card)==1:
            #     Gui.newMessage('使用被撤销。')
            #     return #检查skill,0---use 
            if Skill.card!=None:
                Player.used.append(card)
        else:#设施
            if self.haveFacility(card.name):
                Gui.newMessage('已拥有。')
                self.draw()
                had=True
                Player.used.append(card)
            if(not had):
                if 1 in card.skill:#check buff
                    Player.appendBuff(card.name)
                self.facility.append(card)
                Gui.facilityAppend()
        if(not had):
            self.checkUsing(card)
            self.gainResourse(card)
        
    
    def catch(self,no):
        if no>len(self.monster)-1:return
        m=self.monster[no]
        Gui.newMessage(f'{self.name}捕获了{m.name}')
        #return None or 0 will catch it,except 1
        r=Skill.spell0(m)
        if not r :
            Player.exileAdd(self.monster.pop(no))
            self.gainFromMonster()
            return True
        #Gui.monsterLost(no)
    
    def showThrow(self):
        name=[]
        for i in self.throw:
            name.append(i.name)
        Gui.newMessage(self.name,'的弃牌堆:',name)
    
    def showHand(self):
        name=[]
        for i in self.hand:
            if i==None:name.append('None')
            else:name.append(i.name)
        Gui.newMessage(self.name,'的手牌:',name)
    
    def showDeck(self):
        # Gui.shuffleAndShow(self.deck)
        name,num,no=[],[],0
        for i in self.deck:
            j=findIndex(name,i.name)
            if  j!=-1:#already exist
                num[j]+=1
            else:
                name.append(i.name)
                num.append(1)
        text=''
        for i in range(len(num)):
            text+=f'{num[i]}x{name[i]}\n'
        text=text[:-1]
        Gui.newMessage(self.name,'的卡组:\n',text)

        for i in range(len(num)-1):
            if num[i+1]>num[i]:
                name[i+1],name[i]=name[i],name[i+1]
                num[i+1],num[i]=num[i],num[i+1]
    
    def lost(self,no):
        card=self.hand[no]
        self.hand[no]=None
        self.throw.append(card)
        # if card!=None:self.throw.append(card)
        # else:print('---------------丢弃时出错')
        Gui.newMessage(f'{self.name}丢弃了{card.name}.')
        Gui.handLost(no)
    
    def repeatCard(self):
        if(self.repeat==[]):return
        for card in self.repeat:
            Gui.newMessage('迂返生效:'+card.name)
            self.gainResourse(card)
            Skill.spell0(card)
            self.throw.append(card)
            # if len(card.skill[0]):
            #     if card.skill[0][0] in [16,26]:
            #         print('复制了迂返效果')
            #         s=card.skill
            #         s[0]=s[0:1]
            #         s.remove(3)
            #         card.gain=[0,0,0]
        self.repeat=[]
    
    def count(self):#计算储备资源
        listsAdd(Player.exResource,self.monster)
        self.gainResourse(self.facility)
    
    def exileOne(self):
        #只删除0或1分卡，
        #并且当弃牌堆与手卡有同名的卡时，只能删除弃牌堆的
        card,no,name=[],[],set()
        inThrow,n=0,0
        for i in self.throw:
            if(i.score<2 and (i.name not in name)):
                card.append(i)
                inThrow+=1
                no.append(n)
                name.add(i.name)
            n+=1
        n=-1
        for i in self.hand:
            n+=1
            if(i==None):continue
            if(i.score==0 and (i.name not in name)):
                card.append(i)
                no.append(n)
                name.add(i.name)
        if(no==[]):
            Gui.newMessage('无卡可放逐!')#No card can be exiled
            return 0
        r=Gui.askOne(card,inThrow,no)
        if(r==-2):#不放逐
            Gui.newMessage('取消放逐.')
            return -2
        else:
            index=no[r]
            if(r<inThrow):#throw
                self.throw.pop(index)
            else:#hand
                self.hand[index]=None
                Gui.handLost(index)
            # Gui.newMessage(f'{self.name}放逐了{name[r]}')
            Player.exileAdd(card[r])
    
    def destory(self,no,show=True):
        if(no>=len(self.facility)):
            Gui.newMessage('越界!')#Out of index
            return 1
        self.throw.append(self.facility.pop(no))
        name=self.throw[-1].name
        if show:
            Gui.facilityLost(no)
            i=findIndex(Player.names,name)
            if(i!=-1):Player.lostBuff(i)
        Gui.newMessage(f'摧毁了{self.name}的{name}.')
    
    def selfDestory(self,name):
        n=0
        for i in self.facility:
            if(i.name==name):
                self.throw.append(self.facility.pop(n))
                Gui.facilityLost(n)
                Gui.newMessage(f'摧毁了{name}')#Destory the 
                return
            n+=1
        Gui.newMessage(f'找不到{name}!')#Can not find 
        return 1
    
    def haveFacility(self,name):
        for i in self.facility:
            if(i.name==name):return True
        return False
    
    def obtain(self,card,no=10):
        Gui.showResource(Player.resource)
        if card.category()==2:#monster
            Gui.newMessage(f'{self.name}退治了{card.name}.')
            self.gainResourse(card)
            Skill.spell1(card)
            if(card.canBeClick()):
                self.monster.append(card)
                Gui.monsterAppend()
            else:self.monster2.append(card)
            Skill.checkRetreat(card.totalCost())
            self.gainFromMonster()
        else:#character or facility
            Gui.newMessage(f'{self.name}获得了{card.name}.')
            if self.checkGaining(card):
                self.throw.append(card)
        Gui.center.next(no)
        return True
    
    def checkUsing(self,card):
        if(card.isFaith()):#信仰相关记录
            Player.faithCard+=1
            if(card.category()==0):
                Player.faithChar+=1
                if (Player.buff[0] 
                    and Player.faithChar==1 
                    and self.haveFacility('赛钱箱')):
                    Gui.newMessage('赛钱箱生效。')
                    Player.lostBuff(0)
                    Player.resource[1]+=1
                    Gui.showResource(Player.resource) #'赛钱箱'
        if( Player.buff[1] and card.place==10):
            # print('miko')
            for i in Player.used[:-1]:#'丰聪耳神子'
                if(i.name==card.name):return
            self.gainResourse(card)
            Gui.newMessage('丰聪耳神子生效。')
    def checkGaining(self,card):
        if (not Player.timing[1]) or (not card.isFaith()):
            return True
        b=Player.buff
        name=card.name
        c=card.category()
        if b[9] and c==1:
            Gui.newMessage('纳兹琳生效。')
            ask=messagebox.askyesno('纳兹琳',
                        f'是否将{name}加入手卡？')
            if ask:
                self.hand.append(card)
                Gui.handAppend()
                Player.lostBuff(9)
                return False
        #if go to other place,return false
        result=True
        for i in range(6,9):
            if b[i]:#如果有buff
                if i<8:#御柱，阿牟
                    if i==6 and not self.haveFacility('神奈子的御柱'):
                            continue
                    Gui.newMessage(f'{Player.names[i]}生效。')
                    ask=messagebox.askyesno(Player.names[i],
                        f'是否将{name}放置在牌堆顶？')
                    if ask:
                        self.deck.append(card)
                        result= False
                        break
                        #Player.cardTemp=None
                else:#八坂神奈子
                    Gui.newMessage('八坂神奈子生效。')
                    ask=messagebox.askyesno('八坂神奈子',
                        f'是否将{name}加入手卡？')
                    if ask:
                        self.hand.append(card)
                        Gui.handAppend()
                        result= False
                        break
        for i in range(6,9):
            if b[i]:Player.lostBuff(i)
        return result
    def checkBeforeGaining(self):
        pass

    def handNumber(self):
        n=0
        for i in self.hand:
            if i != None:n+=1
        return n
    
    def rebuild(self):
        card,no,n=[],[],-1
        for i in self.throw:
            n+=1
            if(i.category()==1):
                card.append(i)
                no.append(n)
        if(card==[]):
            Gui.newMessage('没有设施牌在弃牌堆!')#No facility in throw
            return 1
        elif len(no)==1:
            r=0
        else:#
            r=Gui.askOne2(card,'选择一张重建')
            if(r==-2):return 1
        #上手
        self.hand.append(card[r])
        self.throw.pop(no[r])
        Gui.handAppend()
        Gui.newMessage(f'{self.name}重建了{card[r].name}.')#
    
    def neatHand(self):
        n=0
        for i in self.hand:
            if i==None:n+=1
        for i in range(n):self.hand.remove(None)
    
    def bind():
        Skill.init()
        Gui.showHome()
        Gui.root.bind('<space>',Player.useAll)
        Gui.root.bind('<Control-e>',Gui.end)
        Gui.root.bind('<Control-r>',Gui.returnHome)
        Gui.root.bind('<Control-s>',Skill.spellAny)
        Gui.root.bind('<Control-f>',Player.launchOne)
        Gui.root.bind('<Control-q>',Gui.beNormal)
        Gui.root.bind('<Control-t>',Gui.changeAlpha)
from skill import Skill


# Gui.init()
# print(time()-timeCount)
# Gui.root.mainloop()
# def listsAdd(a,b):#a is resourse,b are cards
#     for i in b:
#         for j in range(3):a[j]+=i.gain[j]
