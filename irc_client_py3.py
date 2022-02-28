import liquidcrystal_i2c
import socket
import threading
from sys import argv
def usage():
    print("IRC simple Python client | by bl4de | github.com/bl4de | twitter.com/_bl4de | hackerone.com/bl4de\n")
    print("$ ./irc_client_py3.py user channel\n")
    print("where: usr - your user, channel - channel you'd like to join (eg. channel or #channel)")
def chn(chn):
    if chn.startswith("#") == False:
        return "#" + chn
    return chn
def print_resp():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    resp = ins.get_resp()
    if resp:
        msg = resp.strip().split(":")
        if i <= 3:
            lcd.printline(data,"< {}> {}".format(
                msg[1].split("!")[0],msg[2].strip()))
        else:
            clean()
        if i <= 2:
            i = i + 1
            clean()
class Client:
    def __init__(self, usr, chn, server="irc.freenode.net", port=6667):
        self.usr = usr
        self.server = server
        self.port = port
        self.chn = chn
    def conn(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.conn((self.server, self.port))
    def get_resp(self):
        return self.conn.recv(512).decode("utf-8")
    def send(self, cmd, message):
        self.conn.send("{} {}\r\n".format(cmd,message).encode("utf-8"))
    def sendmsg2chn(self, message):
        command = "PRIVMSG {}".format(self.chn)
        self.send_cmd(command, ":" + message)
    def join(self):
        self.send_cmd("JOIN", self.chn)
if __name__ == "__main__":
    if len(argv) != 3:
        usage()
        exit(0)
    else:
        usr = argv[1]
        chn = chn(argv[2])
    i = 0
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    cmd = ""
    joined = False
    ins = Client(usr, chn)
    ins.conn()
    num = 0
    while(joined == False):
        resp = ins.get_resp()
        if num <= 2:
            num = num + 1
            clean()
        else:
            num = num - 3
            clean()
        lcd.printline(num, resp.strip())
        if "No Ident resp" in resp:
            ins.send("NICK", usr)
            ins.send("usr","{} * * :{}".format(usr,usr))
        if "376" in resp:
            ins.join()
        if "433" in resp:
            usr = "_" + usr
            ins.send("usr","{} * * :{}".format(usr,usr))
            ins.send("NICK", usr)
        if "PING" in resp:
            ins.send("PONG", ":" + resp.split(":")[1])
        if "366" in resp:
            joined = True
    while(cmd != "/quit"):
        cmd = input("< {}> ".format(usr)).strip()
        if cmd == "/quit":
            ins.send_cmd("QUIT", "Good bye!")
        ins.sendmsg2chn(cmd)
        run = threading.Thread(target=print_resp)
        run.daemon = True
        run.start()
def clean():
    for x in range(0, 3):
        lcd.printline(x, "")
