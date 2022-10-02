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
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
        lcd.printline(i, "< {}> {}".format(
            msg[1].split("!")[0], msg[2].strip()))

def PrintTimeConstantly():
    with open("./keys.json", "rb") as f:
            config = json.load(f)
    while config["key1_main"] == config['key1_mirror']:
        LogToScreen(0, now.strftime("%H:%M:%S"))
        time.sleep(1)
        for i in range(0, 1): lcd.printline(i, "")

def PrintWeatherConstantly():
    # Based off of https://www.tutorialspoint.com/find-current-weather-of-any-city-using-openweathermap-api-in-python
    BASE_URL = 
    with open("./api.json", "rb") as api_conf:
        api_config = json.load(api_conf)
    with open("./location.json", "rb") as loc_conf:
        locator_config = json.load(loc_conf)
    with open("./keys.json", "rb") as key_conf:
        key_config = json.load(key_conf)
    while config["key2_main"] == config['key2_mirror']:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={locator_config['CITY']}&appid={api_config['API_KEY']}"
        )
        if response.status_code == 200:
            main = response.json()['main']
            LogToScreen(1, main['temp'])
            time.sleep(1)
            for x in range(0, 1): lcd.printline(i, "")

if __name__ == "__main__":
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    lcd.printline(0, "WeatherPi Client")
    lcd.printline(1, "Type start and press enter to start!")
    lcd.printline(2, "Initilization Status:")
    lcd.printline(3, "Init Complete!")
    ClearScreen()
    for num in range(0, 1): lcd.printline(num, "")
    t1 = threading.Thread(target=PrintWeatherConstantly)
    t2 = threading.Thread(target=PrintTimeConstantly)
    lcd.printline(2, "Bootup Status:")
    lcd.printline(3, "Bootup is beginning")
    t1.Start()
    t2.Start()
    lcd.printline(3, "Complete! | WeatherPi OS v0.1")
