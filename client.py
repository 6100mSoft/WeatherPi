from liquidcrystal_i2c import LiquidCrystal_I2C
from time import sleep
from json import load
import sys
import threading
import requests

def ClearScreen():
    LogToScreen(1, "Clearing in 10 seconds.")
    sleep(10)
    for x in range(0, 3): LogToScreen(x, "")
 
def LogToScreen(msg, integer_data):
      LiquidCrystal_I2C(0x27, 1, numlines=4).printline(integer_data, "< {}> {}".format(msg[1].split("!")[0], msg[2].strip()))

def PrintTimeConstantly():
    with open("./keys.json", "rb") as keys_list: config = json.load(keys_list)
    while config["key1_main"] == config['key1_mirror']:
        LogToScreen(0, now.strftime("%H:%M:%S"))
        sleep(1)
        lcd.printline(0, "")

def PrintWeatherConstantly():
    # Based off of 
    # https://www.tutorialspoint.com/find-current-weather-of-any-city-using-openweathermap-api-in-python
    with open("./api.json", "rb") as api_conf: api_config = load(api_conf)
    with open("./location.json", "rb") as loc_conf: locator_config = load(loc_conf)
    with open("./keys.json", "rb") as key_conf: key_config = load(key_conf)
    while config["key2_main"] == config['key2_mirror']:
        if requests.get(f"{api_config['API_URL'}?q={locator_config['CITY']}&appid={api_config['API_KEY']}").status_code == 200:
                LogToScreen(1, response.json()['main']['temp'])
                sleep(96)
                LiquidCrystal_I2C(0x27, 1, numlines=4).printline(1, "")

def BootupIsComplete(): 
    LogToScreen(3, "Complete! | WeatherPi OS v0.1")

if __name__ == "__main__":
    with open("./keys.json", "rb") as key_configuration: key_json = json.load(key_configuration)
    while key_json['key3_main'] == key_json['key3_mirror']:
        LogToScreen(0, "WeatherPi Client")
        LogToScreen(1, "Type start and press enter to start!")
        LogToScreen(2, "Initilization Status:")
        LogToScreen(3, "Init Complete!")
        if input("Listening....") == "enter":
            ClearScreen()
            t1 = threading.Thread(target=PrintWeatherConstantly)
            t2 = threading.Thread(target=PrintTimeConstantly)
            t3 = threading.Thread(target=BootupIsComplete)
            LogToScreen(2, "Bootup Status:")
            LogToScreen(3, "Bootup is beginning")
            sleep(24)
            ClearScreen()
            t1.Start()
            t2.Start()
            t3.Start()
            t3.Join()
            t2.Join()
            t1.Join()
       else: sys.exit(1)
