import Adafruit_BBIO.PWM as PWM

SERVO_L = ""
SERVO_R = ""

PWM.stop(SERVO_L)
PWM.stop(SERVO_R)
PWM.cleanup()
