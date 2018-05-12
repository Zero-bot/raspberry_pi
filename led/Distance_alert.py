import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)
alert = False

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def setup_scaner():
	PIN_TRIGGER = 7
	PIN_ECHO = 11
	GPIO.setup(PIN_TRIGGER, GPIO.OUT)
	GPIO.setup(PIN_ECHO, GPIO.IN)
	print("Waiting for sensor to settle")
	time.sleep(1)

def trigger():
	PIN_TRIGGER = 7
	PIN_ECHO = 11
	GPIO.output(PIN_TRIGGER, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIGGER, GPIO.LOW)
	while GPIO.input(PIN_ECHO)==0:
		pulse_start_time = time.time()
	while GPIO.input(PIN_ECHO)==1:
		pulse_end_time = time.time()
	pulse_duration = pulse_end_time - pulse_start_time
	distance = round(pulse_duration * 17150, 2)
	print ("Distance:", distance, "cm")
	global alert
	if distance < 25:
		alert = True
		print(bcolors.FAIL + "Please stay away!" + bcolors.ENDC)
	else:
		alert = False

def start_scanning(run_event):
	setup_scaner()
	try:
		while run_event.is_set():
			trigger()
			time.sleep(1)
	except:
		print("Interrupt!")
		GPIO.cleanup()

def setup_led(run_event):
	GPIO.setup(40, GPIO.OUT)
	while run_event.is_set():
		if alert:
			GPIO.output(40, 1)
		else:
			GPIO.output(40, 0)
		time.sleep(.3)

def buzzer(run_event):
	GPIO.setup(15,GPIO.OUT)
	while run_event.is_set():
		if alert:
			GPIO.output(15,0)
			time.sleep(.3)
			GPIO.output(15,1)
			time.sleep(.2)
		else:
			GPIO.output(15,0)
			time.sleep(.5)

if __name__=='__main__':
	run_event = threading.Event()
	run_event.set()
	scanner = threading.Thread(name="scanner", target=start_scanning, args=(run_event, ))
	led = threading.Thread(name="led", target=setup_led, args=(run_event, ))
	buzz = threading.Thread(name="buzzer", target=buzzer, args=(run_event, ))
	scanner.start()
	led.start()
	buzz.start()
	try:
		while 1:
			time.sleep(.1)
	except KeyboardInterrupt:
		run_event.clear()
		scanner.join()
		led.join()
		GPIO.cleanup()
		print (bcolors.OKGREEN + "Threads successfully closed" + bcolors.ENDC)