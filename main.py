# from RPLCD.i2c import CharLCD

# lcd = CharLCD('PCF8574', 0x27, cols=40, rows=4)
# lcd.backlight_enabled = True

# lcd.write_string('Hello, World 1!\n') 

# lcd.write_string('Hello, World 2!\n') 

# lcd.write_string('Hello, World 3!\n') 

# lcd.write_string('Hello, World 4!\n') 


## https://bitbucket.org/kosci/charlcd/src/master/
from charlcd import buffered as lcd
from charlcd.drivers.i2cm import I2C as I2CM

i2cm_interface = I2CM(0x27, 1)
i2cm_interface.pins['E2'] = 1

lcd_writer = lcd.CharLCD(40, 4, i2cm_interface, 0, 0)

lcd_writer.init()
lcd_writer.stream('Why do hardware engineers love I2C? Because this brilliant two-wire protocol allows effortless communication between your chips. It keeps PCB layouts efficient.')
lcd_writer.flush()



