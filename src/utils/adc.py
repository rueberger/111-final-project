import numpy as np
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# conversion factor
ADC_TO_V = 3.3 / 1023

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def read_adc(adcnum=0,
            clockpin=SPICLK,
            mosipin=SPIMOSI,
            misopin=SPIMISO,
            cspin=SPICS):
    """
    adcnum is the MCP3008 channel being used, 0 is on the left
    the other params are pin settings - for now just using the default from the tutorial
    IMPORTANT: do not load with more than 3.3V
    """

    if ((adcnum > 7) or (adcnum < 0)):
            return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(mosipin, True)
            else:
                    GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                    adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout * ADC_TO_V

def readadc_avg(pin=0, itrs=10):
    """
    averages itrs measurements, returns
    """
    return np.mean([read_adc(pin) for _ in xrange(itrs)])

def read_while(itr=500):
    for _ in xrange(500):
        print read_adc()
        time.sleep(0.5)

def read_rms(itrs=100):
    # see how long this many iterations takes
    measurements = np.array([read_adc() for _ in xrange(itrs)])
    return np.sqrt(np.mean(measurements ** 2))