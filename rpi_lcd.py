import pcd8544
import RPIO

class LCD(pcd8544.LCD):
	# button numbers
	BUTTON_1 = 4
	BUTTON_2 = 17
	BUTTON_3 = 21
	BUTTON_4 = 22
	# event type
	BUTTON_UP = 1
	BUTTON_DOWN = 0
	BUTTON_EITHER = 2

	def __init__(self, backlight_pin=24):
		RPIO.setwarnings(False)
		PCD8544.LCD.__init__(self)
		self._backlight_pin = backlight_pin
	
	def initialize(self):
		""" sets up the rpi status board pins"""
		PCD8544.LCD.initialize(self)
		RPIO.setup(self._backlight_pin, RPIO.OUT, initial=RPIO.LOW)
	
	def set_backlight(self, enabled=True):
		""" enables or disable the backlight leds"""
		if enabled:
			RPIO.output(self._backlight_pin, RPIO.HIGH)
		else:
			RPIO.output(self._backlight_pin, RPIO.LOW)

	def add_button_callback(self, button, function, event=BUTTON_DOWN, threaded=True):
		""" attaches a calback function to the button interrupt

		The callback receives two arguments, the button number (ie BUTTON_1),
		and the value of the button (ie BUTTON_UP or BUTTON_DOWN).

		Event determines if this assigns to BUTTON_UP or BUTTON_DOWN or BUTTON_EITHER.

		If threaded is True, the interrupt will spawn a new thread, otherwise
		this thread will be used and no other interrupts can occur while this
		one is being serviced.
		"""
		if event == LCD.BUTTON_DOWN:
			edge = 'falling'
		elif event == LCD.BUTTON_UP:
			edge = 'rising'
		elif event == LCD.BUTTON_EITHER:
			edge = 'both'
		RPIO.add_interrupt_callback(button, function, edge, RPIO.PUD_UP, threaded, 20)

	def delete_button_callback(self, button):
		""" deletes all callbacks set to button event"""
		RPIO.del_interrupt_callback(button)

	def wait_for_buttons(self, threaded=True):
		""" waits for button interrupts to occur
		If threaded is True, this polling is done in a separate thread, if
		False, it will block forever, handling events"""
		RPIO.wait_for_interrupts(threaded)

