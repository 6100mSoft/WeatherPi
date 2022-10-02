import liquidcrystal_i2c
import time
import threading

def ClearScreen():
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    for x in range(0, 3):
        lcd.printline(x, "")
    LogToScreen(0, "clear func trigger pulled")
    LogToScreen(1, "Refreshing in 10 seconds......")
    for x in range(0, 3):
        lcd.printline(x, "")

def LogToScreen(msg, i):
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
        lcd.printline(i, "< {}> {}".format(
            msg[1].split("!")[0], msg[2].strip()))
if __name__ == "__main__":
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
    lcd.printline(0, "WeatherPi Client")
    lcd.printline(1, "Type start and press enter to start!")
    lcd.printline(2, "Initilization Status:")
    lcd.printline(3, "Init Complete!")
    ClearScreen()
    t1 = threading.Thread(target=print_square)
    t2 = threading.Thread(target=print_cube)
    lcd.printline(2, "Bootup Status:")
    lcd.printline(3, "Bootup is beginning")
    t1.Start()
    t2.Start()
    lcd.printline(3, "")
    lcd.printline(3, "Complete! | WeatherPi OS v0.1"
                  
