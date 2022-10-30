from liquidcrystal_i2c import LiquidCrystal_I2C
from time import sleep
from json import load
from threading import Thread
from os import _exit
from requests import get

def LogToScreen(line_num, msg_data): 
	LiquidCrystal_I2C(0x27, 1, numlines=4).printline(line_num, msg_data)
    
def PrintTimeConstantly():
    with open("./keys.json", "rb") as keys_json: key = load(keys_json)
    while key["key1_main"] == key['key1_mirror']: LogToScreen(0, "%H:%M:%S"))

def PrintWeatherConstantly():
    with open("./api.json", "rb") as api_json: api = load(api_json)
    with open("./location.json", "rb") as loc_json: location = load(loc_json)
    with open("./keys.json", "rb") as key_json: key = load(key_json)
    while key["key2_main"] == key['key2_mirror']:
        if get(f"{api['API_URL'}?q={location['CITY']}&appid={api['APIKEY']}").status_code == 200:
        	LogToScreen(1, response.json()['main']['temp'])

if __name__ == "__main__":
    with open("./keys.json", "rb") as key_json: key = load(key_json)
    while key['key3_main'] == key['key3_mirror']: for num in range(0, 3), data in ["WeatherPi Client",
	"Type start and press enter to start!", "Initilization Status:", "Init Complete!"]: LogToScreen(num, data)
        if input("Listening....") == "start":
            t1 = Thread(target=PrintWeatherConstantly)
            t2 = Thread(target=PrintTimeConstantly)
	    for num in range(2, 3), data in ["Bootup Status:", "Bootup is beginning"]: LogToScreen(num, data)
            sleep(24)
            LogToScreen(1, "Clearing in 10 seconds.")
            sleep(10)
            for num in range(0, 3): LogToScreen(num, "")
            for num in range(2, 3), data in ["Bootup Status:", "Complete! | WeatherPi OS v0.1"]: LogToScreen(num, data)
            t2.Start()
            t3.Start()
            t3.Join()
            t2.Join()
       else: _exit(24)
