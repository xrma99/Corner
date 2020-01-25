import socket
import threading
from time import ctime,sleep


class user:
    '''
    hostname����������
    addr:ip��ַ
    port���˿ںţ�Ĭ��12345
    s:������socket
    head:�μӵ�corner����ͷ
    length:�μӵ�Corner����
    '''
    length=0
    head=None
    s=None
    def __init__(self):
        self.hostname = socket.gethostname()
        self.addr=socket.gethostbyname(self.hostname)  
        self.port=6000#Ĭ�϶˿ںŶ�ʹ��12345
    def __repr__(self):
        #print
        return str("ipaddress:"+self.addr+"\n"+"port:"+str(self.port))
    
    
    def sendmessage(self):    
        self.s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
        while 1:
            tempmessage=input("input command>>>")
                
            #��Server�˽��в���
            message=tempmessage.encode('utf-8')#String->Bytes
            self.s.sendto(message,('127.0.0.1',12345))
            
            tempResponse,serverAddress=self.s.recvfrom(2048)
            Response=bytes.decode(tempResponse)#Bytes->String
            print (Response)
            
            while(Response[0]=="*"):#�ж��Ƿ�����Ϣ
                tempResponse,serverAddress=self.s.recvfrom(2048)
                Response=bytes.decode(tempResponse)#Bytes->String
                print (Response)
                
            #leaveָ���Ϊ����
            if(tempmessage=="/leave"):#leaveָ��رտͻ�����ߵ�socket
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
