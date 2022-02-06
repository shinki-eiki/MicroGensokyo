from tkinter import Radiobutton
class PlayerButton():
	"""docstring for ClassName"""
	def __init__(self,father,text,f,**kw):
		#label show text
		self.label =Radiobutton(father,
			font=f,textvariable=text,**kw)
		self.button=Radiobutton(father,**kw)
		self.var=self.label['value']
	# use image as a parameter
	def changeImageWithPhoto(self,photo):
		self.button.config(image=photo)
		self.button.image=photo

	def place2(self,y):#height0=0.3
		self.button.place(rely=y,relheigh=0.14,relwidth=0.3)
		self.label .place(relx=0.3,rely=y,relheigh=0.14,relwidth=0.7)

	def setText(self,t):
		self.label.config(text=t)
'''
	# def get(self):return self.label['value']
	def bind(self,fun):
		self.button.bind('<Enter>',fun)
		self.label .bind('<Enter>',fun)
	
	def changeImage(self,card):
		photo=card.getImage()
		self.button.config(image=photo)
		self.button.image=photo

	def pack(self,**kw):
		self.label. pack(kw)
		self.button.pack(kw)

	def place(self,x,y=0):#height0=0.3
		self.label .place(relx=x,rely=y,relheigh=0.25,relwidth=0.15)
		self.button.place(relx=x,rely=y+0.25,relheigh=0.75,relwidth=0.15)
		#chane
	def place_forget(self):
		self.button.place_forget()
		self.label .place_forget()
'''