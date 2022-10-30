from liquidcrystal_i2c import LiquidCrystal_I2C
from json import load
from threading import Thread
from requests import get


def TimePrint(key, dup):
    while key == dup:
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(0, "%H:%M:%S")


def TempPrint(lst, resp=response.json()["main"]["temp"]):
    while lst[0]["key2_main"] == lst[0]["key2_mirror"]:
        if get(data[3]).status_code == 200:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(1, resp)


if __name__ == "__main__":
    lst = [
        load(open("./keys.json", "rb")),
        load(open("./api.json", "rb")),
        load(open("./location.json", "rb")),
        f"{data[1]['URL']}?q={data[2]['CITY']}&appid={data[1]['API_KEY']}",
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
            for num in range(2, 3), data in ["Bootup Complete!", "WeatherPi OS v0.2"]:
                LiquidCrystal_I2C(0x27, 1, numlines=4).printline(num, data)
            Thread(target=TempPrint, args=(lst)).Start()
            Thread(target=TimePrint, args=(lst[0]["key1"], lst[0]["key1_dup"])).Start()
            Thread(target=TempPrint, args=(lst)).Join()
            Thread(target=TimePrint, args=(lst[0]["key1"], lst[0]["key1_dup"])).Join()
