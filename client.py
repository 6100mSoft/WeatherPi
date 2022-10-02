import liquidcrystal_i2c
import time
import threading
import requests
import json

def ClearScreen():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    for x in range(0, 3): lcd.printline(x, "")
    LogToScreen(0, "clear func trigger pulled")
    LogToScreen(1, "Refreshing in 10 seconds......")
    for x in range(0, 3): lcd.printline(x, "")
 
def LogToScreen(msg, i):
        liquidcrystal_i2c.LiquidCrystal_I2C(
            0x27, 1, numlines=4).printline(i, "< {}> {}".format(
                msg[1].split("!")[0], msg[2].strip()))

def PrintTimeConstantly():
    with open("./keys.json", "rb") as keys_list: config = json.load(keys_list)
    while config["key1_main"] == config['key1_mirror']:
        LogToScreen(0, now.strftime("%H:%M:%S"))
        time.sleep(1)
        lcd.printline(0, "")

def PrintWeatherConstantly():
    # Based off of 
    # https://www.tutorialspoint.com/find-current-weather-of-any-city-using-openweathermap-api-in-python
    with open("./api.json", "rb") as api_conf: api_config = json.load(api_conf)
    with open("./location.json", "rb") as loc_conf: locator_config = json.load(loc_conf)
    with open("./keys.json", "rb") as key_conf: key_config = json.load(key_conf)
    while config["key2_main"] == config['key2_mirror']:
        api = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={locator_config['CITY']}&appid={api_config['API_KEY']}")
        if api.status_code == 200:
            LogToScreen(1, response.json()['main']['temp'])
            time.sleep(96)
            lcd.printline(1, "")

def BootupIsComplete():
    lcd.printline(3, "Complete! | WeatherPi OS v0.1")

if __name__ == "__main__":
    with open("./keys.json", "rb") as key_configuration: key_json = json.load(key_configuration)
    while key_json['key3_main'] == key_json['key3_mirror']:
        lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
        lcd.printline(0, "WeatherPi Client")
        lcd.printline(1, "Type start and press enter to start!")
        lcd.printline(2, "Initilization Status:")
        lcd.printline(3, "Init Complete!")
        ClearScreen()
        t1 = threading.Thread(target=PrintWeatherConstantly)
        t2 = threading.Thread(target=PrintTimeConstantly)
        t3 = threading.Thread(target=BootupIsComplete)
        lcd.printline(2, "Bootup Status:")
        lcd.printline(3, "Bootup is beginning")
        t1.Start()
        t2.Start()
        t3.Start()
        t3.Join()
        t2.Join()
        t1.Join()
