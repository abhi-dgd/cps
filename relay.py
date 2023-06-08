import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

rfid= SimpleMFRC522()
channel = 17

def relay_on(pin):
    GPIO.output(pin,GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin,GPIO.LOW)

while True:
      id, text = rfid.read()
      print(id)
      
      if id == 1002059512185:
        relay_on(channel)
        print(text+":Access granted")
        time.sleep(5)
        relay_off(channel)

      else:
        relay_off(channel)
        print("Not allowed...")