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

try:
	while True:
		LCD.set_cursor(0, 0)
		LCD.print_string("time: " + time.strftime('%X'))
		tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
		LCD.set_cursor(0, 1)
		LCD.print_string("temp: " + str(tempC) + " C")
		LCD.set_cursor(0, 3)
		LCD.print_string(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
		load = open("/proc/loadavg").readline().split(" ")[:3]
		LCD.set_cursor(0, 5)
		LCD.print_string(str(load[0]) + "," + str(load[1]) + "," + str(load[2]))
		time.sleep(1)
except (RuntimeError, TypeError, NameError, ValueError, IOError):
	pass
