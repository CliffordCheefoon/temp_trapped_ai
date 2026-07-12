from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)

lcd.write_string('Hello, World! 1')
lcd.write_string('Hello, World! 2')
lcd.write_string('Hello, World! 3')
lcd.write_string('Hello, World! 4')