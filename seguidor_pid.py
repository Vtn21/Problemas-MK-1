import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time

SENSOR_L = "P9_37"
SENSOR_R = "P9_38"
MOTOR_L = "P9_14"
MOTOR_R = "P8_13"
SENSOR_FRONT = "P9_39"
SENSOR_FLAG = "P9_40"

HIGH_L = 9.8
LOW_L = 7.6
HIGH_R = 1.2
LOW_R = 6.6

time_ini = 0
count = True
TOLERANCE = 2.0

class pid:
	'proporcional,integral,derivada'

	def __init__(self,kp,ki,kd,setPoint):
		self.kp=kp
		self.ki=ki
		self.kd=kd
		self.setPoint=setPoint
		self.p=0
		self.i=0
		self.d=0
		self.err=0
		self.lastE=0
		self.pid=0
	def pidGet(self):
		return self.pid
	def pidAdd(self,Leitura):
		self.lastE=self.err
		self.err=Leitura-self.setPoint
		self.p=self.kp*self.err
		self.i=self.i+(self.err*self.ki)
		self.d=self.kd*(self.err-self.lastE)
		self.pid=self.p+self.i+self.d

pidIn = pid(1,1,1,)#definir setPoint
pidOut = pid(1,1,1,)#definir setPoint
ADC.setup()
PWM.start(MOTOR_L, 0, 50)
PWM.start(MOTOR_R, 0, 50)

def followInside():
	pidIn.pidAdd(ADC.read(SENSOR_L));
	PWM.set_duty_cycle(MOTOR_L, HIGH_L)
	PWM.set_duty_cycle(MOTOR_R, HIGH_R+pidIn.pidGet())
	
def followOutside():
	pidOut.pidAdd(ADC.read(SENSOR_R));
	PWM.set_duty_cycle(MOTOR_L, HIGH_L)
	PWM.set_duty_cycle(MOTOR_R, HIGH_R+pidOut.pidGet())
		
def stop():
	PWM.set_duty_cyle(MOTOR_R, 0)
	PWM.set_duty_cycle(MOTOR_L, 0)

while (1):
	
	
	if(ADC.read(SENSOR_FRONT) < 0.15):	 
		if(ADC.read(SENSOR_FLAG) < 0.4): #flag detected
			if(count): #bigger loop
				if(time.time() < time_ini + TOLERANCE): #dummy detected
					stop()
					time.sleep(2)
					time_ini = time.time()
					while(time.time() < time_ini + TOLERANCE):
						followInside()
					while(ADC.read(SENSOR_FLAG) > 0.4):
						followInside()
					time_ini = time.time()
					while(time.time() < time_ini + TOLERANCE):
						followInside()
				else: #dummy not detected
					time_ini = time.time()
					while(time.time() < time_ini + TOLERANCE):
						if(ADC.read(SENSOR_FRONT) > 0.15):
							stop()
						else:
							followOutside()
					count = False
			else: #smaller loop
				time_ini = time.time()
				while(time.time() < time_ini + TOLERANCE):
					if(ADC.read(SENSOR_FRONT) > 0.15):
						stop()
					else:
						followOutside()
		else: #flag not detected
			followOutside()
	else: #dummy detected	
		stop()
		time.sleep(0.05)
		if(ADC.read(SENSOR_FRONT) > 0.15):
			time_ini = time.time()
