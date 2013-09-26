import rpi_lcd
import time
import netifaces

LCD = rpi_lcd.LCD()

LCD.initialize()
LCD.set_backlight()

def le_callback(button, event):
	print 'button {0} - {1}'.format(button, event)

LCD.add_button_callback(LCD.BUTTON_1, le_callback, LCD.BUTTON_EITHER)
LCD.add_button_callback(LCD.BUTTON_2, le_callback, LCD.BUTTON_EITHER)
LCD.add_button_callback(LCD.BUTTON_3, le_callback, LCD.BUTTON_EITHER)
LCD.add_button_callback(LCD.BUTTON_4, le_callback, LCD.BUTTON_EITHER)
LCD.wait_for_buttons()

while True:
	LCD.set_cursor(0, 0)
	LCD.print_string(time.strftime('%X'))
	LCD.set_cursor(0, 1)
	LCD.print_string(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
	time.sleep(1)
