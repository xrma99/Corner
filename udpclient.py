import socket
import threading
from time import ctime,sleep


class user:
    '''
    hostname：电脑名字
    addr:ip地址
    port：端口号，默认12345
    s:建立的socket
    head:参加的corner链表头
    length:参加的Corner数量
    '''
    length=0
    head=None
    s=None
    def __init__(self):
        self.hostname = socket.gethostname()
        self.addr=socket.gethostbyname(self.hostname)  
        self.port=6000#默认端口号都使用12345
    def __repr__(self):
        #print
        return str("ipaddress:"+self.addr+"\n"+"port:"+str(self.port))
    
    
    def sendmessage(self):    
        self.s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
        while 1:
            tempmessage=input("input command>>>")
                
            #在Server端进行操作
            message=tempmessage.encode('utf-8')#String->Bytes
            self.s.sendto(message,('127.0.0.1',12345))
            
            tempResponse,serverAddress=self.s.recvfrom(2048)
            Response=bytes.decode(tempResponse)#Bytes->String
            print (Response)
            
            while(Response[0]=="*"):#判断是否是信息
                tempResponse,serverAddress=self.s.recvfrom(2048)
                Response=bytes.decode(tempResponse)#Bytes->String
                print (Response)
                
            #leave指令较为特殊
            if(tempmessage=="/leave"):#leave指令，关闭客户端这边的socket
                return
            if(Response=="404"):
                print("Sorry, the server is closed by manager\n")
                return
            
    def closeconnection(self):
        if(self.s==None):
            print("No connection")
            return
        print("close at",ctime())
        self.s.close()
        self.s=None




if __name__ == '__main__':
    user1 = user() 
    user1.sendmessage()    
    user1.closeconnection()
