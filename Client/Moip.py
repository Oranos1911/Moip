"""

@Oranos 2018

"""

from threading import Thread
from socket import *
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import configparser

config = configparser.ConfigParser()
config.read('Settings.ini')

FONT_COLOR = config.get('Design' , 'FONT_COLOR')
BG_COLOR = config.get('Design' , 'BG_COLOR')

IP = config.get('Network' , 'IP')
PORT = int(config.get('Network' , 'PORT'))

LOGO_IMG = """
█▀▄▀█ █▀▀█ ░▀░ █▀▀█
█░▀░█ █░░█ ▀█▀ █░░█ 
▀░░░▀ ▀▀▀▀ ▀▀▀ █▀▀▀
"""

LOGO_STR = "@_ʍ๏iρ by @Oranos"

class Main() :

    root = Tk()
    root.geometry('{}x{}'.format(720 , 460))
    root.resizable(width=False, height=False)
    root.title('Moip (%s:%d)' %(IP , PORT))
    root.configure(background = BG_COLOR)
    root.iconbitmap('icon.ico')

    def __init__(self) :

        self.initApplication()
        self.root.mainloop()


    def Connect(self , ip , port) :

        try:

            self.connection = socket(AF_INET, SOCK_STREAM)
            self.connection.connect((ip , port))

        except error as err:
            tkinter.messagebox.showerror(title='Network Error', message=err)
            quit()

        def loop():

            while True:

                try:
                    message = self.connection.recv(2048).decode('UTF-8')
                    self.Write(message)
                except error as err:
                    tkinter.messagebox.showerror(title='Network Error', message=err)
                    quit()

        cthread = Thread(target=loop)
        cthread.daemon = True
        cthread.start()

    def Write (self , message):

        self.RecvBox.config(state=NORMAL)
        self.RecvBox.insert("end", message + "\n")
        self.RecvBox.see("end")
        self.RecvBox.config(state=DISABLED)

    def Send (self, message):

        message = str.encode(message)

        try :
            self.connection.send(message)
            self.SendBox.delete(0, 'end')
        except AttributeError :
            tkinter.messagebox.showerror(title= 'Connection Error' , message= 'Not connected to any server yet')

    def SetMainButton(self, master, text, command, width=30):
        button = Button(master, text=text, font='Unispace 12', height=1, activebackground=BG_COLOR,
                        activeforeground=FONT_COLOR, bg=BG_COLOR, fg=FONT_COLOR, width=width, command=command)
        return button

    def SetSecendaryButton(self, master, text, command, size=8):
        button = Button(master, text=text, height=1, activebackground=BG_COLOR,
                        activeforeground=FONT_COLOR, font='Unispace %s bold' % (size), bg=BG_COLOR, fg=FONT_COLOR,
                        width=10, command=command)
        return button

    def SetLabel(self, master, text, size=12):

        label = Label(master=master, text=text, bg=BG_COLOR, fg=FONT_COLOR, font='Unispace %s bold' % (size))
        return label


    def initApplication(self):


        self.SetLabel(self.root , text = LOGO_IMG , size = 15).grid(row = 0 , pady = 5)

        self.RecvBox = Text(self.root, state=DISABLED, bg='#000000', fg='#ffffff', selectbackground='#000000', height=15, width = 85)
        self.RecvBox.grid(row=1, padx=15 , sticky = W)

        message = StringVar()

        self.SendBox = Entry(self.root, bg=BG_COLOR, fg=FONT_COLOR, bd=1, selectbackground=BG_COLOR, textvariable= message, width=95)
        self.SendBox.grid(row=2, padx=15, pady=15, sticky=W)
        self.SendBox.bind("<Return>", lambda event : self.Send(message.get()))

        self.SetSecendaryButton(self.root, 'Send' , lambda : self.Send(message.get())).grid(row= 2, padx= 40 , sticky=E)

        ipVar , portVar = StringVar() , StringVar()

        self.SetLabel(self.root, "Server : ", 10).grid(row = 3 , sticky = W , padx = 15)
        self.IpBox = Entry(self.root, bg=BG_COLOR , fg = FONT_COLOR, bd=1, selectbackground=BG_COLOR, textvariable= ipVar, width=25)
        self.IpBox.grid(row = 3 , sticky = W , padx = 90)

        self.SetLabel(self.root , "Port : " , 10).grid(row = 3 , sticky = W , padx = 250)
        self.PortBox = Entry(self.root, bg=BG_COLOR, fg=FONT_COLOR, bd=1, selectbackground=BG_COLOR, textvariable= portVar , width = 10)
        self.PortBox.grid(row = 3 , sticky = W , padx = 300)

        self.SetSecendaryButton(self.root, 'Connect', lambda: self.Connect(ipVar.get() , int(portVar.get()))).grid(row=3, padx= 250, sticky=E)


Main()
