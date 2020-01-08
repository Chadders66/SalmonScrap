from tkinter import *
from PIL import ImageTk,Image
import os

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("1000x600")

frame = LabelFrame(root, text="Player One", padx=20, pady=20)
frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=10, pady=5)

frame1 = LabelFrame(root, text="Player Two", padx=20, pady=20)
frame1.grid(row=0, column=2, rowspan=2, columnspan=2, padx=10, pady=5)


image = Image.open("SalmonScrap/v0.2/assets/blank.png") #resize image
image = image.resize((165, 130), Image.ANTIALIAS)

img_blank = ImageTk.PhotoImage(image) #puts it in a variable
label = Label(frame, image=img_blank) #puts it in player frame
label1 = Label(frame, image=img_blank)
label2 = Label(frame, image=img_blank)
label3 = Label(frame, image=img_blank)
label.grid(row=0, column=0)
label1.grid(row=0, column=1)
label2.grid(row=1, column=0)
label3.grid(row=1, column=1)

label4 = Label(frame1, image=img_blank) #puts it in player frame
label5 = Label(frame1, image=img_blank)
label6 = Label(frame1, image=img_blank)
label7 = Label(frame1, image=img_blank)
label4.grid(row=0, column=2)  
label5.grid(row=0, column=3)
label6.grid(row=1, column=2)
label7.grid(row=1, column=3)

root.mainloop()
