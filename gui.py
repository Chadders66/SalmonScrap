from tkinter import *
from PIL import ImageTk,Image
import os

root = Tk()
root.title("Salmon Scrap - Get the most fish!")
root.geometry("400x300")

frame = LabelFrame(root, text="Player One", padx=20, pady=20)
frame.grid(row=0, column=0, padx=10, pady=5)


image = Image.open("SalmonScrap/v0.2/assets/longliner.png") #resize image
image = image.resize((165, 130), Image.ANTIALIAS)

img_longliner = ImageTk.PhotoImage(image) #puts it in a variable
label = Label(frame, image=img_longliner) #puts it in player frame
label.pack()                                #displays

root.mainloop()
