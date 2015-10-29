import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time

ADC.setup()

SENSOR = " "                  #SOMENTE UM SENSOR QUE VAI SEGUIR A LINHA
SENSOR_FRONT = " "            #PINO SENSOR FRONTAL
SENSOR_FLAG = " "
MOTOR_L = "P8_13"      #PINO MOTOR ESQUERDO
MOTOR_R = "P9_14"      #PINO MOTOR DIREITO

V_BASE = 60   # de 0 a 100

KP = 1.5
KI = 4
KD = 2.5

MAX = 70     
MIN = 0
MEAN = (MAX + MIN)/2

DELAY = 0.01
TOLERANCE = 1

TARGET = 50        #DE 0 A 55
FLAG_TARGET = 45   #DETECTA A FLAG
FLAG_DELAY = 2000

i = 0  #global 

def PID():
	lastErr = 0
	error = ADC.read(SENSOR_R) - MEAN
	p = error * KP
	global i += (((error - lastErr) / DELAY * KD) / (DELAY/1000)
	lastErr = error
	pid = p + i + d
	return pid

count = True  #global
time = - TOLERANCE #global

while(True):
	if ADC.read(SENSOR_FRONT) < TARGET:
		PWM.stop(MOTOR_L)
		PWM.stop(MOTOR_R)
		global time = time.time()		
	else:
		if ADC.read(SENSOR_FLAG) > FLAG_TARGET:
			if count:
				if time.time() < time + TOLERANCE:
					PWM.stop(MOTOR_L)
					PWM.set_duty_cycle(MOTOR_R, 20)
					time.sleep(2)
					global time = time.time()
					while time.time() < time + FLAG_DELAY:
						if ADC.read(SENSOR_FRONT) < TARGET:
							PWM.stop(MOTOR_L)
							PWM.stop(MOTOR_R)
						else:
							pid = PID()
							PWM.set_duty_cycle(MOTOR_L, V_BASE + pid)
							PWM.set_duty_cycle(MOTOR_R, V_BASE - pid)
							time.sleep(DELAY)
					while ADC.read(SENSOR_FLAG) < FLAG_TARGET:
						pid = PID()
						PWM.set_duty_cycle(MOTOR_L, V_BASE + pid)
						PWM.set_duty_cycle(MOTOR_R, V_BASE - pid)
						time.sleep(DELAY)
					global time = time.time()
					while time.time() < time + FLAG_DELAY:
						pid = PID()
						PWM.set_duty_cycle(MOTOR_L, V_BASE + pid)
						PWM.set_duty_cycle(MOTOR_R, V_BASE - pid)
						time.sleep(DELAY)
					PWM.set_duty_cycle(MOTOR_L, 40)
					PWM.set_duty_cycle(MOTOR_R, 20)
					time.sleep(0.5)
				else:
					global time = time.time()
					while time.time() < time + FLAG_DELAY:
						if ADC.read(SENSOR_FRONT) < TARGET:
							PWM.stop(MOTOR_L)
							PWM.stop(MOTOR_R)
						else:
							pid = PID()
							PWM.set_duty_cycle(MOTOR_L, V_BASE - pid)
							PWM.set_duty_cycle(MOTOR_R, V_BASE + pid)
							time.sleep(DELAY)
					count = False
			else:
				global time = time.time()
				while time.time() < time + FLAG_DELAY:
					if ADC.read(SENSOR_FRONT) < TARGET:
						PWM.stop(MOTOR_L)
						PWM.stop(MOTOR_R)
					else:
						pid = PID()
						PWM.set_duty_cycle(MOTOR_L, V_BASE - pid)
						PWM.set_duty_cycle(MOTOR_R, V_BASE + pid)
						time.sleep(DELAY)
