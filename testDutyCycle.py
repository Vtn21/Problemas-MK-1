import Adafruit_BBIO.PWM as PWM

MOTOR = "P9_14"

PWM.start(MOTOR, 2, 50)

while(True):
    dutyCycle = input("Duty cycle: ")
	PWM.set_duty_cycle(MOTOR, dutyCycle)
