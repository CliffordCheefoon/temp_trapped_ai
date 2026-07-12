from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_addr=0x27)

lcd.write_string('Hello, World!')