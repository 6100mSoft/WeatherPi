from sys import argv
from threading import Thread
import liquidcrystal_i2c
import socket
def clr():
    for x in range(0,3):
        lcd.printline(x,"")
def log():
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    if ins.get_resp():
        msg=ins.get_resp().strip().split(":")
        if i<=3:
            lcd.printline(i,"< {}> {}".format(msg[1].split("!")[0],msg[2].strip()))
        else:
            clr()
class Client:
    def __init__(self,usr,ch,srv="irc.freenode.net",dev=6667):
        self.usr=usr
        self.srv=srv
        self.dev=dev
        self.ch=ch
    def con(self):
        self.con=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.con.connect((self.srv,self.dev))
    def get(self):
        return self.con.recv(512).decode("utf-8")
    def send(self,cmd,msg):
        self.con.send("{} {}\r\n".format(cmd,msg).encode("utf-8"))
    def msgr(self,msg):
        cmd="PRIVMSG {}".format(self.chn)
        self.send(cmd,":"+msg)
    def join(self):
        self.send("JOIN",self.chn)
if __name__=="__main__":
    lcd=liquidcrystal_i2c.LiquidCrystal_I2C(0x27,1,numlines=4)
    n=3
    i=0
    if len(argv)!=3:
        lcd.printline(0,"bl4de IRC Client mod")
        lcd.printline(1,"client.py user" + "#" + "channel")
        lcd.printline(2,"Initilization Status:")
        lcd.printline(3,"Init Complete!")
        exit(0)
    usr=argv[1]
    ch=f"#{argv[2]}"
    cmd=""
    flg=False
    ins=Client(usr,ch)
    ins.con()
    lcd.printline(2,"Bootup Status:")
    lcd.printline(3,"Bootup Complete!")
    # Proper registration implementation by my friend epicness @ github.com/3picness
    # Thanks! :3
    authNotSent = True
    while(flg==False):
        res=ins.get()
        if n<=2:
            n=n+1
            clr()
        else:
            n=n-3
            clr()
        if "No Ident response" in res or authNotSent:
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
            authNotSent = False
        if "376" in res:
            ins.join()
        if "433" in res:
            usr="_"+usr
            ins.send("USER","{} * * :{}".format(usr,usr))
            ins.send("NICK",usr)
        if "PING" in res:
            ins.send("PONG", ":"+res.split(":")[1])
        if "366" in res:
            flag=True
    while(cmd != "/quit"):
        if input("< {}> ".format(usr)).strip()=="/quit":
            ins.send("QUIT", "Good bye!")
        ins.msgr(cmd)
        run=Thread(target=log)
        run.daemon=True
        run.start()
