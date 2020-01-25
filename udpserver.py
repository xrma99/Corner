import socket
import datetime 
import hashlib #����ת��bytes��string��
import threading
from time import ctime,sleep


#��Ŵ�1��ʼ����

class userNode:
    '''
    name
    addr  
    num
    _next: ������һ���ڵ����
    '''
    num=0 #�û����
    def __init__(self,n,address,pnext=None):
        self.name=n
        self.addr=address
        self._next = pnext

    def __repr__(self):
        '''
        ��������userNode���ַ������
        printΪ���data
        '''
        if (self.num==0):#��û�м���Ӣ���
            return str("username:"+self.name+"\nip:"+str(self.addr)+"\n")
        else:#�û��Ѿ�����Ӣ���
            return str("NO."+str(self.num)+":username:"+self.name+"\nip:"+str(self.addr)+"\n")
        
    def adduser(self,newuser):
        if(self!=userheadmxr):
            return #ֻ��userheadmxr�����Ȩ�޿��Լӣ�userheadmxr�����ϴ󣡱���Ƕ�һ�޶���0��
        item=newuser
        node=userheadmxr
        while node._next:
            node=node._next
        item.num=node.num+1
        node._next=item
        
    def searchname(self,n):
        if(self!=userheadmxr):
            return None#ֻ��userheadmxr�����Ȩ�޿�����Ѱ��userheadmxr�����ϴ󣡱���Ƕ�һ�޶���0��
        node=userheadmxr
        while node:
            if(node.name==n):
                return node
            node=node._next
            
        return None
    
    def isregister(self,addr):#ͨ�����addr���Ƿ����޽���������
        if(self!=userheadmxr):
            return None#ֻ��userheadmxr�����Ȩ�޿�����Ѱ��userheadmxr�����ϴ󣡱���Ƕ�һ�޶���0��
        node=userheadmxr
        while node:
            if(node.addr==addr):
                return node
            node=node._next
            
        return None
    
    def deleteuser(self,n):
        if(n=="mxr"):
            return#server manager can't be deleted
        if(self!=userheadmxr):
            return#ֻ��userheadmxr�����Ȩ�޿�����Ѱ��userheadmxr�����ϴ󣡱���Ƕ�һ�޶���0��
        prev=userheadmxr
        node=userheadmxr._next
        while node:
            if(node.name==n):
                prev._next=node._next
                break
            prev=node
            node=node._next
        
        node=prev._next
        while node:
            node.num-=1
            node=node._next
        
        
#######################################################################################################################    
    
class corner:
    name="corner"#corner name
    num=0 #corner num
    length=0 #user ������
    head=None #user ����ͷ
    
    def __init__(self,n,pnext=None):
        self.name = n
        self._next = pnext
        
    def __repr__(self):
        '''
        ��������corner���ַ����
        '''
        return str("NO."+str(self.num)+":cornername:"+self.name+"\n")
   
    def adduser(self, newuser):
        item = newuser

        if not self.head:#cornerΪ��
            self.head = item
            self.length += 1
            item.num=1
            return 1#�ɹ�����

        else:
            node = self.head
            while node._next:#���û��ӵ����һ���ڵ�ĺ���
                if(node.name==item.name):#����û��Ѿ������Ӣ���������
                    return 0
                node = node._next
            if(node.name==item.name):#����û��Ѿ������Ӣ��������ˣ�������һ��usernode
                return 0
            self.length += 1
            item.num=self.length
            node._next = item
            
        return 1
    
    def deleteuser(self, n):#����user��name��ɾ���û�
        if(self.length==0):#Empty corner
            print ("this corner has no user.")
            return 0

        node = self.head
        if(node.name==n):#delete head
            self.head = self.head._next
            self.length -= 1
            node=self.head
            while node:
                node.num-=1
                node=node._next
            return 1

        #prevΪ����ǰ���ڵ�,nodeΪ���浱ǰ�ڵ�
        #ɾ��һ���ڵ�֮��������ȼ�һ����Ҫ�Ѻ����û��ı����ǰŲ1

        flag=0
        node=self.head._next#�Ѿ������ͷ������Ҫɾ���Ķ���
        prev = self.head
        while node:
            if(node.name==n):
                flag=1
                prev._next = node._next
                self.length -= 1
                break
            prev = node
            node = node._next
        
        node=prev._next
        while node:
            node.num-=1
            node=node._next
            
        return flag


    def listusers(self):
        if(self.length==0):
            res=self.name+": empty corner, no user.\n"
            return
            
        res="Users of "+self.name+":\n"          
        node=self.head
        while node:
            res=res+"NO."+str(node.num)+":username:"+node.name+"\n"
            node=node._next
        return res
    
    
            
#######################################################################################################################        
            

class server:
    '''
    server����Ԫ�أ�
    HOST,PORT,password
    length,head
    s:socket,��Ҫ�о������
    '''
    length=0 #corner������
    head=None #corner����ͷ
    password="16307130347"
    PORT=12345
    HOST='127.0.0.1'
    s=None
        
    def kickoutuser(self,n):
        node=self.head
        while node:
            node.deleteuser(n)
            node=node._next
            
        userheadmxr.deleteuser(n)#�ڹ���Ա����ɾ����¼
            
        

    def opencorner(self, newcorner):
        item = newcorner

        if not self.head:#û��corner
            self.head = item
            self.length += 1
            item.num=1
            return 1

        else:
            node = self.head
            while node._next:#��corner�ӵ����һ���ڵ�ĺ���
                if(node.name==newcorner.name):
                    return 0#���corner�Ѿ����ڣ��޷�add
                node = node._next
                
            if(node.name==newcorner.name):
                return 0#���corner�Ѿ����ڣ��޷�add
            node._next = item
            self.length += 1
            item.num=self.length
            return 1
    
    def closecorner(self,n):#nΪcorner��name
        if (self.length==0):#��server
            print ("no corner.")
            return 0

        node = self.head        
        if (node.name==n):#delete head
            self.head = self.head._next
            self.length -= 1
            node=self.head
            while node:
                node.num-=1
                node=node._next
            return 1
        #ɾ��һ���ڵ�֮��������ȼ�һ����Ҫ�Ѻ����û��ı����ǰŲ1
        #prevΪ����ǰ���ڵ�,nodeΪ���浱ǰ�ڵ�

        node = self.head._next
        prev = self.head
        flag=0
        while node:
            if(node.name==n):
                prev._next = node._next
                self.length -= 1
                flag=1
                break
            prev = node
            node = node._next
        
        node=prev._next
        while node:
            node.num-=1
            node=node._next
            
        return flag
              
    def listcorners(self):
        if(self.length==0):
            res="no corner,please create one.\n"
            return res
        res="Corners:\n"    
        #print("Corners:\n")         
        node=self.head
        while node:
            res=res+"NO."+str(node.num)+":cornername:"+node.name+"\n"
            node=node._next
            
        return res
    
    def findcorner(self,n):#����name����corner������
        node=self.head
        while node:
            if(node.name==n):
                return node
            node=node._next
        return None

        
    def listenmessage(self):#����ָ��
        if(self.s==None):
            print("No socket established,error!")
            return
        useflag=0#��¼���IP��ַ�Ƿ��ǵ�һ�η���Ϣ��server���������ô�����µ�user
        flag=1
        while 1:#��ν�����Ϣ
            if(self.s==None):
                return
            data,addr=self.s.recvfrom(2048) #ֻ�᷵��data,�յ������ݸ�ʽ��b'cmd',��Bytes����
            cmd=bytes.decode(data)#Bytes->String
            thisuser=userheadmxr.isregister(addr)
            if(thisuser==None):#registerע��
                words=cmd.split()
                if(words[0]=="/name"):
                    l=len(words)
                    
                    if(l==1):#���ֲ���Ϊ��
                        thisuser=userNode(" ",addr)
                        restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed,Please register again\n")
                        res=restemp.encode('utf-8')#String->Bytes
                        self.s.sendto(res,thisuser.addr)#����ָ��
                        
                    else:
                        n=" ".join(words[1:l])#�ϲ�String������String���м��Կո�������ȡ�û���
                        thisuser=userNode(n,addr)
                        if(userheadmxr.searchname(n)!=None):#�Ѿ����û�ע�����������                       
                            restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed.This name has been taken\n")
                            res=restemp.encode('utf-8')#String->Bytes
                            self.s.sendto(res,thisuser.addr)#����ָ��
                        
                        else:
                            userheadmxr.adduser(thisuser)
                            print(str(thisuser.addr)+" enter at %s \n" %ctime())#��¼�û�ʹ�ü�¼
                            restemp="#status:Succeed#\n"+self.makemessage(cmd,self,thisuser,"Register successfully\n")
                            res=restemp.encode('utf-8')#String->Bytes
                            self.s.sendto(res,thisuser.addr)#����ָ��
                else:
                    thisuser=userNode("Unverified User",addr)
                    restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed,Please register again\n")
                    res=restemp.encode('utf-8')#String->Bytes
                    self.s.sendto(res,thisuser.addr)#����ָ��
            
                    
            else:
                self.handlemessage(cmd,thisuser)#�Ƿ�Ӧ��ֹͣ����ָ��
            
        
    
    def handlemessage(self,cmd,user):#��������ָ��
        #�ȼٶ�ȫ�����ǻ�ָ��
        restemp1="Wrong command format\n"
        restemp2="#status:Failed#\n"+self.makemessage(cmd,self,user,restemp1)
    
        words=cmd.split()
    
        if(words[0]=="mxr"):#it is command from server manager
            if(words[1]==serv.password):#verify identification
                print("Server logging......\n"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))#��¼server��¼ʱ��
                l=len(words)
                n=" ".join(words[3:l])
                if(words[2]=="kickout"):           
                    self.kickoutuser(n)
                    restemp2=self.makemessage(cmd,self,user,("Manager mxr kickout %s\n"%n))
                if(words[2]=="opencorner"):
                    temp=corner(n)
                    if(self.opencorner(temp)==1):#�ɹ�open��һ��corner
                        restemp2=self.makemessage(cmd,self,user,("Manager mxr opencorner %s\n"%n))
                    else:
                        restemp2=self.makemessage(cmd,self,user,("Corner %s has already existed.\n"%n))
                if(words[2]=="closecorner"):
                    if(self.closecorner(n)==1):#�ɹ�close��һ��corner
                        restemp2=self.makemessage(cmd,self,user,("Manager mxr closecorner %s\n"%n))
                    else:
                        restemp2=self.makemessage(cmd,self,user,("Corner %s doesn't exist.\n"%n))
                        
                if(words[2]=="terminate"):#�ر�socket
                    restemp2=self.makemessage(cmd,self,user,("Terminate the Server.\n"))
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#����ָ��
                    
                    #֪ͨ�����û��������Ѿ��ر�
                    restemp2="404"
                    res=restemp2.encode('utf-8')#String->Bytes
                    node=userheadmxr._next
                    while node:
                        self.s.sendto(res,node.addr)#����ָ��
                        node=node._next
                    
                    self.closesocket()
                    return 0
            
            
        if(words[0][0]=='/'):#it is command from client user
            l=len(words[0])
            if(l==1):#����ֻ����/�����
                res=restemp2.encode('utf-8')#String->Bytes
                self.s.sendto(res,user.addr)#����ָ��
                return 1
            subcmd=words[0][1:l]#��ȡcommand���������,��һλ��������l��ȡ����ȡ�±�Ϊl-1���ַ�

            if(subcmd=="corners"):#�г����п�ͨ�������
                print(str(user.addr)+"listcorners at %s \n" %ctime())#��¼�û�ʹ�ü�¼
                restemp1=serv.listcorners()
                restemp2=self.makemessage(cmd,self,user,restemp1)              
                
            if(subcmd=="listusers"):#�г���ǰ��������ǵ������û�
                l=len(words)
                n=" ".join(words[1:l])#�ϲ�String������String���м��Կո���
                print(str(user.addr)+"listusers at corner %s at %s \n" %(n,ctime()))#��¼�û�ʹ�ü�¼
                
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                else:
                    restemp1=cor.listusers()
                        
                restemp2=self.makemessage(cmd,cor,user,restemp1) 
                
            if(subcmd=="join"):#Join corner username
                l=len(words)
                n=" ".join(words[1:l])#�ϲ�String������String���м��Կո���
                print(str(user.addr)+"joins the corner %s at %s \n" %(n,ctime()))#��¼�û�ʹ�ü�¼
                
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                    restemp2=self.makemessage(cmd,cor,user,restemp1)
                else:#����corner
                    temp=userNode(user.name,user.addr)
                    if(cor.adduser(temp)==1):
                        restemp2=self.makemessage(cmd,cor,user,("User %s joins %s\n"%(user.name,cor.name)))
                    else:
                        restemp2=self.makemessage(cmd,cor,user,("User %s has already joined %s\n"%(user.name,cor.name)))
                         
                
            if(subcmd=="exit"):#exit a corner
                l=len(words)
                n=" ".join(words[1:l])#�ϲ�String������String���м��Կո���
                              
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                    restemp2=self.makemessage(cmd,cor,user,restemp1) 
                else:#�˳�corner
                    if(cor.deleteuser(user.name)==1):#�ɹ��˳���Ӧcorner
                        print(str(user.addr)+"exits the corner %s at %s \n" %(n,ctime()))#��¼�û�ʹ�ü�¼
                        restemp2=self.makemessage(cmd,cor,user,("User %s exits %s\n"%(user.name,cor.name)))
                    else:
                        restemp2=self.makemessage(cmd,cor,user,("User %s is not in %s\n"%(user.name,cor.name)))
                
                
                
            if(subcmd=="msg"):#��������з���һ����Ϣ����������������û��յ�������ֻ�е��ʳ���Ϊ1��corner���ܲ����������
                cor=self.findcorner(words[1])
                if(cor==None):
                    restemp1=("Accessable corner %s doesn't exit.\n"%words[1])
                    restemp2=self.makemessage(cmd,self,user,restemp1)
                else:
                    l=len(words)
                    m=" ".join(words[2:l])
                    restemp1=("This is a message From %s :\n"%user.name)+m
                    restemp2="*message*"+self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    print(str(user.addr)+"msg inside the corner at %s \n" %ctime())#��¼�û�ʹ�ü�¼
                    
                    node=cor.head
                    
                    while node:
                        self.s.sendto(res,node.addr)#����ָ��
                        node=node._next
                     
                    restemp1=("send message to corner %s successfully.\n"%cor.name)
                    restemp2=self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#����ָ��
                    
                        
                    return 1
                        
                
                
            if(subcmd=="leave"):#�˳������Ӧ���ǹر���һ���߳�
                restemp1="leave\n"
                print(str(user.addr)+"leaves the server at %s \n" %ctime())#��¼�û�ʹ�ü�¼
                restemp2=self.makemessage(cmd,self,user,restemp1)
                res=restemp2.encode('utf-8')#String->Bytes
                self.s.sendto(res,user.addr)#����ָ��
                self.kickoutuser(user.name)#��server��ɾ�����û��ļ�¼
                return 1
                
            if(subcmd[0]=='@'):#@userid message,��ĳ���û�����˽����Ϣ
                desusername=words[0][2:l]
                desuser=userheadmxr.searchname(desusername)
                if(desuser==None):
                    restemp1=("User %s doesn't exit\n"%desusername)
                    restemp2=self.makemessage(cmd,self,user,restemp1)

                else:
                    l=len(words)
                    m=" ".join(words[1:l])
                    restemp1=("This is a message From %s :\n"%user.name)+m
                    restemp2="*message*"+self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    print(str(user.addr)+"send a msg to private user %s at %s \n" %(words[1],ctime()))#��¼�û�ʹ�ü�¼
                    
                    self.s.sendto(res,desuser.addr)#����ָ��
                    
                    restemp1=("send message to %s successfully.\n"%desuser.name)
                    restemp2=self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#����ָ��
                    
                    return 1
                    
                                         
        res=restemp2.encode('utf-8')#String->Bytes
        self.s.sendto(res,user.addr)#����ָ��
        return 1
        

        
    
    def makemessage(self,cmd,sender,user,data):#�����ظ���Ϣ
        head="#Response to command:"+str(cmd)+"#"
        head=head+"\nFrom Server:127.0.0.1"+"\nTo User:"+str(user.addr)+"\nTime:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if(isinstance(sender,server)):#server ����Ϣ
            head=head+"\nMessage from server"
        if(isinstance(sender,corner)):#corner ����Ϣ
            head=head+"\nMessage from corner:"+sender.name
        head=head+"\nMessage to user:"+user.name+"\n\n"
        
        body=head+str(data)
        
        body=body+"\n#end#"#sign end
        return body
    
    def establishsocket(self):#����socket
        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((self.HOST,self.PORT))
        print('The server is ready to receive:')
    
    def closesocket(self):#����ͨ�ţ��ر�socket
        if(self.s==None):
            print("No connection")
            return
        print("close at",ctime())
        self.s.close()#��֪��s����֮�����ʲô
        self.s=None
        
#########################################################################################################################    
    

userheadmxr=userNode("mxr",("127.0.0.1",12345))


if __name__=='__main__':
    
    serv=server()
    
    serv.establishsocket()#����socket
       
    serv.listenmessage()

    