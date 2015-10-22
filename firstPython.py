import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

motorL = #pino desconhecido
motorR = #pino desconhecido
sensorL = #pino desconhecido
sensorR = #pino desconhecido
sensorFlag = #pino desconhecido
sensorFront = #pino desconhecido

speed = 70
reduction = 10 #ajustar

GPIO.setup(motorL, GPIO.OUT)
GPIO.setup(motorR, GPIO.OUT)
GPIO.setup(sensorL, GPIO.IN)
GPIO.setup(sensorR, GPIO.IN)
GPIO.setup(sensorFlag, GPIO.IN)
GPIO.setup(sensorFront, GPIO.IN)

PWM.start(motorL,speed)
PWM.start(motorR,speed)

GPIO.add_event_detect(sensorFlag, GPIO.FALLING)

def followOut():	
	if GPIO.input(sensorR):
		PWM.set_duty_cycle(motorR, speed - reduction)
	else:
		PWM.set_duty_cycle(motorR, speed)
	return
	
def followIn():
	if GPIO.input(sensorL):
		PWM.set_duty_cycle(motorL, speed-reduction)
	else:
		PWM.set_duty_cycle(motorL, speed)
	return
	
def detect():
	global speed
	if GPIO.input(sensorFront):
		speed = 50 #ajustar
		return True
	else:
		speed = 70 #ajustar
		return False
	return
