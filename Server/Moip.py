
from socket import *
import threading
import urllib3
import sqlite3
from datetime import datetime as dt
import configparser

config = configparser.ConfigParser()
config.read('Settings.ini')

PORT = int(config.get('Network' , 'PORT'))


def getIP() :

    try :

        http = urllib3.PoolManager()
        request = http.request('GET' , "http://ipecho.net/plain" )
        ip = request.data.decode('utf-8')
        return (ip)

    except Exception :
        return "localhost"

class User() :

    username = ''

    def __init__(self , client , addr) :

        ip , _ = addr

        for (address ,username) in self.GetData('Acounts') :
            if (ip == address) :
                self.username = username

        client.send(str.encode("Welcome %s ! Connected to Moip server %s"%(self.username , getIP() )))

        if not self.username :

            with open('WelcomeMessage.txt') as f :
                WelcomeMessage = f.read() %(getIP() , ip)


            client.send(str.encode(WelcomeMessage))
            self.username = client.recv(2048).decode()

            self.InsertData('Acounts' , (ip , self.username))


        LogDate = dt.today().strftime('%D %T')
        self.InsertData('Logs' , (ip , LogDate))
         

    def GetData(self , table):

          conn = sqlite3.connect('DB.db')
          cur = conn.cursor()
          cur.execute("SELECT * FROM '%s'" %(table))
          return cur.fetchall()

    def InsertData(self , table , data):

        d1  , d2 = data

        conn = sqlite3.connect('DB.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO %s Values('%s' , '%s')" % (table , d1 , d2))
        conn.commit()


class Server :

    Server = socket(AF_INET, SOCK_STREAM)
    Connections = []

    def __init__(self , port):

        try:
            self.Server.bind(('0.0.0.0', port))
            print ( "Host name : " + getfqdn() )
            print('Server Listening on %s:%d' %(getIP() , port))
        except error as e :
            print(e)
            quit()

        self.Server.listen(1)

    def Handler(self , client , addr) :

        print("(%s:%s) Connected" % (addr[0], addr[1]))

        username = User(client, addr).username

        for connection in self.Connections:
            c , _ = connection
            c.send(str.encode("%s Connected" %(username)))

        self.Connections.append((client , addr))

        while True :

            try :
                message = client.recv(2048).decode()
                if message is not None :
                    print("%s : %s" %(addr  , message))
                    for connection in self.Connections:
                        c , _ = connection
                        c.send(str.encode("%s : %s" %(username , message)))
            except error :
                break

        client.close()
        self.Connections.remove((client , addr))

        print("(%s:%s) Dissconnected" % (addr[0], addr[1]))

        for connection in self.Connections:
            c , _ = connection
            c.send(str.encode("%s Disconnected" %(username)))

    def run(self):

        try :

            while True :

                client , addr = self.Server.accept()
                cthread = threading.Thread(target = self.Handler , args=(client, addr))
                cthread.daemon = True
                cthread.start()

        except KeyboardInterrupt :

                self.Server.close()
                print("[*] Sever stopped ! ")



Server = Server(PORT)
Server.run()
