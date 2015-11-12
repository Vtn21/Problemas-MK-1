import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time

SENSOR = "P9_38"
MOTOR_L = "P9_14"
MOTOR_R = "P8_13"
SENSOR_FRONT = "P9_39"
SENSOR_FLAG = "P9_40"

HIGH_L = 7
LOW_L = 28
HIGH_R = 1
LOW_R = 12

time = 0
count = True

ADC.setup()
PWM.start(MOTOR_L, 0, 30)
PWM.start(MOTOR_R, 0, 90)

while (1):
	if(ADC.read(SENSOR_FRONT) > 0.08): #dummy detected
		PWM.set_duty_cyle(MOTOR_R, 0)
		PWM.set_duty_cycle(MOTOR_L, 0)
	else: 
		if(ADC.read(SENSOR_FLAG) < 0.4): #flag detected
		
		else: #flag not detected
			if(ADC.read(SENSOR) < 0.4):
				PWM.set_duty_cycle(MOTOR_L, HIGH_L)
				PWM.set_duty_cycle(MOTOR_R, LOW_R)
			else:
				PWM.set_duty_cycle(MOTOR_R, HIGH_R)
				PWM.set_duty_cycle(MOTOR_L, LOW_L)
				
