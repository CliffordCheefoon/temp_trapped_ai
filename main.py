# from RPLCD.i2c import CharLCD

# lcd = CharLCD('PCF8574', 0x27, cols=40, rows=4)

# lcd.write_string('Hello, World 1!\n') 

# lcd.write_string('Hello, World 2!\n') 

# lcd.write_string('Hello, World 3!\n') 

# lcd.write_string('Hello, World 4!\n') 

from charlcd import direct as lcd
from charlcd.drivers.i2c import I2C


l = lcd.CharLCD(40, 4, I2C(0x27, 1))
l.write("Hello, World 1!, Hello, World 2!, Hello, World 3!, Hello, World 4!, Hello, World 5!, Hello, World 6!, Hello, World 7!, Hello, World 8!, Hello, World 9!, Hello, World 10!, Hello, World 11!, Hello, World 12!, Hello, World 13!, Hello, World 14!, Hello, World 15!, Hello, World 16!, Hello, World 17!, Hello, World 18!, Hello, World 19!, Hello, World 20!")



