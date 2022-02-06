from PIL import Image,ImageTk

# imgOpen=Image.open(a)
# photo=ImageTk.PhotoImage(imgOpen)
# return photo

#头像文件夹下
def findHeadImage(s):
    a='headImage/'+f'{s}.jpg'
    imgOpen=Image.open(a)
    photo=ImageTk.PhotoImage(imgOpen)
    return photo
#当前目录下
def findImage(s='test'):#find image
    a=str(s)+'.jpg'
    photo=ImageTk.PhotoImage(file=a)
    return photo
#image文件夹下
def findCardImage(s='test'):#find image
    a='image/'+f'{s}.jpg'
    photo=ImageTk.PhotoImage(file=a)
    return photo
#给出card对象
def changeImageWithCard(label,card):
    photo=card.getImage()
    label.config(image=photo)
    label.image=photo
# 
#给出图片名字,place indicate where the image is,0 is normal card image
def changeImageWithName(label,name='cover',place=0):
    #need to find image
    if place==0:photo=findImage(name)
    elif place==1:photo=findHeadImage(name)
    label.config(image=photo)
    label.image=photo

#给出图片
def changeImageWithPhoto(label,photo):
    label.config(image=photo)
    label.image=photo

# import tkinter as tk
# if __name__ == "__main__":
# 	root=tk.Tk()
# 	button=tk.Label(root)
# 	button.pack()
# 	changeIma(button,1,1)
# 	root.mainloop()
