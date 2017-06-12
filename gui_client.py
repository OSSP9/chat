# -*- coding: utf-8 -*-
import random
import sys
import subprocess
import os
import io
import glob
import PIL.Image
import PIL.ImageTk
from itertools import cycle
from tkinter import *
from threading import Thread
from socket import *

# BSD socket 인터페이스. AF_INET address family를 사용하고 socket types으로는 SOCK_STREAM을 지정
mySocket = socket(AF_INET, SOCK_STREAM)
import traceback

from select import select
import socket

serverPort = 7382  # 포트

# 초기값 설정
INITIAL_COLOR = "blue"
INITIAL_SHAPE = "line"
HELP_MESSAGE = "Choose a color from the color menu, and a shape.\nThen," \
               " click twice on the canvas (or 3 times for triangle) to" \
               " create the shape. "
ERROR_NAME_MSG = "Invalid username or group name.\nplease enter a name " \
                 "that contains numbers or letters (or both)"
ERROR_PORT_MSG = "The port is not valid. please enter a numerical expression"

READ_LIMIT = 1024
READ_SOCK = 0
MSG_TYPE = 0
MSG_CONTENT = 1
X_COORD = 0
Y_COORD = 1 
OVAL_LINE_RECT_COORDS_AMOUNT = 2
DEFAULT_LINE_WIDTH = 3
NAME_COORDS = 0
LEAVE_MSG = "leave\n"
STARTING_INDEX = 2
b1 = "up"
xold, yold = None, None
num = 1

class window1:  # IP,NICKNAME 입력화면 클래스

    def __init__(self, Master):
        self.master = Master
        Master.title("Entrance")
        self.mainFrame = Frame(self.master)
        self.mainFrame.pack(fill=X)

        # serverIP 입력 프레임과 입력위젯
        self.IP_frame1 = Frame(self.mainFrame)
        self.IP_frame1.pack(fill=X)
        self.ipLabel = Label(self.IP_frame1)  # Server IP메시지 출력 위젯
        self.ipLabel.configure(text="Server IP", width=10)
        self.ipLabel.pack(side=LEFT)
        self.IP_entry = Entry(self.IP_frame1)  # Server IP입력창 위젯
        self.IP_entry.pack(side=LEFT)

        # nickname입력 프레임과 입력위젯
        self.nick_frame1 = Frame(self.mainFrame)
        self.nick_frame1.pack(fill=X)
        self.nickLabel = Label(self.nick_frame1)  # Nickname메시지 출력 위젯
        self.nickLabel.configure(text="NickName", width=10)
        self.nickLabel.pack(side=LEFT)
        self.nick_entry = Entry(self.nick_frame1)  # Nickname입력창 위젯
        self.nick_entry.pack(side=LEFT)

        # OK버튼,END버튼 프레임과 위젯
        self.IP_frame2 = Frame(self.mainFrame)
        self.IP_frame2.pack(fill=X)
        self.emptyLabel = Label(self.IP_frame2)  # 이건 그냥 빈공간 만드려고 한 것 (무시)
        self.emptyLabel.configure(text="   ", width=1)
        self.emptyLabel.pack(side=LEFT)
        self.button1 = Button(self.IP_frame2)  # OK버튼 위젯
        self.button1.configure(text="OK", width=10, command=self.submit)

        self.button1.pack(side=LEFT, fill=X)
        self.button2 = Button(self.IP_frame2)  # END버튼 위젯
        self.button2.configure(text="END", width=10, command=self.exit1)
        self.button2.pack(side=LEFT, fill=X)

    def submit(self):  # 입력화면에서 OK버튼을 누르면 입력한 IP를 저장 후, 닉네임입력화면으로 넘어가는 함수
        global IP, Name
        Name = self.nick_entry.get()
        IP = self.IP_entry.get()
        # Input_List.append(Name)
        self.master.quit()
        self.master.destroy()

    def exit1(self):  # IP입력화면에서 END버튼을 누르면 시스템 종료
        sys.exit()


class mainapp():  # 채팅 화면
    # --------------------그림그리기 함수들----------------------
    def exit3(self):  # 채팅화면에서 EXIT버튼을 누르면 시스템 종료

        channelToServer.close()
        mySocket.close()
        sys.exit()

    def save(self):

        global num
        if num == 10:
           num = 1
              
        save_path='/home/som/imagefolder'
        ps=self.__canvas.postscript(colormode='color')
        img=PIL.Image.open(io.BytesIO(ps.encode('utf-8')))

        name=random.randrange(num,num+1)

        fullname=os.path.join(save_path,str(name)+".png")
        #fullname2=os.path.join(save_path2,str(name2)+".png")
        img.save(fullname)
        num = num+1

    def create_window(self):
        #self.master=Master
       
        window=Toplevel(root2)
        window.geometry("605x600")

        self.galleryframe=Frame(window)
        self.galleryframe.pack(side=TOP)
        #self.galleryframe.bind("<Key-return>",self.save)
        self.label_bold = Label(self.galleryframe, text="GALLERY",width=10)
        self.label_bold.pack()
        self.topgframe=Frame(self.galleryframe,width=600,height=200)
        self.topgframe.pack(side=TOP)

        self.ibutton1=Button(self.topgframe,width=20,height=10)
        try:
            self.image1=PhotoImage(file="/home/som/imagefolder/1.png")
            self.ibutton1=Button(self.topgframe,width=160,height=188)
            self.image1=self.image1.subsample(2)
            self.ibutton1.config(image=self.image1)
            self.ibutton1.image=self.image1
        except TclError:
            pass
        self.ibutton1.pack(side=LEFT)

        self.ibutton2=Button(self.topgframe,width=20,height=10)
        try:
            self.image2=PhotoImage(file="/home/som/imagefolder/2.png")
            self.ibutton2=Button(self.topgframe,width=160,height=188)
            self.image2=self.image2.subsample(2)
            self.ibutton2.config(image=self.image2)
            self.ibutton2.image=self.image2
        except TclError:
            pass
        self.ibutton2.pack(side=LEFT)

        self.ibutton3=Button(self.topgframe,width=20,height=10)
        try:
            self.image3=PhotoImage(file="/home/som/imagefolder/3.png")
            self.ibutton3=Button(self.topgframe,width=160,height=188)
            self.image3=self.image3.subsample(2)
            self.ibutton3.config(image=self.image3)
            self.ibutton3.image=self.image3
        except TclError:
            pass
        self.ibutton3.pack(side=RIGHT)

     

        self.midgframe=Frame(self.galleryframe,width=600,height=200)
        self.midgframe.pack(side=TOP)

        self.ibutton4=Button(self.midgframe,width=20,height=10)
        try:
            self.image4=PhotoImage(file="/home/som/imagefolder/4.png")
            self.ibutton4=Button(self.midgframe,width=160,height=188)
            self.image4=self.image4.subsample(2)
            self.ibutton4.config(image=self.image4)
            self.ibutton4.image=self.image4
        except TclError:
            pass
        self.ibutton4.pack(side=LEFT)

        self.ibutton5=Button(self.midgframe,width=20,height=10)
        try:
            self.image5=PhotoImage(file="/home/som/imagefolder/5.png")
            self.ibutton5=Button(self.midgframe,width=160,height=188)
            self.image5=self.image5.subsample(2)
            self.ibutton5.config(image=self.image5)
            self.ibutton5.image=self.image5
        except TclError:
            pass
        self.ibutton5.pack(side=LEFT)

        self.ibutton6=Button(self.midgframe,width=20,height=10)
        try:
            self.image6=PhotoImage(file="/home/som/imagefolder/6.png")
            self.ibutton6=Button(self.midgframe,width=160,height=188)
            self.image6=self.image6.subsample(2)
            self.ibutton6.config(image=self.image6)
            self.ibutton6.image=self.image6
        except TclError:
            pass
        self.ibutton6.pack(side=RIGHT)      


        self.botgframe=Frame(self.galleryframe,width=600,height=200)
        self.botgframe.pack(side=TOP)

        self.ibutton7=Button(self.botgframe,width=20,height=10)
        try:
            self.image7=PhotoImage(file="/home/som/imagefolder/7.png")
            self.ibutton7=Button(self.botgframe,width=160,height=188)
            self.image7=self.image7.subsample(2)
            self.ibutton7.config(image=self.image7)
            self.ibutton7.image=self.image7
        except TclError:
            pass
        self.ibutton7.pack(side=LEFT)

        self.ibutton8=Button(self.botgframe,width=20,height=10)
        try:
            self.image8=PhotoImage(file="/home/som/imagefolder/8.png")
            self.ibutton8=Button(self.botgframe,width=160,height=188)
            self.image8=self.image8.subsample(2)
            self.ibutton8.config(image=self.image8)
            self.ibutton8.image=self.image8
        except TclError:
            pass
        self.ibutton8.pack(side=LEFT)

        self.ibutton9=Button(self.botgframe,width=20,height=10)
        try:
            self.image9=PhotoImage(file="/home/som/imagefolder/9.png")
            self.ibutton9=Button(self.botgframe,width=160,height=188)
            self.image9=self.image9.subsample(2)
            self.ibutton9.config(image=self.image9)
            self.ibutton9.image=self.image9
        except TclError:
            pass
        self.ibutton9.pack(side=RIGHT)  

    # GUI를 그리는 함수
    def GUI_PART(self, Master):
        self.master = Master
        Master.title("Start")
        # -----------Master---------
        self.masterFrame = Frame(self.master)
        self.masterFrame.pack()

        # ipad,pad size
        frame_ipadx = "2"
        frame_ipady = "2"
        frame_padx = "2"
        frame_pady = "2"

        # -----------toptop_frame------------------SAVE, EXIT버튼 프레임 및 위젯
        self.toptop_frame = Frame(self.masterFrame, width=450, height=1)
        self.toptop_frame.pack()
       
        self.savebutton = Button(self.toptop_frame, text="SAVE", width=36,command=self.save)
        self.savebutton.pack(side=LEFT)
        self.exitbutton = Button(self.toptop_frame, text="EXIT", width=35, command=self.exit3)
        self.exitbutton.pack(side=RIGHT)

        # -------------top_frame----------------
        self.top_frame = Frame(self.masterFrame, width=450, height=500)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=YES)

        ##------------left_frame and right_frame in top_frame
        self.left_frame = Frame(self.top_frame, width=150, height=480)
        self.left_frame.pack(side=LEFT)

        self.right_frame = Frame(self.top_frame, width=380, height=480)
        self.right_frame.pack(side=RIGHT)

        ###---------------- paint_tool in left_frame 페인트 툴 프레임
        ####----------------------tool_frame 페인트 툴에 색(빨주노초파보)을 구현할 프레임
        self.tool_frame = Frame(self.left_frame, width=160, height=70)
        self.tool_frame.pack(side=TOP)
        # 빨
        self.red_color = Button(self.tool_frame, background="red", activebackground="red", borderwidth=0,
                                command=self.__color_menu_handler("red"))
        self.red_color.pack(side=LEFT, fill=BOTH)
        # 주
        self.orange_color = Button(self.tool_frame, background="orange", activebackground="orange", borderwidth=0,
                                   command=self.__color_menu_handler("orange"))
        self.orange_color.pack(side=LEFT, fill=BOTH)
        # 노
        self.yellow_color = Button(self.tool_frame, background="yellow", activebackground="yellow", borderwidth=0,
                                   command=self.__color_menu_handler("yellow"))
        self.yellow_color.pack(side=LEFT)
        # 초
        self.green_color = Button(self.tool_frame, background="green", activebackground="green", borderwidth=0,
                                  command=self.__color_menu_handler("green"))
        self.green_color.pack(side=LEFT)
        # 파
        self.blue_color = Button(self.tool_frame, background="blue", activebackground="blue", borderwidth=0,
                                 command=self.__color_menu_handler("blue"))
        self.blue_color.pack(side=LEFT)
        # 보
        self.purple_color = Button(self.tool_frame, background="purple", activebackground="purple", borderwidth=0,
                                   command=self.__color_menu_handler("purple"))
        self.purple_color.pack(side=LEFT)


        # 검정
        self.black_color = Button(self.tool_frame, background="black", activebackground="black", borderwidth=0,command=self.__color_menu_handler("black"))
        self.black_color.pack(side=LEFT, fill=BOTH)

        ####----------------------tool2_frame 페인트 툴에 색(검정), 지우기, 선,원,사각형을 구현할 프레
        self.tool2_frame = Frame(self.left_frame, width=160, height=70)
        self.tool2_frame.pack(side=TOP)

        # 지우기 버튼
        self.erase = Button(self.tool2_frame, text="erase", width=1, command=self.__shape_button_handler("erase"))
        self.erase.pack(side=LEFT, fill=BOTH)
        # 선 버튼
        self.option = Button(self.tool2_frame, text="/", width=1, command=self.__shape_button_handler("line"))
        self.option.pack(side=LEFT, fill=BOTH)
        # 원 버튼
        self.option1 = Button(self.tool2_frame, text="O", width=1, command=self.__shape_button_handler("oval"))
        self.option1.pack(side=LEFT, fill=BOTH)
        # 사각형 버튼
        self.option2 = Button(self.tool2_frame, text="ㅁ", width=1, command=self.__shape_button_handler("rectangle"))
        self.option2.pack(side=LEFT, fill=BOTH)
        # 펜버튼
        self.option3 = Button(self.tool2_frame, text="P", width=1, command=self.__shape_button_handler("pen"))
        self.option3.pack(side=LEFT, fill=BOTH)
     

        self.tool3_frame = Frame(self.left_frame, width=150, height=70)
        self.tool3_frame.pack(side=TOP)
        # 슬라이드 쇼 적용할 버튼
        self.boldbutton = Button(self.tool3_frame, text="Gallery",width=20, command=self.create_window)
        self.boldbutton.pack(side=LEFT)


        ####----------------------empty tool_frame 페인트 툴에 커스텀이모티콘 저장소  ()
        self.tool4_frame = Frame(self.left_frame, width=150, height=420)
        self.tool4_frame.pack(side=TOP)

        #### Label in right_top_frame 공지메시지, 그림판
        # ------------noticeLabel 공지메시지  띄우는 위젯
        self.noticeLable = Label(self.right_frame, width=54)
        self.noticeLable.configure(text="NOTICE", background="white")
        self.noticeLable.pack()

        ###----------------drawing_area in right_frame------------그림판 위젯
        self.__canvas = Canvas(self.right_frame, background="white", width=380, height=480)
        self.__canvas.pack()
        # self.__canvas.bind("<Button-1>", self.__get_click_coords)
        self.__canvas.bind("<Motion>", self.motion)
        self.__canvas.bind("<ButtonPress-1>", self.b1down)
        self.__canvas.bind("<ButtonRelease-1>", self.b1up)

        # ---------------bottom_frame---------사용자 리스트, 메시지 채팅창 프레임
        self.bottom_frame = Frame(self.masterFrame, height=190, width=400)
        self.bottom_frame.pack(side=TOP, fill=BOTH, expand=YES)

        ##left2_frame and right2_frame in bottom_frame
        # 사용자 리스트 프레임
        self.left2_frame = Frame(self.bottom_frame, height=190, width=170)
        self.left2_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # 메시지 채팅창 프레임
        self.right2_frame = Frame(self.bottom_frame, width=380, height=190)
        self.right2_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        ###--------------listbox in left2_frame 사용자 리스트 위젯
        self.listbox = Listbox(self.left2_frame, height=12, width=26, background="white")
        self.listbox.pack(side=LEFT)

        ###----------- right2_top_frame in right2 frame 메시지 채팅창 프레임 내의 메시지 로그창 프레임
        #### --------------right2_top_frame in right2_frame
        self.right2_top_frame = Frame(self.right2_frame, background="white", width=380, height=170)
        self.right2_top_frame.pack()

        #####----------------messageLog in right2_top_frame 메시지 로그창 프레임내 메시지 로그 , 메시지 스크롤바 위젯
        self.messageLog = Text(self.right2_top_frame)
        self.messageLog.insert(END, 'Enter "/notice message" to change the notice' + '\n')
        self.messageLog.tag_add("here", "1.0", "1.0+1lines")
        self.messageLog.tag_config("here", background="floral white")
        self.scrollbar = Scrollbar(self.right2_top_frame, command=self.messageLog.yview)
        self.messageLog.configure(width=60, height=11, state="disabled", yscrollcommand=self.scrollbar.set)
        self.messageLog.grid()
        self.messageLog.pack(side=LEFT, fill="both", expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=False)

        ####------------ right2_bottom_frame in right2_frame  메시지 채팅창 프레임 내 메시지를 입력하는 프레임
        self.right2_bottom_frame = Frame(self.right2_frame, background="white", width=380, height=30)
        self.right2_bottom_frame.pack()

        ##### textinput and button in right2_bottom_frame 메시지를 입력하는 프레임 내 메시지 입력 위젯과 메시지 보내기 버튼 위젯
        # ---------------textinput & button
        self.textinput = Text(self.right2_bottom_frame, width=50, height=1)
        self.textinput.pack(side=LEFT)
        self.sendButton = Button(self.right2_bottom_frame, width=6, height=1, text="Send", command=self.sendMessage)
        self.sendButton.pack()
        self.textinput.bind("<Key-Return>", self.buttonClicked_sub)
        self.sendButton.configure(background="yellow")
        self.sendButton.pack(side=RIGHT)

        self.__join_game()
        self.__get_data()

        self.master.protocol("WM_DELETE_WINDOW",
                             self.__close_window_handler)

        self.master.resizable(0, 0)  # the 0 make window's size constant

    # 메인앱의 생성자
    def __init__(self, Master, s, user_name, group_name, channelToServerFromArg):
        self.__user_name = user_name
        self.__group_name = group_name
        self.__channelToServer = channelToServerFromArg
        self.__current_color = INITIAL_COLOR
        self.__current_shape = INITIAL_SHAPE
        self.__online_friends = []
        self.__mouse_coordinates = []
        self.GUI_PART(Master)

    #
    def __data_to_list(self, decoded_data):
        """
        __get_data() 함수에서 쓰이는 함수
        서버에서 받은 바이트를 디코딩한 메세지를 배열의 배열로 바꿔주는 역할
        아주 큰 길이의 스트링을 작은 단위의 배열로 바꿔준다
        파라미터 decoded_data: 스트링이고 각 자료는 ;로 나눠져있고 다른종류의 자료는 \n로 구분
        """

        # 디코딩된자료길이에서부터 -1까지 1씩 빼면서 루프
        for index in range(len(decoded_data) - 1, -1, -1):
            if decoded_data[index] == '\n':
                filtered_decoded_data = decoded_data[:index]
                initial_list = filtered_decoded_data.split('\n')
                final_list = [message.split(';') for message in initial_list]

                return final_list

        return []

    def __join_friend(self, friend_name):
        """
        __get_data() 함수에서 쓰이는 함수.
        채팅방에 참가한 유저를 업데이트
        파라미터 friend_name: 새로운 유저이름을 담고있는 스트링
        """
        self.__online_friends.append(friend_name)
        self.listbox.insert(1, friend_name)


    def motion(self, event):
        if b1 == "down":
            global xold, yold
            if xold is not None and yold is not None:
                x1,y1 = event.x, event.y
                self.__mouse_coordinates.append((x1,y1))
                event.widget.create_line(xold, yold, x1,y1, smooth=TRUE)
            xold = event.x
            yold = event.y

    def b1down(self,event):
        global b1
        if self.__current_shape == 'pen':
            b1 = "down"
        else:
            point = (event.x, event.y)  # 마우스버튼을 눌렀을때의 좌표
            self.__mouse_coordinates.append(point)
            self.__draw_shape()

    def b1up(self, event):
        global b1, xold, yold
        b1 = "up"
        xold = None
        yold = None
        self.__draw_shape()  # 도형을 그린다


    def __draw_other_shapes(self, msg_lst):
        """
        __get_data() 함수에서 쓰이는 함수.
        서버에서 도형정보, 좌표정보, 색깔등의 정보를 받아와서 캔버스에 그린다
        파라미터 msg_lst: 배열의 배열. 각 배열은 사용자이름, 도형정보, 도형좌표, 색깔정보를 담고있다
        """
        user_name, shape, coords, color = msg_lst[MSG_CONTENT:]
        # print(color)  # 현재 그려진 도형의 색깔출력
        coords_tuple = tuple(coords.split(','))
        print(coords_tuple)

        if shape == "line":
            self.__canvas.create_line(coords_tuple, fill=color, width=3)
        elif shape == "rectangle":
            self.__canvas.create_rectangle(coords_tuple, fill=color)
        elif shape == "oval":
            self.__canvas.create_oval(coords_tuple, fill=color)
        elif shape == "triangle":
            self.__canvas.create_polygon(coords_tuple, fill=color)
        elif shape == "erase":
            self.__canvas.delete("all")
            self.coords_tuple = tuple("")
        elif shape == "pen":
            for i in range(2, len(coords_tuple), 2):
                x1,y1,x2,y2 = coords_tuple[i-2:i+2]
                one_tuple = tuple((x1,y1,x2,y2))
                self.__canvas.create_line(coords_tuple, fill=color, width=3)


    def __friend_leave(self, msg_list):
        """
        __get_data() 함수에서 쓰이는 함수.
        유져가 나가면 서버로부터 데이터를 받아 업데이트
        파라미터 msg_list: 스트링들의 배열
        """
        friend_name = msg_list[MSG_CONTENT]
        index = self.__online_friends.index(friend_name)
        self.__online_friends.remove(friend_name)
        self.listbox.delete(1)

    def __add_initial_friends(self, msg_lst):
        """
        __get_data() 함수에서 쓰이는 함수.
        새로운 유져가 접속하게되면 이미 접속되어 있는 유저들의 리스트들 받고 참가유저리스트 업데이트
        파라미터 msg_lst: 스트링들의 배열. 배열의 2번째 인덱스에 참가된 모든 유저들의 이름을 담고있다
        :return: None
        """
        users = msg_lst[1].split(',')

        for username in users:
            self.__online_friends.append(username)
            self.listbox.insert(1, username)

    def __error_msg(self, error_msg):
        """
       __get_data() 함수에서 쓰이는 함수.
        에러가 발생하면 새로운 윈도우를 띄운다
        파라미터 error_msg: 에러메세지를 나타내는 스트링
        :return: None
        """
        error_root = Toplevel()
        error_root.title("External error")
        frame1 = Frame(error_root, width=300, height=50)
        frame1.pack()
        help_label = Label(error_root, text=error_msg)
        help_label.pack()
        frame2 = Frame(error_root, width=300, height=50)
        frame2.pack()

    def __get_data(self):

        # 서버로 부터 데이터를 받아오는 메인펑션
        # 받은 자료를 읽을수 있는 데이터 리스트의 리스트로 변환
        # 어떤 종류의 메세지인지 알아내고 그에 맞는 함수에 전달해서 GUI를 업데이트 한다.
        # return: 없음

        decoded_data = ''

        """
            다중입출력을 위해 select사용
            select(rlist, wlist, xlist, timeout) -> (rlist, wlist, xlist)
            파일디스크립터들이 입출력을 위한 준비가 완료될때까지 기다린다
            rlist -- 읽을준비가 완료될때까지 기다린다
            wlist -- 쓰기준비과 완료될때까지 기다린다
            xlist -- 특별한 상황에만 쓰인다
            timeout -- 이 시간을 넘기면 타임아웃
        """
        readable_sockets = select([self.__channelToServer], [], [], 0.01)[READ_SOCK]

        while len(readable_sockets) > 0:  # 받을 자료가 있다면
            for sock in readable_sockets:
                if sock == self.__channelToServer:
                    coded_data = sock.recv(READ_LIMIT)  # recv는 바이트로 받기때문에
                    decoded_data += coded_data.decode()  # 디코드해서 스트링으로 바꿔준다
                    readable_sockets = select([self.__channelToServer], [], [], 0.01)[READ_SOCK]

        data_list = self.__data_to_list(decoded_data)

        # 각 메세지에 맞는 함수를 부른다
        for msg_lst in data_list:
            if msg_lst[MSG_TYPE] == "join":
                self.__join_friend(msg_lst[MSG_CONTENT])
            elif msg_lst[MSG_TYPE] == "shape":
                self.__draw_other_shapes(msg_lst)
            elif msg_lst[MSG_TYPE] == "leave":
                self.__friend_leave(msg_lst)
            elif msg_lst[MSG_TYPE] == "users":
                self.__add_initial_friends(msg_lst)
            elif msg_lst[MSG_TYPE] == "error":
                self.__error_msg(msg_lst[MSG_CONTENT])

        self.master.after(100, self.__get_data)  # 100ms 마다 호출

    def __join_game(self):
        """
        채팅방에 참여한다는 메세지를 보내는 함수
        서버에게 유저네임을 보낸다.
        """
        join_msg = "join;" + self.__user_name + ';' + self.__group_name + '\n'
        self.__channelToServer.sendall(bytes(join_msg, encoding='utf8'))

    def __color_menu_handler(self, value):
        """
        색깔을 고르는 이벤트가 발생했을때 처리하는 함수
        파라미터 value: 유저가 고른 색깔
        """

        def set_color():
            # 현재 색깔변수를 유저가 고른 색깔로 변경한다
            self.__current_color = value
            print("color")

            # 유져가 색깔을 고를때 그전에 클릭했던것을 저장해놓은것을 지워버리기로 결정
            self.__mouse_coordinates = []

        return set_color

    def __shape_button_handler(self, shape):
        """
        도형종류를 정하는 이벤트가 발생하면 처리하는 함수
        파라미터 shape: 도형의 종류
        """

        def determine_shape():
            """
            도형의 종류를 결정한다.
            """
            # 현재 도형을 입력받은 도형으로 변경
            self.__current_shape = shape

            # 유저가 새로운 도형을 선택할경우 이전에 캔버스에 클릭해놓은것을 저장해놓은것을 지움
            self.__mouse_coordinates = []

        return determine_shape

    def __get_click_coords(self, event):
        """
        마우스를 클릭하면 좌표를 저장하는 함수
        파라미터 event: 마우스 클릭 이벤트
        """
        print('in click')

        point = (event.x, event.y)  # 마우스버튼을 눌렀을때의 좌표
        self.__mouse_coordinates.append(point)
        self.__draw_shape()  # 도형을 그린다

    def __list_to_tuple(self, lst):
        """
        이 함수는 마우스 클릭 x,y 좌표 튜플 리스트를 받는다
        튜플배열을 하나의 튜플로 바꾼다
        파라미터 lst: 튜플들로 이루어진 배열
                    예) [(x1,y1),(x2,y2),...]
        반환하는것: 하나의 튜플, 파라미터로 받은 리스트의 모든 좌표를 담고있다
        """

        answer_list = []
        for tup in lst:
            answer_list.append(tup[X_COORD])
            answer_list.append(tup[Y_COORD])
        return tuple(answer_list)

    def __tup_string(self, mouse_coordinates):
        """
        __list_to_tuple의해 생성된 마우스 좌표 튜플을 받아서
        스트링으로 바꾼다
        파라미터: self.__list_to_tuple 의해 생성된 마우스좌표 튜플.
            (x1, y1, x2, y2, ...) 식으로 생성되어있다
        반환값: 스트링. 마우스 클릭 좌표를 담고있고 콤마로 구분되어 있다
        예) 'x1,y1,x2,y2,...'
        """
        # parentheses제거
        temp_string = str(mouse_coordinates)[1:-1]

        # 콤마뒤 스페이스 제거
        final_string = temp_string.replace(" ", "")

        return final_string

    def __draw_shape(self):
        """
        도형을 그리는 함수
        충분한 마우스 클릭이 있었는지 확인후
        현재 고른 도형에 맞는 도형을 그리라는 메세지를 서버로 보낸다
        """
        global b1

        mouse_coordinates = self.__list_to_tuple(self.__mouse_coordinates)
        msg_coords = self.__tup_string(mouse_coordinates)
        # 도형메세지를 생성하는 부분 ;로 구분이 되어있고 도형종류, 색갈등의 정보를 담는 스트링
        shape_message = "shape" + ';' + self.__current_shape + ';' + \
                        msg_coords + ';' + self.__current_color + '\n'

        if self.__current_shape == "pen":
             if b1 == "up":
                self.__mouse_coordinates = []  # 마우스좌표 초기화
                self.__channelToServer.sendall(bytes(shape_message, encoding='utf8')) 

        elif len(self.__mouse_coordinates) == OVAL_LINE_RECT_COORDS_AMOUNT :

            self.__mouse_coordinates = []  # 마우스좌표 초기화

            # 서버로 전송
            self.__channelToServer.sendall(bytes(shape_message, encoding='utf8'))


        elif self.__current_shape == "erase":
            self.__canvas.delete("all")
            self.__channelToServer.sendall(bytes(shape_message, encoding='utf8'))


    def __close_window_handler(self):
        """
        윈도우 종료이벤트를 처리하는 함수
        """
        # 나간다는 메세지를 서버에게 전송한다
        self.__channelToServer.sendall(bytes(LEAVE_MSG, encoding='utf8'))
        self.master.quit()  # tkinter gui창을 종료한다

    # 공지글설정
    def notice_change(self, msgcontent):
        str1, str2 = msgcontent.split(': ')
        str3 = str2[:8]
        str4 = str2[8:]
        length = len(str4)
        str5 = str4[:length - 1]
        if str3 == '/notice ':
            self.noticeLable.configure(text=str5)

    # 메시지 출력
    def logRefresh(self, data):

        # 바이너리디코드
        data = str(data, 'utf8')

        # 포맷제외하고 내용만만들기
        arr = data.split('\'')
        user = arr[1]
        txt = arr[3].split('\\')[0]

        # user_length = len(user)


        msgcontent = user + " : " + txt + '\n'
        data2 = msgcontent.encode()

        self.messageLog.configure(state="normal")
        self.messageLog.insert(END, msgcontent)
        self.messageLog.configure(state="disabled")
        self.messageLog.see(END)
        self.notice_change(msgcontent)

    # 메시지 입력

    def buttonClicked_sub(self, event):
        message = self.textinput.get(1.0, 'end-1c')
        if message[0] == '\n' : message = message[1:] #\n이 다음메세지에 딸려오는것방지
        mySocket.send(message.encode('utf-8'))
        self.textinput.delete(1.0, END)

    def sendMessage(self):
        message = self.textinput.get(1.0, END)
        if message[0] == '\n' : message = message[1:] #\n이 다음메세지에 딸려오는것방지
        mySocket.send(message.encode('utf-8'))
        self.textinput.delete(1.0, END)


def handler(sock):
    print("Thread start!")
    while 1:
        try:
            data = sock.recv(1024)
        except timeout:
            continue
        else:
            print(data)
            main.logRefresh(data)


root = Tk()
entrance = window1(root)
root.title("IP")
root.mainloop()

try:
    print(IP + "로 접속 시도")
    mySocket.connect((IP, int(serverPort)))
    mySocket.settimeout(5.1)
    # s.send(Name)
    mySocket.send(Name.encode('utf-8'))
    print(Name + "으로 접속!")
    print("접속 완료")
except:
    print("접속 실패")
    traceback.print_exc()
    sys.exit()

thread1 = Thread(target=handler, args=(mySocket,)).start()

# 서버와의 연결:
# 2개의 연결이 있는데 아래가 페인트서버와연결 포트는 5678사용
channelToServer = socket.socket()
channelToServer.connect((IP, int(5678)))

# 채팅화면
root2 = Tk()
main = mainapp(root2, mySocket, Name, 'demo', channelToServer)
root2.title("main")
root2.mainloop()

channelToServer.close()
mySocket.close()  
