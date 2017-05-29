# -*- coding: utf-8 -*-
#from tkinter import *
#import Tkinter
from Tkinter import *
import sys
import thread
from socket import *

serverPort = 7382  # 포트
b1 = "up"
xold, yold = None, None

class window1:#IP 입력화면 클래스 

 def __init__(self,Master):
   self.master = Master
   Master.title("IP") 
   self.mainFrame = Frame(self.master)
   self.mainFrame.pack(fill=X)
   
   #serverIP 입력 프레임과 입력위젯 
   self.IP_frame1 = Frame(self.mainFrame)
   self.IP_frame1.pack(fill=X)
   self.ipLabel = Label(self.IP_frame1)#Server IP메시지 출력 위젯 
   self.ipLabel.configure(text = "Server IP", width =10)
   self.ipLabel.pack(side = LEFT)
   self.IP_entry = Entry(self.IP_frame1)#Server IP입력창 위젯 
   self.IP_entry.pack(side=LEFT)
   
   #OK버튼,END버튼 프레임과 위젯 
   self.IP_frame2 = Frame(self.mainFrame)
   self.IP_frame2.pack(fill=X)
   self.emptyLabel = Label(self.IP_frame2)#이건 그냥 빈공간 만드려고 한 것 (무시)
   self.emptyLabel.configure(text = "   ", width =1)
   self.emptyLabel.pack(side = LEFT)
   self.button1= Button(self.IP_frame2)#OK버튼 위젯 
   self.button1.configure(text ="OK",width =10,command=self.submit_IP)

   self.button1.pack(side =LEFT, fill=X)
   self.button2= Button(self.IP_frame2)#END버튼 위젯
   self.button2.configure(text ="END",width =10,command=self.exit1)
   self.button2.pack(side=LEFT, fill=X)
   
 def submit_IP(self): #입력화면에서 OK버튼을 누르면 입력한 IP를 저장 후, 닉네임입력화면으로 넘어가는 함수  
     global IP
     IP= self.IP_entry.get()
     self.master.quit()
     self.master.destroy()

 def exit1(self):#IP입력화면에서 END버튼을 누르면 시스템 종료  
     sys.exit()

class window2:#Nickname 입력화면 클래스 
 
 def __init__(self,Master):
   self.master = Master
   Master.title("Start") 
   self.mainFrame = Frame(self.master)
   self.mainFrame.pack(fill=X)

   #nickname입력 프레임과 입력위젯 
   self.nick_frame1 = Frame(self.mainFrame)
   self.nick_frame1.pack(fill=X)
   self.nickLabel = Label(self.nick_frame1) #Nickname메시지 출력 위젯 
   self.nickLabel.configure(text = "NickName", width =10)
   self.nickLabel.pack(side = LEFT) 
   self.nick_entry = Entry(self.nick_frame1) #Nickname입력창 위젯  
   self.nick_entry.pack(side=LEFT)

   #OK버튼,END버튼 프레임과 위젯
   self.nick_frame2 = Frame(self.mainFrame)
   self.nick_frame2.pack(fill=X)
   self.emptyLabel2 = Label(self.nick_frame2)#이건 그냥 빈공간 만드려고 한 것 (무시)
   self.emptyLabel2.configure(text = "   ", width =1)
   self.emptyLabel2.pack(side = LEFT)
   self.button3= Button(self.nick_frame2)#OK버튼 위젯 
   self.button3.configure(text ="OK",width =10,command=self.submit_Nick)
   self.button3.pack(side =LEFT, fill=X)
   self.button4= Button(self.nick_frame2)#END버튼 위젯  
   self.button4.configure(text ="END",width =10,command=self.exit2)
   self.button4.pack(side=LEFT, fill=X)


 def submit_Nick(self): #입력화면에서 OK버튼을 누르면 입력한 Nickname를 저장 후, 채팅화면으로 넘어가는 함수 
   global Name
   Name = self.nick_entry.get()
   self.master.quit()
   self.master.destroy()

 def exit2(self):#채팅화면에서 EXIT버튼을 누르면 시스템종료  
     sys.exit()

class mainapp():#채팅 화면  
#--------------------그림그리기 함수들----------------------  
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

 def exit3(self):#채팅화면에서 EXIT버튼을 누르면 시스템 종료  
   sys.exit()

 def __init__(self,Master,s):

   self.master = Master
   Master.title("Start") 
   #-----------Master---------
   self.masterFrame = Frame(self.master)
   self.masterFrame.pack()
   
   # ipad,pad size
   frame_ipadx="2"
   frame_ipady="2"
   frame_padx="2"
   frame_pady="2"
   
   #-----------toptop_frame------------------SAVE, EXIT버튼 프레임 및 위젯  
   self.toptop_frame = Frame(self.masterFrame,width = 450,height=1)
   self.toptop_frame.pack()
   self.savebutton=Button(self.toptop_frame,text="SAVE",width=35)
   self.savebutton.pack(side=LEFT)
   self.exitbutton=Button(self.toptop_frame,text="EXIT",width=35,command = self.exit3)
   self.exitbutton.pack(side=RIGHT)


   #-------------top_frame---------------- 
   self.top_frame = Frame(self.masterFrame,  width = 450,height = 500)
   self.top_frame.pack(side = TOP,fill=BOTH, expand = YES)
  

   ##------------left_frame and right_frame in top_frame
   self.left_frame= Frame(self.top_frame,width= 150,height = 480)
   self.left_frame.pack(side=LEFT)

   self.right_frame = Frame(self.top_frame,width=380, height = 480)
   self.right_frame.pack(side=RIGHT)

   ###---------------- paint_tool in left_frame 페인트 툴 프레임 
   ####----------------------tool_frame 페인트 툴에 색(빨주노초파보)을 구현할 프레임
   self.tool_frame = Frame(self.left_frame, width = 160, height = 70)
   self.tool_frame.pack(side=TOP)
   #빨  
   self.red_color=Button(self.tool_frame, background="red",activebackground="red",borderwidth=0)
   self.red_color.pack(side=LEFT, fill= BOTH)
   #주  
   self.orange_color=Button(self.tool_frame, background="orange",activebackground="orange",borderwidth=0)
   self.orange_color.pack(side=LEFT, fill= BOTH)
   #노  
   self.yellow_color=Button(self.tool_frame, background="yellow",activebackground="yellow",borderwidth=0)
   self.yellow_color.pack(side=LEFT)
   #초  
   self.green_color=Button(self.tool_frame, background="green",activebackground="green",borderwidth=0)
   self.green_color.pack(side=LEFT)
   #파  
   self.blue_color=Button(self.tool_frame, background="blue",activebackground="blue",borderwidth=0)
   self.blue_color.pack(side=LEFT)
   #보 
   self.purple_color=Button(self.tool_frame, background="purple",activebackground="purple",borderwidth=0)
   self.purple_color.pack(side=LEFT)

   ####----------------------tool2_frame 페인트 툴에 색(검정), 지우기, 선,원,사각형을 구현할 프레
   self.tool2_frame = Frame(self.left_frame, width = 160, height = 70)
   self.tool2_frame.pack(side=TOP)

   #검정  
   self.black_color=Button(self.tool2_frame,   background="black",activebackground="black",borderwidth=0)
   self.black_color.pack(side=LEFT,fill= BOTH)
   #지우기 버튼 
   self.erase=Button(self.tool2_frame,text="erase",width=1)
   self.erase.pack(side=LEFT, fill= BOTH)
   #선 버튼 
   self.option=Button(self.tool2_frame, text="/",width=1)
   self.option.pack(side=LEFT, fill= BOTH)
   #원 버튼 
   self.option1=Button(self.tool2_frame, text="O",width=1)
   self.option1.pack(side=LEFT, fill= BOTH)
   #사각형 버튼  
   self.option2=Button(self.tool2_frame, text="ㅁ",width=1)
   self.option2.pack(side=LEFT, fill= BOTH)

   ####----------------------tool3_frame 페인트 툴에 선의 두께를 구현할 프레임  
   self.tool3_frame = Frame(self.left_frame, width = 150, height = 70)
   self.tool3_frame.pack(side=TOP)
   #Bold 라고 화면에 글씨 띄우는 위젯 
   self.label_bold =Label(self.tool3_frame,text="Bold")
   self.label_bold.pack(side=LEFT)
   #두께 입력창  
   self.Entry_bold = Entry(self.tool3_frame,width=13)
   self.Entry_bold.pack(side=LEFT)
   #두께 입력하고 적용할 버튼 
   self.boldbutton=Button(self.tool3_frame, text="set",width=1)
   self.boldbutton.pack(side=LEFT)

   ####----------------------empty tool_frame 페인트 툴에 빈 프레임 (무시)  
   self.tool4_frame = Frame(self.left_frame, width = 150, height = 420)
   self.tool4_frame.pack(side=TOP)


   #### Label in right_top_frame 공지메시지, 그림판   
   #------------noticeLabel 공지메시지  띄우는 위젯 
   self.noticeLable = Label(self.right_frame,width = 54)
   self.noticeLable.configure(text="NOTICE",background="white")
   self.noticeLable.pack()

   ###----------------drawing_area in right_frame------------그림판 위젯  
   self.drawing_area = Canvas(self.right_frame,background="white",width=380,height=480)
   self.drawing_area.pack()
   self.drawing_area.bind("<Motion>", self.motion)
   self.drawing_area.bind("<ButtonPress-1>", self.b1down)
   self.drawing_area.bind("<ButtonRelease-1>", self.b1up)


   #---------------bottom_frame---------사용자 리스트, 메시지 채팅창 프레임  
   self.bottom_frame=Frame(self.masterFrame,height=190, width=400)
   self.bottom_frame.pack(side =TOP,fill=BOTH,expand=YES)

   ##left2_frame and right2_frame in bottom_frame 
   #사용자 리스트 프레임 
   self.left2_frame= Frame(self.bottom_frame, height = 190,width =170)
   self.left2_frame.pack(side = LEFT, fill =BOTH, expand=YES)

   #메시지 채팅창 프레임 
   self.right2_frame= Frame(self.bottom_frame, width=380,height = 190)
   self.right2_frame.pack(side = LEFT, fill =BOTH, expand=YES)

   ###--------------listbox in left2_frame 사용자 리스트 위젯 
   self.listbox = Listbox(self.left2_frame, height = 12,width =24,background="white")
   self.listbox.insert(1,"John")
   self.listbox.insert(1,"cris")
   self.listbox.pack(side = LEFT)


   ###----------- right2_top_frame in right2 frame 메시지 채팅창 프레임 내의 메시지 로그창 프레임  
   #### --------------right2_top_frame in right2_frame
   self.right2_top_frame = Frame (self.right2_frame,background="white",width=380,height=170)
   self.right2_top_frame.pack()

   #####----------------messageLog in right2_top_frame 메시지 로그창 프레임내 메시지 로그 , 메시지 스크롤바 위젯  
   self.messageLog=Text(self.right2_top_frame)
   self.scrollbar=Scrollbar(self.right2_top_frame,command=self.messageLog.yview)
   self.messageLog.configure(width=60,height=11,state = "disabled",yscrollcommand=self.scrollbar.set)
   self.messageLog.grid()
   self.messageLog.pack(side=LEFT,fill="both",expand=True)
   self.scrollbar.pack(side=RIGHT,fill=Y,expand=False)
   

  

   ####------------ right2_bottom_frame in right2_frame  메시지 채팅창 프레임 내 메시지를 입력하는 프레임  
   self.right2_bottom_frame = Frame(self.right2_frame,background="white",width=380,height=30)
   self.right2_bottom_frame.pack()


   ##### textinput and button in right2_bottom_frame 메시지를 입력하는 프레임 내 메시지 입력 위젯과 메시지 보내기 버튼 위젯 
   #---------------textinput & button
   self.textinput=Text(self.right2_bottom_frame,width = 50,height=1)
   self.textinput.pack(side=LEFT)
   self.sendButton = Button(self.right2_bottom_frame,width=6,height=1,text="Send",command=self.sendMessage)
   self.sendButton.pack()
   self.sendButton.bind("<Return>",self.buttonClicked_sub)
   self.textinput.bind("<Key-Return>",self.buttonClicked_sub)
   self.sendButton.configure(background="yellow")
   self.sendButton.pack(side=RIGHT)
   
  # thread.start_new_thread(handler,(s,))


#메시지 출력
 def logRefresh(self,data):
     self.messageLog.configure(state="normal")
     self.messageLog.insert(END,data)
     self.messageLog.configure(state="disabled")

#메시지 입력
 def buttonClicked(self):
     self.sendMessage()
     
 def buttonClicked_sub(self,event):
     self.sendMessage()

 def sendMessage(self):
     message = self.textinput.get(1.0,END)
     s.send(message)
     self.textinput.delete(1.0,END)





def handler(sock) :
        print "Thread start!"
        #sock.send("gogo!")
        #sock.socket= socket.socket()
        #sock.connect((IP,int(serverPort)))
        while 1:
            try:
                data = sock.recv(1024)
            except timeout:
                continue
            else:
                print data
                main.logRefresh(data)
           
          


#IP입력화면 
s = socket(AF_INET,SOCK_STREAM) #소켓생성

root = Tk()
entrance= window1(root)
root.title("IP")
root.mainloop()

try:
    print IP+"로 접속 시도"
    s.connect((IP,int(serverPort)))
    s.settimeout(5.1)
    print "접속 완료"
except:
    print "접속 실패"
    sys.exit()


#Nickname입력화면 
root1 = Tk()
entrance= window2(root1)
root1.title("Nickname")
root1.mainloop()

try:
    s.send(Name)
    print Name+"으로 접속!"
except:
    print "접속 실패"
    sys.exit()



thread1= thread.start_new_thread(handler,(s,))
#채팅화면 
root2=Tk()
main=mainapp(root2,s)
root2.title("main")
root2.mainloop()

s.close() 
#thread = thread.start_new_thread(handler,(s,))
#thread1 = threading.Thread(target = network)

#thread1.start()







