#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPin = 13    # pin11 --- led
BtnPin = 12    # pin12 --- button

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to make led off

def loop():
	status = GPIO.HIGH
	while True:
		if GPIO.input(BtnPin) == GPIO.LOW: # Check whether the button is pressed or not.
			print 'clicked'
			status = toggle(status)
			GPIO.output(LedPin, status)  # led on
			time.sleep(.3)
		# else:
			# print 'led off...'
			# GPIO.output(LedPin, GPIO.HIGH) # led off

def toggle(status):
	if status == GPIO.HIGH:
		status = GPIO.LOW
	else:
		status = GPIO.HIGH
	return status
			
def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()