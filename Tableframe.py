from Tkinter import *
from ttk import *
class Tableframe(Frame):
    
    def __init__(self, parent,tableheight=164, *args, **kw):
        Frame.__init__(self,parent,*args, **kw)            
        Label(self,text="User DATA").pack(side=TOP)
        
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        
        canvas = Canvas(self, bd=0 ,bg='white', highlightthickness=0,yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        self.row=[]             
        self.rowId=[]          
        self.rowLabel={}       
        self.header=[]          
        
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        
        self.interior = interior = Frame(canvas)
        interior_id=canvas.create_window(0,0,window=interior,anchor=NW, state= NORMAL) 

        
        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth(),height=tableheight)
        interior.bind('<Configure>', _configure_interior)



        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width(): 
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    def setHeader(self,ls):
        k=0
        for i in ls:
            self.header.append(i)
            Button(self.interior,text=i).grid(row=0,column=k,sticky=EW)
            self.row.append(Frame(self.interior))
            self.row[-1].grid(row=1,column=k,sticky=EW)                
            k=k+1

            
    def insertRow(self,ls):
        k=[]
        a=0
        self.rowId.append(Label(self.row[a],text=len(self.rowLabel)+1,relief=SOLID,width=len(self.header[a])))
        self.rowId[-1].pack(side=TOP,fill=X)
        a=a+1
        for i in ls:
            k.append(Label(self.row[a],text=i,relief=SOLID,width=len(self.header[a])))
            k[-1].pack(side=TOP,fill=X)
            a=a+1
        try:
            self.rowLabel[ls[0]]=k
        except:
            pass
        return len(self.rowLabel)+1
    def delRow(self,ls):
        k=self.rowLabel.pop(ls[0])
        for i in k:
            i.pack_forget()
            i.destroy()
        self.rowId.pop().destroy()

        
    def setData(self,ls,col,value):
        k=self.rowLabel.pop(ls[0])
        k[col-1].configure(text=value)
        ls[col-1]=value
        self.rowLabel[ls[0]]=k
