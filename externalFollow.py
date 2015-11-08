import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

SENSOR = ""
SERVO_L = ""
SERVO_R = ""

TARGET = 

HIGH_DUTY_CYCLE = 
LOW_DUTY_CYCLE = 

PWM.start(SERVO_L, 0, 20)
PWM.start(SERVO_R, 0, 20)

while(True):
	if(ADC.read(SENSOR) < TARGET): #Line detected
		PWM.set_duty_cycle(SERVO_L, HIGH_DUTY_CYCLE)
		PWM.set_duty_cycle(SERVO_R, LOW_DUTY_CYCLE)
	else:
		PWM.set_duty_cycle(SERVO_R, HIGH_DUTY_CYCLE)
		PWM.set_duty_cycle(SERVO_L, LOW_DUTY_CYCLE)
