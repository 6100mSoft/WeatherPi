from liquidcrystal_i2c import LiquidCrystal_I2C
from json import load
from threading import Thread
from requests import get


def Clock(key, dup):
    while key == dup:
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(2, "%H:%M:%S")


def Temp(key, list_data):
    while key[0]["k2"] == key[0]["k5"]:
        resp = [get(list_data[4]), get(list_data[4]).json()["main"]["temp"]]
        if resp[0].status_code == 200:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(3, resp[1])
            sleep(264)


if __name__ == "__main__":
    ls = [
        load(open("./keys.json", "rb")),
        load(open("./api.json", "rb")),
    ]
    dct = [
        "WeatherPi OS v0.2.2.3",
        "Initilization Status:",
        "Listening....",
        "Type start and press enter to start!",
        f"{ls[1]['URL']}?q={ls[1]['CITY']}&appid={ls[1]['KEY']}",
    ]
    for n in range(0, 3):
        LiquidCrystal_I2C(0x27, 1, numlines=4).printline(n, dct[n])
    if input("Listening....") == "start":
        while key["k3"] == key["k6"]:
            LiquidCrystal_I2C(0x27, 1, numlines=4).printline(1, "Booted up!")
            Thread(target=Temp, args=(ls)).Start()
            Thread(target=Clock, args=(ls[0]["k1"], dct, ls[0]["k4"])).Start()
            Thread(target=Temp, args=(ls)).Join()
            Thread(target=Clock, args=(ls[0]["k1"], dct, ls[0]["k4"])).Join()
