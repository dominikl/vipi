#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import logging
from subprocess import call
from subprocess import check_output

# Configuration
logfile = "/var/log/vpncontrol.log"
vpncmd = "/usr/local/sbin/managevpn.sh"

# Interval (in sec) to check vpn status
checkinterval = 10

# LED pin numbers (BCM)
powerledpin = 5
led1pin = 6
led2pin = 13
led3pin = 19
led4pin = 26

# Button pin numbers (BCM)
powerbuttonpin = 3 # pull down pin 3 will also start up Raspi!
button1pin = 4
button2pin = 17
button3pin = 27
button4pin = 22
# End Configuration

# Setup logger
logger = logging.getLogger('vpncontrol')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Setup GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(powerledpin, GPIO.OUT)
GPIO.setup(led1pin, GPIO.OUT)
GPIO.setup(led2pin, GPIO.OUT)
GPIO.setup(led3pin, GPIO.OUT)
GPIO.setup(led4pin, GPIO.OUT)

GPIO.setup(powerbuttonpin, GPIO.IN)
GPIO.setup(button1pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button2pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button3pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button4pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Define necessary functions
def ledOn(led):
    if not GPIO.input(int(led)):
        logger.info("set led on " + str(led))
        GPIO.output(int(led), 1)

def ledOff(led):
    if GPIO.input(int(led)):
        logger.info("set led off " + str(led))
        GPIO.output(int(led), 0)

def setVpnLed(led):
    if int(led) != 1:
        ledOff(led1pin)
    if int(led) != 2:
        ledOff(led2pin)
    if int(led) != 3:
        ledOff(led3pin)
    if int(led) != 4:
        ledOff(led4pin)

    if int(led) == 1:
        ledOn(led1pin)
    if int(led) == 2:
        ledOn(led2pin)
    if int(led) == 3:
        ledOn(led3pin)
    if int(led) == 4:
        ledOn(led4pin)

def checkvpn():
    active = check_output([vpncmd, "status"])
    if active:
        setVpnLed(active)

def connectvpn(server):
    if int(server) == 0:
        logger.info("disconnect vpn")
        call([vpncmd, "disconnect"])
    else:
        logger.info("connect vpn " + str(server))
        call([vpncmd, "connect", str(server)])

def buttonPressed(pin):
    logger.info("buttonPressed " + str(pin))

    if pin == powerbuttonpin:
        logger.info("shutting down...")
        call("shutdown -h now")

    if pin == button1pin:
        if GPIO.input(int(led1pin)):
            connectvpn(0)
        else:
            connectvpn(1)

    if pin == button2pin:
        if GPIO.input(int(led2pin)):
            connectvpn(0)
        else:
            connectvpn(2)

    if pin == button3pin:
        if GPIO.input(int(led3pin)):
            connectvpn(0)
        else:
            connectvpn(3)

    if pin == button4pin:
        if GPIO.input(int(led4pin)):
            connectvpn(0)
        else:
            connectvpn(4)

# Add button event listeners
GPIO.add_event_detect(powerbuttonpin, GPIO.BOTH, callback=buttonPressed, bouncetime=300)
GPIO.add_event_detect(button1pin, GPIO.FALLING, callback=buttonPressed, bouncetime=300)
GPIO.add_event_detect(button2pin, GPIO.FALLING, callback=buttonPressed, bouncetime=300)
GPIO.add_event_detect(button3pin, GPIO.FALLING, callback=buttonPressed, bouncetime=300)
GPIO.add_event_detect(button4pin, GPIO.FALLING, callback=buttonPressed, bouncetime=300)

# Run endless loop checking vpn status
try:
    logger.info("starting up...")
    ledOn(powerledpin)
    while True:
        checkvpn()
        time.sleep(checkinterval)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
