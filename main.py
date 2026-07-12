from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27, cols=40, rows=4)

lcd.write_string('Hello, World 1!\n') 

lcd.write_string('Hello, World 2!\n') 

lcd.write_string('Hello, World 3!\n') 

lcd.write_string('Hello, World 4!\n') 
