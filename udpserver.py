import socket
import datetime 
import hashlib #用来转换bytes与string的
import threading
from time import ctime,sleep


#编号从1开始计数

class userNode:
    '''
    name
    addr  
    num
    _next: 保存下一个节点对象
    '''
    num=0 #用户编号
    def __init__(self,n,address,pnext=None):
        self.name=n
        self.addr=address
        self._next = pnext

    def __repr__(self):
        '''
        用来定义userNode的字符输出，
        print为输出data
        '''
        if (self.num==0):#还没有加入英语角
            return str("username:"+self.name+"\nip:"+str(self.addr)+"\n")
        else:#用户已经加入英语角
            return str("NO."+str(self.num)+":username:"+self.name+"\nip:"+str(self.addr)+"\n")
        
    def adduser(self,newuser):
        if(self!=userheadmxr):
            return #只有userheadmxr有这个权限可以加，userheadmxr就是老大！编号是独一无二的0！
        item=newuser
        node=userheadmxr
        while node._next:
            node=node._next
        item.num=node.num+1
        node._next=item
        
    def searchname(self,n):
        if(self!=userheadmxr):
            return None#只有userheadmxr有这个权限可以搜寻，userheadmxr就是老大！编号是独一无二的0！
        node=userheadmxr
        while node:
            if(node.name==n):
                return node
            node=node._next
            
        return None
    
    def isregister(self,addr):#通过检测addr看是否有无建立过连接
        if(self!=userheadmxr):
            return None#只有userheadmxr有这个权限可以搜寻，userheadmxr就是老大！编号是独一无二的0！
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
            return#只有userheadmxr有这个权限可以搜寻，userheadmxr就是老大！编号是独一无二的0！
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
    length=0 #user 的数量
    head=None #user 链表头
    
    def __init__(self,n,pnext=None):
        self.name = n
        self._next = pnext
        
    def __repr__(self):
        '''
        用来定义corner的字符输出
        '''
        return str("NO."+str(self.num)+":cornername:"+self.name+"\n")
   
    def adduser(self, newuser):
        item = newuser

        if not self.head:#corner为空
            self.head = item
            self.length += 1
            item.num=1
            return 1#成功加入

        else:
            node = self.head
            while node._next:#新用户加到最后一个节点的后面
                if(node.name==item.name):#这个用户已经在这个英语角里面了
                    return 0
                node = node._next
            if(node.name==item.name):#这个用户已经在这个英语角里面了，检查最后一个usernode
                return 0
            self.length += 1
            item.num=self.length
            node._next = item
            
        return 1
    
    def deleteuser(self, n):#根据user的name来删除用户
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

        #prev为保存前导节点,node为保存当前节点
        #删除一个节点之后把链表长度减一，还要把后续用户的编号向前挪1

        flag=0
        node=self.head._next#已经检测完头部不是要删除的对象
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
    server含有元素：
    HOST,PORT,password
    length,head
    s:socket,需要研究多进程
    '''
    length=0 #corner的数量
    head=None #corner链表头
    password="16307130347"
    PORT=12345
    HOST='127.0.0.1'
    s=None
        
    def kickoutuser(self,n):
        node=self.head
        while node:
            node.deleteuser(n)
            node=node._next
            
        userheadmxr.deleteuser(n)#在管理员那里删除记录
            
        

    def opencorner(self, newcorner):
        item = newcorner

        if not self.head:#没有corner
            self.head = item
            self.length += 1
            item.num=1
            return 1

        else:
            node = self.head
            while node._next:#新corner加到最后一个节点的后面
                if(node.name==newcorner.name):
                    return 0#这个corner已经存在，无法add
                node = node._next
                
            if(node.name==newcorner.name):
                return 0#这个corner已经存在，无法add
            node._next = item
            self.length += 1
            item.num=self.length
            return 1
    
    def closecorner(self,n):#n为corner的name
        if (self.length==0):#空server
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
        #删除一个节点之后把链表长度减一，还要把后续用户的编号向前挪1
        #prev为保存前导节点,node为保存当前节点

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
    
    def findcorner(self,n):#根据name返回corner的类型
        node=self.head
        while node:
            if(node.name==n):
                return node
            node=node._next
        return None

        
    def listenmessage(self):#接收指令
        if(self.s==None):
            print("No socket established,error!")
            return
        useflag=0#记录这个IP地址是否是第一次发消息给server，如果是那么创建新的user
        flag=1
        while 1:#多次接收信息
            if(self.s==None):
                return
            data,addr=self.s.recvfrom(2048) #只会返回data,收到的数据格式是b'cmd',是Bytes类型
            cmd=bytes.decode(data)#Bytes->String
            thisuser=userheadmxr.isregister(addr)
            if(thisuser==None):#register注册
                words=cmd.split()
                if(words[0]=="/name"):
                    l=len(words)
                    
                    if(l==1):#名字不能为空
                        thisuser=userNode(" ",addr)
                        restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed,Please register again\n")
                        res=restemp.encode('utf-8')#String->Bytes
                        self.s.sendto(res,thisuser.addr)#发送指令
                        
                    else:
                        n=" ".join(words[1:l])#合并String数组变成String，中间以空格间隔，获取用户名
                        thisuser=userNode(n,addr)
                        if(userheadmxr.searchname(n)!=None):#已经有用户注册了这个名字                       
                            restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed.This name has been taken\n")
                            res=restemp.encode('utf-8')#String->Bytes
                            self.s.sendto(res,thisuser.addr)#发送指令
                        
                        else:
                            userheadmxr.adduser(thisuser)
                            print(str(thisuser.addr)+" enter at %s \n" %ctime())#记录用户使用记录
                            restemp="#status:Succeed#\n"+self.makemessage(cmd,self,thisuser,"Register successfully\n")
                            res=restemp.encode('utf-8')#String->Bytes
                            self.s.sendto(res,thisuser.addr)#发送指令
                else:
                    thisuser=userNode("Unverified User",addr)
                    restemp="#status:Failed#\n"+self.makemessage(cmd,self,thisuser,"Register failed,Please register again\n")
                    res=restemp.encode('utf-8')#String->Bytes
                    self.s.sendto(res,thisuser.addr)#发送指令
            
                    
            else:
                self.handlemessage(cmd,thisuser)#是否应该停止接收指令
            
        
    
    def handlemessage(self,cmd,user):#处理并发送指令
        #先假定全部都是坏指令
        restemp1="Wrong command format\n"
        restemp2="#status:Failed#\n"+self.makemessage(cmd,self,user,restemp1)
    
        words=cmd.split()
    
        if(words[0]=="mxr"):#it is command from server manager
            if(words[1]==serv.password):#verify identification
                print("Server logging......\n"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))#记录server登录时间
                l=len(words)
                n=" ".join(words[3:l])
                if(words[2]=="kickout"):           
                    self.kickoutuser(n)
                    restemp2=self.makemessage(cmd,self,user,("Manager mxr kickout %s\n"%n))
                if(words[2]=="opencorner"):
                    temp=corner(n)
                    if(self.opencorner(temp)==1):#成功open了一个corner
                        restemp2=self.makemessage(cmd,self,user,("Manager mxr opencorner %s\n"%n))
                    else:
                        restemp2=self.makemessage(cmd,self,user,("Corner %s has already existed.\n"%n))
                if(words[2]=="closecorner"):
                    if(self.closecorner(n)==1):#成功close了一个corner
                        restemp2=self.makemessage(cmd,self,user,("Manager mxr closecorner %s\n"%n))
                    else:
                        restemp2=self.makemessage(cmd,self,user,("Corner %s doesn't exist.\n"%n))
                        
                if(words[2]=="terminate"):#关闭socket
                    restemp2=self.makemessage(cmd,self,user,("Terminate the Server.\n"))
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#发送指令
                    
                    #通知所有用户服务器已经关闭
                    restemp2="404"
                    res=restemp2.encode('utf-8')#String->Bytes
                    node=userheadmxr._next
                    while node:
                        self.s.sendto(res,node.addr)#发送指令
                        node=node._next
                    
                    self.closesocket()
                    return 0
            
            
        if(words[0][0]=='/'):#it is command from client user
            l=len(words[0])
            if(l==1):#考虑只发送/的情况
                res=restemp2.encode('utf-8')#String->Bytes
                self.s.sendto(res,user.addr)#发送指令
                return 1
            subcmd=words[0][1:l]#截取command命令的种类,后一位参数，即l的取法是取下标为l-1的字符

            if(subcmd=="corners"):#列出所有开通的外语角
                print(str(user.addr)+"listcorners at %s \n" %ctime())#记录用户使用记录
                restemp1=serv.listcorners()
                restemp2=self.makemessage(cmd,self,user,restemp1)              
                
            if(subcmd=="listusers"):#列出当前所在外语角的所有用户
                l=len(words)
                n=" ".join(words[1:l])#合并String数组变成String，中间以空格间隔
                print(str(user.addr)+"listusers at corner %s at %s \n" %(n,ctime()))#记录用户使用记录
                
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                else:
                    restemp1=cor.listusers()
                        
                restemp2=self.makemessage(cmd,cor,user,restemp1) 
                
            if(subcmd=="join"):#Join corner username
                l=len(words)
                n=" ".join(words[1:l])#合并String数组变成String，中间以空格间隔
                print(str(user.addr)+"joins the corner %s at %s \n" %(n,ctime()))#记录用户使用记录
                
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                    restemp2=self.makemessage(cmd,cor,user,restemp1)
                else:#加入corner
                    temp=userNode(user.name,user.addr)
                    if(cor.adduser(temp)==1):
                        restemp2=self.makemessage(cmd,cor,user,("User %s joins %s\n"%(user.name,cor.name)))
                    else:
                        restemp2=self.makemessage(cmd,cor,user,("User %s has already joined %s\n"%(user.name,cor.name)))
                         
                
            if(subcmd=="exit"):#exit a corner
                l=len(words)
                n=" ".join(words[1:l])#合并String数组变成String，中间以空格间隔
                              
                cor=self.findcorner(n)
                if(cor==None):
                    restemp1=n+":No such corner.\n"
                    restemp2=self.makemessage(cmd,cor,user,restemp1) 
                else:#退出corner
                    if(cor.deleteuser(user.name)==1):#成功退出相应corner
                        print(str(user.addr)+"exits the corner %s at %s \n" %(n,ctime()))#记录用户使用记录
                        restemp2=self.makemessage(cmd,cor,user,("User %s exits %s\n"%(user.name,cor.name)))
                    else:
                        restemp2=self.makemessage(cmd,cor,user,("User %s is not in %s\n"%(user.name,cor.name)))
                
                
                
            if(subcmd=="msg"):#在外语角中发布一条消息，被外语角中所有用户收到，设置只有单词长度为1的corner才能采用这个功能
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
                    print(str(user.addr)+"msg inside the corner at %s \n" %ctime())#记录用户使用记录
                    
                    node=cor.head
                    
                    while node:
                        self.s.sendto(res,node.addr)#发送指令
                        node=node._next
                     
                    restemp1=("send message to corner %s successfully.\n"%cor.name)
                    restemp2=self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#发送指令
                    
                        
                    return 1
                        
                
                
            if(subcmd=="leave"):#退出软件，应该是关闭这一条线程
                restemp1="leave\n"
                print(str(user.addr)+"leaves the server at %s \n" %ctime())#记录用户使用记录
                restemp2=self.makemessage(cmd,self,user,restemp1)
                res=restemp2.encode('utf-8')#String->Bytes
                self.s.sendto(res,user.addr)#发送指令
                self.kickoutuser(user.name)#在server端删除该用户的记录
                return 1
                
            if(subcmd[0]=='@'):#@userid message,给某个用户发送私人信息
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
                    print(str(user.addr)+"send a msg to private user %s at %s \n" %(words[1],ctime()))#记录用户使用记录
                    
                    self.s.sendto(res,desuser.addr)#发送指令
                    
                    restemp1=("send message to %s successfully.\n"%desuser.name)
                    restemp2=self.makemessage(cmd,self,user,restemp1)
                    res=restemp2.encode('utf-8')#String->Bytes
                    self.s.sendto(res,user.addr)#发送指令
                    
                    return 1
                    
                                         
        res=restemp2.encode('utf-8')#String->Bytes
        self.s.sendto(res,user.addr)#发送指令
        return 1
        

        
    
    def makemessage(self,cmd,sender,user,data):#制作回复信息
        head="#Response to command:"+str(cmd)+"#"
        head=head+"\nFrom Server:127.0.0.1"+"\nTo User:"+str(user.addr)+"\nTime:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if(isinstance(sender,server)):#server 发消息
            head=head+"\nMessage from server"
        if(isinstance(sender,corner)):#corner 发消息
            head=head+"\nMessage from corner:"+sender.name
        head=head+"\nMessage to user:"+user.name+"\n\n"
        
        body=head+str(data)
        
        body=body+"\n#end#"#sign end
        return body
    
    def establishsocket(self):#建立socket
        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((self.HOST,self.PORT))
        print('The server is ready to receive:')
    
    def closesocket(self):#结束通信，关闭socket
        if(self.s==None):
            print("No connection")
            return
        print("close at",ctime())
        self.s.close()#天知道s关了之后成了什么
        self.s=None
        
#########################################################################################################################    
    

userheadmxr=userNode("mxr",("127.0.0.1",12345))


if __name__=='__main__':
    
    serv=server()
    
    serv.establishsocket()#建立socket
       
    serv.listenmessage()

    