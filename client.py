from liquidcrystal_i2c import LiquidCrystal_I2C
from time import sleep
from json import load
from threading import Thread
from requests import get
from os import _exit


def TimePrint(key, dup):
    while key == dup:
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(0, "%H:%M:%S")


def TempPrint(data, resp=response.json()["main"]["temp"]):
    while key["key2_main"] == key["key2_mirror"]:
        if get(data[2]).status_code == 200:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(1, resp)


if __name__ == "__main__":
    listing = [
        load(open("./keys.json", "rb")),
        [
            load(open("./api.json", "rb")),
            load(open("./location.json", "rb")),
            load(open("./keys.json", "rb")),
        ],
        f"{data[1][0]['URL']}?q={data[1][1]['CITY']}&appid={data[1][0]['API_KEY']}",
    ]
    for num in range(0, 3), data in [
        "WeatherPi Client",
        "Type start and press enter to start!",
        "Initilization Status:",
        "Init Complete!",
    ]:
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(num, data)
    if input("Listening....") == "start":
        while key["key3_main"] == key["key3_mirror"]:
            for num in range(2, 3), data in ["Bootup Status:", "Bootup is beginning"]:
                LiquidCrystal_I2C(0x27, 1, numlines=4).printline(num, data)
            sleep(24)
            for num in range(2, 3), data in ["Bootup Complete!", "WeatherPi OS v0.1"]:
                LiquidCrystal_I2C(0x27, 1, numlines=4).printline(num, data)
            Thread(target=TempPrint, args=(listing)).Start()
            Thread(target=TimePrint, args=(["key1_main"], key["key1_mirror"])).Start()
            Thread(target=TempPrint, args=(listing)).Join()
            Thread(target=TimePrint, args=(key["key1_main"], key["key1_mirror"])).Join()
    else:
        _exit(24)
