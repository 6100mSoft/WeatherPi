from sys import argv
from threading import Thread
import liquidcrystal_i2c
import socket
def chn(ch):
    if ch.startswith("#")==False:
        return "#"+ch
    return ch
def log_resp():
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    if ins.get_resp():
        msg=ins.get_resp().strip().split(":")
        if i<=3:
            lcd.printline(i,"< {}> {}".format(msg[1].split("!")[0],msg[2].strip()))
        else:
            clr()
class Client:
    def __init__(self,usr,ch,server="irc.freenode.net",port=6667):
        self.usr=usr
        self.server=server
        self.port=port
        self.chn=ch
    def con(self):
        self.con=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.con.conn((self.server,self.port))
    def get_resp(self):
        return self.con.recv(512).decode("utf-8")
    def send(self,cmd,msg):
        self.con.send("{} {}\r\n".format(cmd,msg).encode("utf-8"))
    def send2ch(self,msg):
        cmd="PRIVMSG {}".format(self.chn)
        self.send_cmd(cmd,":"+msg)
    def join(self):
        self.send_cmd("JOIN",self.chn)
if __name__=="__main__":
    if len(argv)!=3:
        print("IRC simple Python client | by bl4de \n")
        print("$ ./irc_client_py3.py user channel")
        exit(0)
    usr=argv[1]
    ch=chn(argv[2])
    i=0
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    cmd=""
    joined=False
    ins=Client(usr,ch)
    ins.con()
    n=0
    while(joined==False):
        res=ins.get_resp()
        if n<=2:
            n=n+1
            clean()
        else:
            n=n-3
            clean()
        lcd.printline(n,res.strip())
        if "No Ident response" in res:
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
        if "376" in res:
            ins.join()
        if "433" in res:
            usr="_"+usr
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
        if "PING" in res:
            ins.send("PONG", ":"+res.split(":")[1])
        if "366" in res:
            joined=True
    while(cmd != "/quit"):
        if input("< {}> ".format(usr)).strip() == "/quit":
            ins.send_cmd("QUIT", "Good bye!")
        ins.send2ch(cmd)
        run=Thread(target=log_resp)
        run.daemon=True
        run.start()
def clean():
    for x in range(0,3):
        lcd.printline(x,"")
