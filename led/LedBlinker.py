#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

leds = {"red": 11, "yellow": 7, "green": 12}

def setUp(LedPin):
	GPIO.setmode(GPIO.BOARD)
	if type(LedPin) is int:
		GPIO.setup(LedPin, GPIO.OUT)
		GPIO.output(LedPin, GPIO.HIGH)
	else:
		for i in LedPin.values():
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, GPIO.HIGH)

def blink(delay, times):
	if times:
		for i in range(times):
			GPIO.output(LedPin, GPIO.LOW)
			time.sleep(delay)
			GPIO.output(LedPin, GPIO.HIGH)
			time.sleep(delay)
	# destroy()

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

def setLedPin(color):
	return leds[color]

def blink_all(times):
	for i in range(times):
		for l in leds.values():
			GPIO.output(l, GPIO.LOW)
			time.sleep(.07)
			GPIO.output(l, GPIO.HIGH)
			time.sleep(.07)
	# destroy()

if __name__ == '__main__':
	LedPin = setLedPin('green')

	try:
		setUp(LedPin)
		blink(.08, 30)
		destroy()
		setUp(leds)
		blink_all(10)
		destroy()
	except KeyboardInterrupt:
		destroy()