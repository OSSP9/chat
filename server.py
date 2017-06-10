# -*- coding: utf-8 -*-

import os
import sys
from socket import *
from socket import error as socket_error
from threading import *
import socketserver
from queue import Queue,Empty
from threading import Thread
import re
import traceback


# 소켓이 모든 IP주소의 연결요청을 Accept하게 호스트 어드레스를 비워둠
HOST = ''
PORT = 7382

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

READLIMIT = 1024
MAXNAMELEN = 20
MAXMSGLEN = 200
COORDBOUND = 10000


REG,UNREG = -1,-2

##ERRORS:
ERR_LONGMESSAGE = 1
ERR_ALREADYJOINED = 2
ERR_NOTJOINED = 3
ERR_NOSUCHGROUP = 4
ERR_INVALIDNAME = 5

MSGDELIM = b'\n'
DELIM = b';'
FIELDSEP = b','

class Service(socketserver.BaseRequestHandler):
    def handle(self):
        self.closed = False
        self.queue = Queue()
        self.controller = controller
        try:
            self.sender = Thread(target=self._datasender)
            self.sender.start()
            self.controller.register(self)
            while True:
                data = self.request.recv(READLIMIT)
                if not data:
                    break
                self.controller.put((id(self),data))
        finally:
            self.close()

    def _datasender(self):
        try:
            while not self.closed:
                self.request.sendall(self.queue.get())
        except OSError:
            pass

    def put(self, item, block=True, timeout=None):
        self.queue.put(item, block=True, timeout=None)

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.controller.unregister(self)

        self.request.close()

class Controller:
    def __init__(self, workerclass):
        self.queue = Queue()
        self.gen = self._datareceiver()
        self.worker = workerclass(self)
        self.connections = {}
        self.buffers = {}

    def _datareceiver(self):
        while True:
            yield self.queue.get()

    def send(self, cid, item, block=True, timeout=None):
        self.connections[cid].put(item+MSGDELIM, block=True, timeout=None)

    def put(self, item, block=True, timeout=None):
        self.queue.put(item, block=True, timeout=None)

    def register(self, conn):
        self.queue.put((REG,conn))

    def unregister(self, conn):
        self.queue.put((UNREG,id(conn)))

    def _register(self,conn):
        if id(conn) not in self.connections:
            self.connections[id(conn)] = conn
            print('CON',conn.client_address)
            self.buffers[id(conn)] = b''

    def _unregister(self,cid):
        try:
            print('DIS',self.connections[cid].client_address)
            del self.connections[cid]
            del self.buffers[cid]
            self.worker.leave(cid)
        except KeyError:
            pass

    def run(self): #The work
        for cid,data in self._datareceiver():
            if cid==REG: 
                #print('REG')
                self._register(data)
            elif cid==UNREG:
                #print('UNREG')
                self._unregister(data)
            elif cid not in self.connections:
                pass
            else:
                data = self.buffers[cid]+data
                while MSGDELIM in data:
                    self.worker.process(cid,data[:data.index(MSGDELIM)])
                    data = data[data.index(MSGDELIM)+1:]
                self.buffers[cid] = data
                if len(data) > MAXMSGLEN:
                    self.worker.error(cid,ERR_LONGMESSAGE)
                    self.buffers[cid] = b''

class Worker:
    def __init__(self, controller):
        self.controller = controller
        self.clientnames = {}
        self.clientgroups = {}
        self.groups = {}
        self.groupcanvas = {}

    def process(self,cid,msg):
        try:
            elems = msg.split(DELIM)
            if elems[0]==b'join':
                assert(len(elems)==3)
                uname,gname = elems[1:]
                self.join(cid,uname,gname)
            elif elems[0]==b'shape':
                assert(len(elems)==4)
                stype,args,color = elems[1:]
                self.shape(cid,stype,args,color)
            elif elems[0]==b'leave':
                assert(len(elems)==1)
                self.leave(cid)
            elif elems[0]==b'who':
                assert(1<=len(elems)<=2)
                if len(elems)==1:
                    self.who(cid)
                else:
                    gname = elems[1]
                    self.who(cid,gname)
            elif elems[0]==b'groups':
                assert(len(elems)==1)
                self.grouplist(cid)
        except Exception:
            traceback.print_exc()

    def join(self,cid,uname,gname):
        assert(checkname(uname) and checkname(gname))
        if cid in self.clientgroups:
            self.error(cid, ERR_ALREADYJOINED)
            return
        if gname not in self.groups:
            self.groups[gname] = set()
            self.groupcanvas[gname] = []
        for tid in self.groups[gname]:
            self.controller.send(tid,DELIM.join((b'join',uname)))
            self.groupcanvas[gname] = [MSGDELIM.join(self.groupcanvas[gname])]
            self.controller.send(cid,self.groupcanvas[gname][0])
            #for msg in self.groupcanvas[gname]:
            #    self.controller.send(cid,msg)
        self.groups[gname].add(cid)
        self.clientnames[cid] = uname
        self.clientgroups[cid] = gname
        self.who(cid)

    def shape(self,cid,stype,args,color):
        if cid not in self.clientgroups:
            self.error(cid, ERR_NOTJOINED)
            return
        gname = self.clientgroups[cid]
        uname = self.clientnames[cid]
        #assert(checkcolor(color) and checkshapeargs(stype,args))
        # TODO: Possibly normalize arg ints
        msg = DELIM.join((b'shape',uname,stype,args,color))
        for tid in self.groups[gname]:
            self.controller.send(tid,msg)
        self.groupcanvas[gname].append(msg)

    def leave(self,cid):
        #print('LEAVE')
        if cid not in self.clientgroups:
            return
        gname = self.clientgroups[cid]
        uname = self.clientnames[cid]
        self.groups[gname].remove(cid)
        for tid in self.groups[gname]:
            self.controller.send(tid,DELIM.join((b'leave',uname)))
        del self.clientnames[cid]
        del self.clientgroups[cid]
        if not self.groups[gname]:
            del self.groups[gname]
            del self.groupcanvas[gname]

    def who(self,cid,gname=None):
        if cid not in self.clientgroups and gname is None:
            self.error(cid, ERR_NOTJOINED)
            return
        if gname is None:
            gname = self.clientgroups[cid]
        if gname not in self.groups:
            self.error(cid, ERR_NOSUCHGROUP)
            return
        self.controller.send(cid,DELIM.join((b'users',FIELDSEP.join(self.clientnames[n] for n in self.groups[gname]))))

    def grouplist(self,cid):
        self.controller.send(cid,DELIM.join((b'groups',FIELDSEP.join(self.groups))))

    def error(self, cid, err):
        messages = {0:b'',
                    ERR_LONGMESSAGE:b'Message too long',
                    ERR_ALREADYJOINED:b'Already joined group',
                    ERR_NOTJOINED:b'Not member of any group',
                    ERR_NOSUCHGROUP:b'Group does not exist',
                    ERR_INVALIDNAME:b'Illegal name',
                }
        self.controller.send(cid,DELIM.join((b'error',messages[err])))

def checkname(name):
    return len(name)<=MAXNAMELEN and bool(re.match(b'[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_]+',name))

def checkshapeargs(stype,args):
    #print(stype,args)
    params = [int(s) for s in args.split(FIELDSEP)]
    length = len(params)
    if max(params)>COORDBOUND or min(params)<-COORDBOUND:
        return False
    if stype == b'triangle':
        return length==6
    if stype in [b'line',b'rectangle',b'oval']:
        return length==4
    return False

def checkcolor(color):
    return color in [b'blue',b'red',b'green',b'yellow',b'black',b'violet',b'orange']

class ThreadAccept(Thread):                     #사용자 접속을 받는 스레드 클래스
                                                #Thread class 를 상속한다.
    shutdown = False
    def __init__(self, socket, socketList):     #생성자
        Thread.__init__(self)                   #쓰레드 초기화
        self.socket = socket
        self.socketList = socketList
        self.childThreads = []
                
    def run(self):
        self.socket.settimeout(0.1)                 # 100ms timeout을 줄것
        while ThreadAccept.shutdown == False:
            try:
                                                    #듀플로 주소와 소켓을 얻어옴
                connection, address = self.socket.accept()        
            except timeout:
                continue
            else:
                name = connection.recv(1024) #이름
                self.socketList.append((connection, address,name))           #리스트에 추가
                print(connection)
                print("[connection ", address," ]: ",name)    #메세지 출력
                handler = ThreadHandler(connection, address,name, socketList)
                handler.start()
                self.childThreads.append(handler)
              #  self.sendmsg(name) #메시지 출력

    def joinChildThreads(self):
        for thread in self.childThreads:
            thread.join()
     
class ThreadHandler(Thread):
    shutdown = False
    
    def __init__(self, socket, addr,name, socketList):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.name = name
        self.socketList = socketList
        
    def run(self):
        self.socket.settimeout(0.1)                # 100ms timeout을 줄것
        while ThreadHandler.shutdown == False:
            try:
                data = self.socket.recv(1024)          #일단 가져온다.
            except timeout:
                continue
            except Exception as e:
                print(e)
                break                
            else:        
                data = data.decode('utf-8')
                if not data:                    #데이터가 없다면
                    continue                    #컨티뉴
                
                if data == '/disconnected':  # 종료메세지라면
                    x = (self.socket,self.addr,self.name)
                    #self.socketList.remove((x))   #목록에서 지우고
                    self.socket.shutdown(SHUT_RDWR)                #소켓 닫기
                    self.socket = None
                    print(self.name, " disconnected")
                    break
                    
               
                else:
                    data = data.encode('utf-8')
                    self.sendMsgToAll(data)   
        #self.socket.shutdown(SHUT_RDWR)
        
    def sendMsgToAll(self, msg):        #리스트에 있는 모든 사람에게 메세지 전송
        for socket, addr, name in self.socketList:
            print(msg)
            data = str(self.name) + ' : ' + str(msg)    #메세지와 주소 결합
            socket.send(data.encode('utf-8'))                   #전송


socketList = []                                 #소켓 리스트 작성
serverSocket = socket(AF_INET, SOCK_STREAM)     #소켓 할당
serverSocket.bind((HOST, PORT))                 #IP, 포트 바인딩
serverSocket.listen(5)                          # 리슨상태
print("Server Start")
print(HOST)
print(PORT)
acceptor = ThreadAccept(serverSocket, socketList)           #스레드 객체 생성
acceptor.start()                                #스레드 시작

ThreadedTCPServer.allow_reuse_address = True
global controller
controller = Controller(Worker)
import sys
port = 5678 if len(sys.argv)==1 else int(sys.argv[1])
t = ThreadedTCPServer(('',port), Service)
Thread(target=t.serve_forever).start()
Thread(target=controller.run).start()

while 1:                                        #커멘드라인 루프
    cmd = input('>>')
    if cmd == 'x':                              #종료
        #스레드는 어떻게 종료?;;
        #객체 삭제 X, __stop() X, 
        ThreadHandler.shutdown = True           # thread들에게 종료 신호를 보낸다.
        ThreadAccept.shutdown = True
        acceptor.joinChildThreads()
        acceptor.join()                         # acceptor thread가 끝날때 까지 기다린다.
        break
print("Server Stop" )

