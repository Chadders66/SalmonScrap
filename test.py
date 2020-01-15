from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("")
root.geometry("")

frameList = []
labelList = []
buttonList = []

image = Image.open("assets/yacht.png")
image = image.resize((165, 130), Image.ANTIALIAS)

for x in range(3):                                           #number of labels you want to create
    labelList.append(Label(root, text=x+1, bg='Yellow'))     #text= image= justify= compound= font= bg= fg=
    labelList[x].grid(row=2*x, column=2, rowspan=2, ipady=16, ipadx=10)          #columnspan= rowspan= padx= pady=

for y in range(3):                                           #number of labels you  want to create
    buttonList.append(Button(root, text='+', width=5))           #text= image= justify= compound= font= bg= fg=
    buttonList[y].grid(row=2*y, column=3)                   #columnspan= rowspan= padx= pady=
for z in range(3):                                           #number of labels you  want to create
    buttonList.append(Button(root, text='-', width=5))           #text= image= justify= compound= font= bg= fg=
    buttonList[z+3].grid(row=(2*z)+1, column=3)                   #columnspan= rowspan= padx= pady=
for a in range(2):                                           #number of labels you  want to create
    buttonList.append(Button(root, text='-', width=5))           #text= image= justify= compound= font= bg= fg=
    buttonList[a+6].grid(row=(2*z)+1, column=3)                   #columnspan= rowspan= padx= pady=

root.mainloop()