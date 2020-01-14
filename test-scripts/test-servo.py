#import statements
import RPi.GPIO as raspiGPIO
import time

#set up gpio control
raspiGPIO.setmode(raspiGPIO.BOARD)

#set up the pwm at pin 11
raspiGPIO.setup(11, raspiGPIO.OUT)
pwm = raspiGPIO.PWM(11, 50)
pwm.start(0)

#toggle the servo through its full cycle
minMaxServoPositions = [2, 12]
for position in range(minMaxServoPositions[0], minMaxServoPositions[1] + 1):
    print('Setting servo to position {} (MIN:{})(MAX:{})'.format(position, *minMaxServoPositions))
    pwm.ChangeDutyCycle(position)
    print('Waiting one second for servo to move fully.')
    time.sleep(1)

#stop and clean up
pwm.stop()
raspiGPIO.cleanup()