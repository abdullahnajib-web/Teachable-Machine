from machine import SoftI2C, Pin, UART, PWM
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from ht16k33Matrix import HT16K33Matrix
from time import sleep_ms

buzzer = PWM(Pin(5, Pin.OUT))
buzzer.freq(1)
buzzer.duty(1)

uart = UART(2, tx=17, rx=16)
uart.init(9600, bits=8, parity=None, stop=1)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, 0x20, 2, 16)

display = HT16K33Matrix(i2c)
display.set_brightness(10)
display.set_angle(0)

display.clear().draw()
display.set_character(ord('-'), True).draw()


result=255
last =0
lcd.clear()
lcd.putstr("-")


while True:
    if uart.any() > 0:        
        result = ord(uart.read())
        
        if last != result :
            
            lcd.clear()
            display.clear().draw()
            
            #LCD
            if result == 10:
                lcd.putstr("Shield")
            elif result == 11:
                lcd.putstr("Neopixel")                
            elif result == 12:
                lcd.putstr("-")
            elif result == 13:
                lcd.putstr("Wheel")

            #dot matrix
            elif result == 0:
                display.set_character(ord('A'), True).draw()
            elif result == 1:
                display.set_character(ord('B'), True).draw()
    
            #buzzer
            elif result == 3:
                buzzer.freq(3000)
                buzzer.duty(512)
                sleep_ms(200)
                buzzer.duty(0)
                result = 255
            elif result == 4:
                buzzer.freq(2000)
                buzzer.duty(512)
                sleep_ms(200)
                buzzer.duty(0)
                result = 255
            elif result == 5:
                buzzer.freq(1000)
                buzzer.duty(512)
                sleep_ms(200)
                buzzer.duty(0)
                result = 255

    last = result            
    while uart.any() > 0:
        uart.read()
                


