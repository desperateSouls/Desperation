__author__ = 'joshszczesniak'
from tkinter import *
import time
class GUI:
    def __init__(self, root):
        self.root = root
        self.threads = []
        self.messagesToSend = []
        self.messageBox = Entry(self.root)
        self.companionsBox = Listbox(self.root)
        self.sendButton = Button(text = "send", command = self.sendmessage)
        self.companionsBox.config(selectmode = 'single')
        self.companionsBox.grid(column = 0, row = 0, rowspan = 2)
        self.messageBox.grid(column = 1, row = 1)
        self.sendButton.grid(column = 2, row = 1)
    def getUsername(self):
        window = popupWindow(self.root)
        self.root.wait_window(window.top)
        self.username = window.username
        return self.username

    def addMessage(self, message):
        needNewThread = True
        for i in message[1:3]:
            if i != self.username:
                messagePartner = i
        for i in self.threads:
            if i.messagePartner == messagePartner:
                needNewThread = False
                i.addMessage( message)
        if needNewThread:
            Thread(messagePartner)

    def poll(self):
        msgs = self.messagesToSend
        self.messagesToSend = []
        return msgs

    def sendmessage(self):
        msg = (time.time(), self.companionsBox.get(ACTIVE), self.username, self.messageBox.get())
        self.messagesToSend.append(msg)
        for i in self.threads:
            if i.messagePartner == msg[1]:
                i.addMessage(msg)

    def update(self):
        for i in self.threads:
            if i.messagePartner == self.companionsBox.get(ACTIVE):
                i.updatePanel()
                i.panel.grid(column = 1, row = 0, columnspan = 2)
            else:
                try:
                    i.panel.gridforget()
                except:
                    pass

        self.root.update()

class Thread:
    def __init__(self,root, messagingPartner):
        self.messagingPartner = messagingPartner
        self.newMessages = []
        self.panel=Frame(root,width=300,height=300)
        self.panel.grid(row=0,column=0)
        self.canvas=Canvas(self.panel,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
        hbar=Scrollbar(self.panel,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(self.panel,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

    def addMessage(self, message):
        self.newMessages.append(message)

    def updatePanel(self):
        for i in self.newMessages:
            label = Label(text = i[2] + ": " + i[3])
            label.pack()
        self.newMessages = []

class popupWindow(object):
    def __init__(self,root):
        top = self.top = Toplevel(root)
        top.title("Log In")
        top.config(height=200, width=800)
        self.l = Label(top,text="Username:")
        self.l.grid(row=0, column=0)
        self.p = Label(top,text="Password:")
        self.p.grid(row=1, column=0)
        self.e = Entry(top)
        self.e.grid(row=0, column=1)
        self.e1 = Entry(top)
        self.e1.grid(row=1, column=1)
        self.b = Button(top,text='Enter:',command=self.cleanup)
        self.b.grid(row=2, columnspan=2)
    def cleanup(self):
        self.username=self.e.get()
        self.password=self.e1.get()
        self.top.destroy()

