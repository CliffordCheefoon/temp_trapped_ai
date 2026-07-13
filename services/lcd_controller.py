import re

from RPLCD.i2c import CharLCD
from charlcd import direct as lcd
from charlcd.drivers.i2cm import I2C as I2CM

LCD_BACKPACK_I2C_ADDR = 0x27
LCD_BACKPACK_CONTROLLER = "PCF8574"
LCD_CHAR_ROWS = 4
LCD_CHAR_COLS = 40



class LCDController:
    def __init__(self) -> None:
        self.lcd_backlight_controller = CharLCD(LCD_BACKPACK_CONTROLLER, LCD_BACKPACK_I2C_ADDR, cols=LCD_CHAR_COLS, rows=LCD_CHAR_ROWS)
        i2cm_interface = I2CM(LCD_BACKPACK_I2C_ADDR, 1)
        ##manually set the Enable Chip 2 pin, as the library does not do this automatically. Needed for dual chip LCDs such as the 40x4.
        i2cm_interface.pins['E2'] = 1 
        self.lcd_writer_controller = lcd.CharLCD(LCD_CHAR_COLS, LCD_CHAR_ROWS, i2cm_interface, 0, 0)
        self.lines: list[str] = [""]
        self.reset()


    def set_backlight(self, enabled: bool) -> None:
        self.lcd_backlight_controller.backlight_enabled = enabled

    def reset(self) -> None:
        self.lcd_writer_controller.init()


    def write_string(self, incoming_str: str) -> None:
        no_breaks = re.sub(r'[\r\n]+', ' ', incoming_str)
        cleaned_text = re.sub(r'[^a-zA-Z0-9 .,!?\'-]', '', no_breaks)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        last_line = self.lines[-1]
        if len(last_line) + len(cleaned_text) < LCD_CHAR_COLS:
            write_col = len(self.lines) - 1
            write_row = len(self.lines[-1])
            self.lcd_writer_controller.write(cleaned_text, write_col, write_row)
            self.lines[-1] += cleaned_text

        else:
            #create a new row
            number_of_rows = len(self.lines)
            if number_of_rows < LCD_CHAR_ROWS:
                write_col = len(self.lines) - 1
                write_row = 0
                self.lcd_writer_controller.write(cleaned_text, write_col, write_row)
                self.lines.append(cleaned_text)
            else:
                self.lines.append(cleaned_text)
                self.reset()
                self.lines = self.lines[-LCD_CHAR_ROWS:]
                for i, line in enumerate(self.lines):
                    self.lcd_writer_controller.write(line, i, 0)





