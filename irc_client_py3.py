from sys import argv
from threading import Thread
import liquidcrystal_i2c
import socket
def chn(chn):
    if chn.startswith("#")==False:
        return "#"+chn
    return chn
def log_resp():
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    if ins.get_resp():
        msg=ins.get_resp().strip().split(":")
        if i<=3:
            lcd.printline(i,"< {}> {}".format(msg[1].split("!")[0],msg[2].strip()))
        else:
            clr()
class Client:
    def __init__(self,usr,chn,server="irc.freenode.net",port=6667):
        self.usr=usr
        self.server=server
        self.port=port
        self.chn=chn
    def con(self):
        self.con=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.con.con((self.server,self.port))
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
    chn=chn(argv[2])
    i=0
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    cmd=""
    joined=False
    ins=Client(usr,chn)
    ins.con()
    n=0
    while(joined==False):
        resp=ins.get_resp()
        if n<=2:
            n=n+1
            clean()
        else:
            n=n-3
            clean()
        lcd.printline(n,resp.strip())
        if "No Ident resp" in resp:
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
        if "376" in resp:
            ins.join()
        if "433" in resp:
            usr="_"+usr
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
        if "PING" in resp:
            ins.send("PONG", ":"+resp.split(":")[1])
        if "366" in resp:
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
