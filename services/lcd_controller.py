import re

from charlcd import direct as lcd
from charlcd.drivers.i2cm import I2C as I2CM

LCD_BACKPACK_I2C_ADDR = 0x27
LCD_BACKPACK_CONTROLLER = "PCF8574"
LCD_CHAR_ROWS = 4
LCD_CHAR_COLS = 40



class LCDController:
    def __init__(self) -> None:
        i2cm_interface = I2CM(LCD_BACKPACK_I2C_ADDR, 1)
        ##manually set the Enable Chip 2 pin, as the library does not do this automatically. Needed for dual chip LCDs such as the 40x4.
        i2cm_interface.pins['E2'] = 1 
        self.lcd_writer_controller = lcd.CharLCD(LCD_CHAR_COLS, LCD_CHAR_ROWS, i2cm_interface, 0, 0)
        self.lines: list[str] = []
        self.reset()



    def reset(self) -> None:
        self.lcd_writer_controller.init()
        self.lines = [""]


    def write_string(self, incoming_str: str) -> None:
        if incoming_str == '':
            return
        cleaned_text = re.sub(r'[\r\n]+', ' ', incoming_str)


        last_line = self.lines[-1]
        if len(last_line) + len(cleaned_text) <= LCD_CHAR_COLS:
            write_row = len(self.lines) - 1
            write_col = len(last_line)
            self.lcd_writer_controller.write(cleaned_text, write_col, write_row)
            self.lines[-1] += cleaned_text

        else:
            #create a new row
            number_of_rows = len(self.lines)
            cleaned_text = cleaned_text.lstrip()
            
            if number_of_rows < LCD_CHAR_ROWS:
                write_row = len(self.lines) - 1 + 1 # new line
                write_col = 0
                self.lcd_writer_controller.write(cleaned_text, write_col, write_row)
                self.lines.append(cleaned_text)
            else:
                self.reset()
                self.lines[-1] += cleaned_text
                self.lcd_writer_controller.write(cleaned_text, 0, 0)






