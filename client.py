from liquidcrystal_i2c import LiquidCrystal_I2C
from time import sleep
from json import load
from threading import Thread
from os import _exit
from requests import get

def LogToScreen(line_num, msg_data): LiquidCrystal_I2C(0x27, 1, numlines=4).printline(line_num, msg_data)
    
def PrintTimeConstantly(main, mirror): while main == mirror: LogToScreen(0, "%H:%M:%S"))

def PrintWeatherConstantly():
    a_dict = [load(open("./api.json", "rb")), load(open("./location.json", "rb")), load(open("./keys.json", "rb"))]
    while key["key2_main"] == key['key2_mirror']:
        if get(f"{a_dict[0]['API_URL']}?q={a_dict[1]['CITY']}&appid={a_dict[2]['APIKEY']}").status_code == 200:
        	LogToScreen(1, response.json()['main']['temp'])

if __name__ == "__main__":
    with open("./keys.json", "rb") as key_json: key = load(key_json)
    while key['key3_main'] == key['key3_mirror']: for num in range(0, 3), data in ["WeatherPi Client",
	"Type start and press enter to start!", "Initilization Status:", "Init Complete!"]: LogToScreen(num, data)
        if input("Listening....") == "start":
	    for num in range(2, 3), data in ["Bootup Status:", "Bootup is beginning"]: LogToScreen(num, data)
            sleep(24)
            for num in range(2, 3), data in ["Bootup Status:", "Complete! | WeatherPi OS v0.1"]: LogToScreen(num, data)
            Thread(target=PrintWeatherConstantly).Start()
            Thread(target=PrintTimeConstantly, args=(key['key1_main'], key['key1_mirror'])).Start()
            Thread(target=PrintWeatherConstantly).Join()
            Thread(target=PrintTimeConstantly, aargs=(key['key1_main'], key['key1_mirror'])).Join()
       else: _exit(24)
