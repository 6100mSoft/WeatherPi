#!/usr/bin/env python
# by bl4de | github.com/bl4de | twitter.com/_bl4de | hackerone.com/bl4de
import socket
import threading
import sys
import liquidcrystal_i2c
def usage():
    print("IRC simple Python ins | by bl4de | github.com/bl4de | twitter.com/_bl4de | hackerone.com/bl4de\n")
    print("$ ./irc_ins.py user chn\n")
    print("where: user - your user, chn - chn you'd like to join (eg. chnname or #chnname)")
def chn(chn):
    if chn.startswith("#") == False:
        return "#" + chn
    return chn
def print_resp():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    resp = ins.get_resp()
    if resp:
        msg = resp.strip().split(":")
        if data <= 3:
            lcd.printline(data,"< {}> {}".format(msg[1].split("!")[0], msg[2].strip()))
        else:
            for x in range(0, 3):
                lcd.printline(x, "")
        if data <= 2:
            data = data + 1
            for x in range(0, 3):
                lcd.printline(x, "")
        else:
            data = data - 3
            for y in range(0, 3):
                lcd.printline(y, "")
class IRCSimpleins:
    def __init__(self, user, chn, server="irc.freenode.net", port=6667):
        self.user = user
        self.server = server
        self.port = port
        self.chn = chn
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))
    def get_resp(self):
        return self.conn.recv(512).decode("utf-8")
    def send_cmd(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message).encode("utf-8")
        self.conn.send(command)
    def send_message_to_chn(self, message):
        command = "PRIVMSG {}".format(self.chn)
        self.send_cmd(command, ":" + message)
    def join_chn(self):
        chn = self.chn
        self.send_cmd("JOIN", chn)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(0)
    else:
        user = sys.argv[1]
        chn = chn(sys.argv[2])
    data = 0
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    cmd = ""
    joined = False
    ins = IRCSimpleins(user, chn)
    ins.connect()
    int_data = 0
    while(joined == False):
        resp = ins.get_resp()
        if data <= 2:
            data = data + 1
            for x in range(0, 3):
                lcd.printline(x, "")
        else:
            data = data - 3
            for y in range(0, 3):
                lcd.printline(y, "")
        lcd.printline(int_data, resp.strip())
        if "No Ident resp" in resp:
            ins.send_cmd("NICK", user)
            ins.send_cmd(
                "USER", "{} * * :{}".format(user, user))
        if "376" in resp:
            ins.join_chn()
        if "433" in resp:
            user = "_" + user
            ins.send_cmd(
                "USER", "{} * * :{}".format(user, user))
            ins.send_cmd("NICK", user)
        if "PING" in resp:
            ins.send_cmd("PONG", ":" + resp.split(":")[1])
        if "366" in resp:
            joined = True
    while(cmd != "/quit"):
        cmd = input("< {}> ".format(user)).strip()
        if cmd == "/quit":
            ins.send_cmd("QUIT", "Good bye!")
        ins.send_message_to_chn(cmd)
        resp_thread = threading.Thread(target=print_resp)
        resp_thread.daemon = True
        resp_thread.start()
