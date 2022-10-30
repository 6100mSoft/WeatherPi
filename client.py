from liquidcrystal_i2c import LiquidCrystal_I2C
from json import load
from threading import Thread
from requests import get


def TimePrint(key, dup):
    while key == dup:
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(2, "%H:%M:%S")


def TempPrint(lst, a_dict, resp=response.json()["main"]["temp"]):
    while lst[0]["key2_main"] == lst[0]["key2_mirror"]:
        if get(a_dict[4]).status_code == 200:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(3, resp)


if __name__ == "__main__":
    lst = [
        load(open("./keys.json", "rb")),
        load(open("./api.json", "rb")),
        load(open("./location.json", "rb")),
    ]
    a_dict = [
        "WeatherPi OS v0.2.1",
        "Initilization Status:",
        "Init Complete!",
        "Type start and press enter to start!",
        f"{lst[1]['URL']}?q={lst[2]['CITY']}&appid={lst[1]['API_KEY']}",
    ]
    for n in range(0, 3):
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(n, a_dict[n])
    if input("Listening....") == "start":
        while key["key3_main"] == key["key3_mirror"]:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(1, "Bootup Complete!")
            Thread(target=TempPrint, args=(lst)).Start()
            Thread(target=TimePrint, args=(lst[0]["key1"], lst[0]["key1_dup"])).Start()
            Thread(target=TempPrint, args=(lst)).Join()
            Thread(target=TimePrint, args=(lst[0]["key1"], lst[0]["key1_dup"])).Join()
