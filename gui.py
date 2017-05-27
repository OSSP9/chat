# -*- coding: utf-8 -*-
#from tkinter import *
#import Tkinter
from Tkinter import *
import sys
import thread
from socket import *

serverPort = 7129  # 포트
b1 = "up"
xold, yold = None, None

class window:
 def sub(self):
   global IP, NAME
   Name = self.entry1.get()
   serverHost= self.entry2.get()
   self.master.quit()
   self.master.destroy()
 def __init__(self,Master):
   self.master = Master
   Master.title("Start") 
   #self.master.geometry("400x200")
   self.mainFrame = Frame(self.master)
   self.mainFrame.pack(fill=X)
   
#nickname
   self.frame1 = Frame(self.mainFrame)
   self.frame1.pack(fill=X)
   self.nickLabel = Label(self.frame1)
   self.nickLabel.configure(text = "NickName", width =10)
   self.nickLabel.pack(side = LEFT)
   self.entry1 = Entry(self.frame1)
   self.entry1.pack(side=LEFT)
   
#serverIP
   self.frame2 = Frame(self.mainFrame)
   self.frame2.pack(fill=X)
   self.ipLabel = Label(self.frame2)
   self.ipLabel.configure(text = "Server IP", width =10)
   self.ipLabel.pack(side = LEFT)
   self.entry2 = Entry(self.frame2)
   self.entry2.pack(side=LEFT)
   
#PORT
  # self.frame3 = Frame(self.mainFrame)
   #self.frame3.pack(fill=X)
   #self.portLabel = Label(self.frame3)
   #self.portLabel.configure(text = "PORT", width =10)
   #self.portLabel.pack(side = LEFT)
   #self.entry3 = Entry(self.frame3)
  # self.entry3.pack(side=LEFT)

   self.frame4 = Frame(self.mainFrame)
   self.frame4.pack(fill=X)
   self.emptyLabel = Label(self.frame4)
   self.emptyLabel.configure(text = "   ", width =1)
   self.emptyLabel.pack(side = LEFT)
   self.button1= Button(self.frame4)
   self.button1.configure(text ="OK",width =10,command=self.sub)
   self.button1.pack(side =LEFT, fill=X)
   self.button2= Button(self.frame4)
   self.button2.configure(text ="END",width =10)
   self.button2.pack(side=LEFT, fill=X)



class mainapp():
 def b1down(self,event):
    global b1
    b1 = "down"           # you only want to draw when the button is down
                          # because "Motion" events happen -all the time-

 def b1up(self,event):
    global b1, xold, yold
    b1 = "up"
    xold = None           # reset the line when you let go of the button
    yold = None

 def motion(self,event):
    if b1 == "down":
        global xold, yold
        if xold is not None and yold is not None:
            event.widget.create_line(xold,yold,event.x,event.y,smooth=TRUE)
                          # here's where you draw it. smooth. neat.
        xold = event.x
        yold = event.y

 def __init__(self,Master):

   self.master = Master
   Master.title("Start") 
   #Master.geometry("500x600")
   #-----------Master---------
   self.masterFrame = Frame(self.master)
   self.masterFrame.pack()
   
   # ipad,pad size
   frame_ipadx="2"
   frame_ipady="2"
   frame_padx="2"
   frame_pady="2"
   
   #-----------toptop_frame------------------
   self.toptop_frame = Frame(self.masterFrame,width = 450,height=1)
   self.toptop_frame.pack()
   self.savebutton=Button(self.toptop_frame,text="SAVE",width=35)
   self.savebutton.pack(side=LEFT)
   self.exitbutton=Button(self.toptop_frame,text="EXIT",width=35)
   self.exitbutton.pack(side=RIGHT)


   #-------------top_frame----------------
   self.top_frame = Frame(self.masterFrame,  width = 450,height = 500)
   self.top_frame.pack(side = TOP,fill=BOTH, expand = YES)
  

   ##------------left_frame and right_frame in top_frame
   self.left_frame= Frame(self.top_frame,width= 150,height = 480)
   self.left_frame.pack(side=LEFT)

   self.right_frame = Frame(self.top_frame,width=380, height = 480)
   self.right_frame.pack(side=RIGHT)

   ###---------------- paint_tool in left_frame
   ####----------------------tool_frame
   self.tool_frame = Frame(self.left_frame, width = 160, height = 70)
   self.tool_frame.pack(side=TOP)
   self.red_color=Button(self.tool_frame, background="red",activebackground="red",borderwidth=0)
   self.red_color.pack(side=LEFT, fill= BOTH)

   self.orange_color=Button(self.tool_frame, background="orange",activebackground="orange",borderwidth=0)
   self.orange_color.pack(side=LEFT, fill= BOTH)

   self.yellow_color=Button(self.tool_frame, background="yellow",activebackground="yellow",borderwidth=0)
   self.yellow_color.pack(side=LEFT)

   self.green_color=Button(self.tool_frame, background="green",activebackground="green",borderwidth=0)
   self.green_color.pack(side=LEFT)

   self.blue_color=Button(self.tool_frame, background="blue",activebackground="blue",borderwidth=0)
   self.blue_color.pack(side=LEFT)

   self.purple_color=Button(self.tool_frame, background="purple",activebackground="purple",borderwidth=0)
   self.purple_color.pack(side=LEFT)

   ####----------------------tool2_frame
   self.tool2_frame = Frame(self.left_frame, width = 160, height = 70)
   self.tool2_frame.pack(side=TOP)

   self.black_color=Button(self.tool2_frame,   background="black",activebackground="black",borderwidth=0)
   self.black_color.pack(side=LEFT,fill= BOTH)

   self.erase=Button(self.tool2_frame,text="erase",width=1)
   self.erase.pack(side=LEFT, fill= BOTH)
   self.option=Button(self.tool2_frame, text="/",width=1)
   self.option.pack(side=LEFT, fill= BOTH)
   self.option1=Button(self.tool2_frame, text="O",width=1)
   self.option1.pack(side=LEFT, fill= BOTH)
   self.option2=Button(self.tool2_frame, text="ㅁ",width=1)
   self.option2.pack(side=LEFT, fill= BOTH)

   ####----------------------tool3_frame
   self.tool3_frame = Frame(self.left_frame, width = 150, height = 70)
   self.tool3_frame.pack(side=TOP)
   self.label_bold =Label(self.tool3_frame,text="Bold")
   self.label_bold.pack(side=LEFT)
   self.Entry_bold = Entry(self.tool3_frame,width=17)
   self.Entry_bold.pack(side=LEFT)

   ####----------------------empty tool_frame
   self.tool4_frame = Frame(self.left_frame, width = 150, height = 420)
   self.tool4_frame.pack(side=TOP)


   #### Label in right_top_frame
   #------------noticeLabel
   self.noticeLable = Label(self.right_frame,width = 54)
   self.noticeLable.configure(text="NOTICE",background="white")
   self.noticeLable.pack()

   ###----------------drawing_area in right_frame------------
   self.drawing_area = Canvas(self.right_frame,background="white",width=380,height=480)
   self.drawing_area.pack()
   self.drawing_area.bind("<Motion>", self.motion)
   self.drawing_area.bind("<ButtonPress-1>", self.b1down)
   self.drawing_area.bind("<ButtonRelease-1>", self.b1up)



   #---------------bottom_frame---------
   self.bottom_frame=Frame(self.masterFrame,height=190, width=400)
   self.bottom_frame.pack(side =TOP,fill=BOTH,expand=YES)

   ##left2_frame and right2_frame in bottom_frame
   self.left2_frame= Frame(self.bottom_frame, height = 190,width =170)
   self.left2_frame.pack(side = LEFT, fill =BOTH, expand=YES)

   self.right2_frame= Frame(self.bottom_frame, width=380,height = 190)
   self.right2_frame.pack(side = LEFT, fill =BOTH, expand=YES)
   ###--------------listbox in left2_frame
   self.listbox = Listbox(self.left2_frame, height = 12,width =24,background="white")
   self.listbox.insert(1,"John")
   self.listbox.insert(1,"cris")
   self.listbox.pack(side = LEFT)


   ###----------- right2_top_frame in right2 frame
   #### --------------right2_top_frame in right2_frame
   self.right2_top_frame = Frame (self.right2_frame,background="white",width=380,height=170)
   self.right2_top_frame.pack()

   #####----------------messageLog in right2_top_frame
   self.messageLog=Text(self.right2_top_frame)
   self.messageLog.configure(width=60,height=11,state = "disabled")
   self.messageLog.grid()
   self.messageLog.pack(side=LEFT)

   self.scrollbar=Scrollbar(self.right2_top_frame)
   self.scrollbar.pack(side=RIGHT,fill=Y,expand=False)

   ####------------ right2_bottom_frame in right2_frame
   self.right2_bottom_frame = Frame(self.right2_frame,background="white",width=380,height=30)
   self.right2_bottom_frame.pack()


   ##### textinput and button in right2_bottom_frame
   #---------------textinput & button
   self.textinput=Text(self.right2_bottom_frame,width = 50,height=1)
   self.textinput.pack(side=LEFT)
   self.sendButton = Button(self.right2_bottom_frame,width=6,height=1,text="Send")
   self.sendButton.configure(background="yellow")
   self.sendButton.pack(side=RIGHT)
   
   

root = Tk()
app = window(root)

root.title("chat")
root.mainloop()

root1=Tk()
pp=mainapp(root1)
root1.mainloop()



