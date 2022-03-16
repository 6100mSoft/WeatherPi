from pathlib import Path
from sys import argv
import threading
import liquidcrystal_i2c
import random
import socket
import time
import threading
import json
import pathlib


def get():
    return Path(__file__).absolute()


def clr():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    for x in range(0, 3):
        lcd.printline(x, "")
    print("clear func trigger pulled")


def refresh():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    for x in range(0, 3):
        lcd.printline(x, "")
    print("refresh func trigger pulled")
    time.sleep(2)


def log():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    if ins.get():
        msg = ins.get().strip().split(":")
    if i <= 3:
        lcd.printline(i, "< {}> {}".format(msg[1].split("!")[0], msg[2].strip()))
    else:
        clr()


class Client:
    def __init__(self, usr, ch, srv="irc.freenode.net", dev=6667):
        self.usr = usr
        self.srv = srv
        self.dev = dev
        self.ch = ch

    def con(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect((self.srv, self.dev))

    def get(self):
        return self.con.recv(512).decode("utf-8")

    def send(self, cmd, msg):
        self.con.send("{} {}\r\n".format(cmd, msg).encode("utf-8"))

    def msgr(self, msg):
        cmd = "PRIVMSG {}".format(self.ch)
        self.send(cmd, ":" + msg)

    def join(self):
        self.send("JOIN", self.ch)


if __name__ == "__main__":
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    n = 3
    i = 0
    if len(argv) != 3:
        lcd.printline(0, "Teddiursa Client")
        lcd.printline(1, "client.py user" + "#" + "channel")
        lcd.printline(2, "Initilization Status:")
        lcd.printline(3, "Init Complete!")
        exit(0)
    else:
        usr = argv[1]
        ch = f"#{argv[2]}"
        cmd = ""
        seed = random.getrandbits(128)
        flg = False
        ins = Client(usr, ch)
        ins.con()
        random.random()
        clr()
        lcd.printline(2, "Bootup Status:")
        lcd.printline(3, "Bootup Complete!")
        # Proper registration implementation
        # by my friend epicness @
        # github.com/3picness
        # Thanks! :3
        authNotSent = True
        while flg == False:
            res = ins.get()
            print(res.strip())
            lcd.printline(n, res.strip())
            if n <= 2:
                n = n + 1
                clr()
            else:
                n = n - 3
                clr()
            with open(get() + "debug.json", "r") as f:
                config = load(f)
            if "No Ident response" in res or authNotSent:
                ins.send("USER", "{} * * :{}".format(usr, usr))
                ins.send("NICK", usr)
                if config["debugflag1"] == true:
                    ins.send(
                        "PRIVMSG",
                        f"{ch} :"
                        + f"Client Node: {seed} | Teddiursa IRC Client: Missing ident response, retrying...",
                    )
                else:
                    print("type 0 --- flag 0 flashed")
                authNotSent = False
            if "376" in res:
                ins.join()
                if config["debugflag2"] == true:
                    ins.send(
                        "PRIVMSG",
                        f"{ch} :"
                        + f"Client Node: {seed} | Teddiursa IRC Client: User has joined. DL Teddiursa IRC Client @ https://github.com/6100m/Teddiursa-IRC-Client/",
                    )
                else:
                    print("type 1 --- flag 0 flashed")
            if "433" in res:
                ins.send("USER", "{} * * :{}".format("_" + usr, "_" + usr))
                ins.send("NICK", "_" + usr)
                if config["debugflag3"] == true:
                    ins.send(
                        "PRIVMSG",
                        f"{ch} :"
                        + f"Client Node: {seed} | Teddiursa IRC Client: Got code 433.",
                    )
                else:
                    print("type 2 --- flag 0 flashed")
            if "PING" in res:
                ins.send("PONG", ":" + res.split(":")[1])
                if config["debugflag4"] == true:
                    ins.send(
                        "PRIVMSG",
                        f"{ch} :"
                        + f"Client Node: {seed} | Teddiursa IRC Client: Testing ping....",
                    )

                else:
                    print("type 3 --- flag 0 flashed")
            if "366" in res:
                flg = True
                if config["debugflag5"] == true:
                    ins.send(
                        "PRIVMSG",
                        f"{ch} :"
                        + f"Client Node: {seed} | Teddiursa IRC Client: Got code 366.",
                    )
                else:
                    print("type 4 --- flag 0 flashed")
        a_int = 0
        while cmd != "/quit":
            cmd = input("< {}> ".format(usr)).strip()
            if a_int <= 2:
                a_int = a_int + 1
            else:
                a_int = a_int - 3
            lcd.printline(a_int, cmd)
            if cmd == "/quit":
                ins.send("QUIT", "Good bye!")
            if cmd == "//refresh":
                for x in range(0, 3):
                    lcd.printline(x, "")
            # Disabled by 6100m
            # threading.thread.start_new_thread( refresh, ("Thread-1", 2, ) )
            ins.msgr(cmd)
            run = threading.Thread(target=log)
            run.daemon = True
            clr()
            run.start()
