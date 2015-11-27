import SocketServer as socketserver
from threading import Thread
from Tkinter import *
from ttk import *
import Tableframe 
import socket
import Queue
import time
import os

global input_q,del_q,set_q,text_q ,widget,broad,data
input_q=Queue.Queue()
del_q=Queue.Queue()
set_q=Queue.Queue()
text_q=Queue.Queue() 
pendrive={0:'Not detected',1:'Detected'}
data = "REQUEST"
escape='\r\n'
widget={}
a= False
broad=True   
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
class RequestHandler(socketserver.StreamRequestHandler):
      def handle(self):  
          tl=[]
          tl.append(self.client_address[0])           
          tl.append(self.rfile.readline().strip())    
          tl.append(self.rfile.readline().strip())    
          tl.append(pendrive[int(self.rfile.readline().strip())])   
          input_q.put(tl)
          l=True




          while l:
              try:
                    l=self.rfile.readline()
                    if len(l)==0:
                          del_q.put(tl)
                          break                          
              except:
                    widget['text'].insert(END,'Client with ip-'+tl[0] +'disconected \n')
                    del_q.put(tl)
                    break
              
              l=l.strip()     
              set_q.put((tl,l))  



def get_os(num):
      key=widget['tableFrame'].row[3].winfo_children()
      return key[num].cget('text')

def get_ip(num):
      key=widget['tableFrame'].row[1].winfo_children()
      return key[num].cget('text')

               
def shut_down(l):
      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
      a=int(l[0])-1
      s.connect((get_ip(a),2121))
      if get_os(a)=='nt':
            s.send('shutdown /s'+escape)
      else:
            s.send('shutdown -P now'+escape)
      s.close()




def note_pad(l):
      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
      a=int(l[0])-1
      s.connect((get_ip(a),2121))
      if get_os(a)=='nt':
            s.send('notepad'+escape)
      else:
            s.send('vi'+escape)
      s.close()

def toggle_broadcast(arg):
      global broad
      if arg.__len__()== 0:
            if broad==True:
                  broad=False
            else:
                  broad=True
      else:
            if arg[0]=='False':
                  broad=False
            else:
                  broad=True
      if broad==True:
            widget['text'].insert(END,'New Broadcast setting set to True \n')
      else:
            widget['text'].insert(END,'New Broadcast setting set to False \n')


def set_strict(arg):
      global data
      if arg.__len__()== 0:
            if data=='REQUEST':
                  data='STRICT'
            else:
                  data='REQUEST'



      else:
            if arg[0]=='False':
                  data='REQUEST'
            else:
                  data='STRICT'
      if data=='STRICT':
            widget['text'].insert(END,'New Strict setting set to True \n')
      else:
            widget['text'].insert(END,'New Strict setting set to False \n')
      key=widget['tableFrame'].row[1].winfo_children()
      for ip in key:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.connect((ip.cget('text'),2121))
            if data=='STRICT':
                  s.send(':strict True'+escape)
            else:
                  s.send(':strict False'+escape)
            s.close()

def un_lock(arg):
      if arg.__len__()==0:
            key=widget['tableFrame'].row[1].winfo_children()
            for ip in key:
                  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                  s.connect((ip.cget('text'),2121))
                  s.send(':unlock'+escape)
                  s.close()
      else:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            a=int(arg[0])-1
            s.connect((get_ip(a),2121))
            s.send(':unlock'+escape)
            s.close()


            
def custom_command(arg):
      if arg.__len__()==0:
            widget['text'].insert(END,'Command need client id to connect\n')
      else:
            key=widget['tableFrame'].row[1].winfo_children()
            a=int(arg[0])-1
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.connect((get_ip(a),2121))
            s.send(' '.join(arg[1:]) +escape)
            print(' '.join(arg[1:])+escape)
            s.close()
            
command={'shutdown':shut_down,'notepad':note_pad,'unlock':un_lock,'command':custom_command}
sys_command= {'broadcast':toggle_broadcast,'strict':set_strict}     


def BroadCast():
    address =('255.255.255.255',6060)
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    while True:
        if broad:  
              client_socket.sendto(data,address)
        time.sleep(10)
        
def check(comm):
      if comm.__len__()==0:
            return
      
      if '\\' == comm[0]:
            l=comm[1:].split(' ')
            fun=command[l[0]]
            print(l[1:])
            fun(l[1:])


      elif ':'==comm[0]:
            l=comm[1:].split(' ')
            fun=sys_command[l[0]]
            fun(l[1:])
            
def entryHandler(event):
      a=widget['cmmEntry'].get()
      if a=='':
            return
      
      text.insert(END,'command:'+ a +'\n')
      check(a)
      widget['cmmEntry'].delete(0,END)

def backup():
      while not input_q.empty():
            widget['tableFrame'].insertRow(input_q.get())
            
      while not set_q.empty():
            ls,val=set_q.get()
            if val!='':
                  widget['tableFrame'].setData(ls,4,pendrive[int(val)])
      while not del_q.empty():
            widget['tableFrame'].delRow(del_q.get())
      widget['root'].after(500,backup)      
          
def closesafely():
      widget['root'].destroy()
      os._exit(0)


if __name__ == '__main__':
    widget['root']= root =Tk()  
    OutputFrame=Frame(root)  
    Label(OutputFrame,text='OUTPUT:').grid(row=0,sticky=W)
    TextScroll=Frame(OutputFrame)
    widget['text']=text=Text(TextScroll,height=10,width=50)
    scroll= Scrollbar(TextScroll,command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.pack(side=LEFT)
    scroll.pack(side=LEFT,fill=Y)
    TextScroll.grid(row=1,sticky=W)
    OutputFrame.grid(row=0,sticky=W)
    CommandFrame=Frame(root)
    Label(CommandFrame,text='COMMAND:').grid(row=0,column=0,sticky=W)
    widget['cmmEntry']=cmmEntry=Entry(CommandFrame,width=126)
    cmmEntry.grid(row=0,column=1,sticky=W)
    CommandFrame.grid(row=1,sticky=W,columnspan=2)
    widget['tableFrame']=tableFrame=Tableframe.Tableframe(root)
    tableFrame.grid(row=0,column=1,sticky=W)
    tableFrame.setHeader(("ID","ADDRESS","NAME","OS","PENDRIVE"))
    cmmEntry.bind('<Return>',entryHandler)
    

    root.resizable(height=FALSE,width=FALSE)
    
    hostname = socket.gethostname()
    s_port =  9999
    c_port =  6600
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((hostname, s_port),RequestHandler)    
    t=Thread(target=server.serve_forever,args=())                               
    b=Thread(target=BroadCast,args=())                                          
    t.daemon=True
    b.daemon=True
    b.start()
    t.start()
    root.protocol('WM_DELETE_WINDOW', closesafely)
    root.after(500,backup)
    root.mainloop()
