#!/usr/bin/env python

from time import sleep
from flask import Flask, abort, request
from uuid import getnode as get_mac
import re
import os
import logging

print("*** If you are seeing many lines with 'fake_rpi.RPi' someone forget " \
      "to switch back to RPi dependencies (still on the fake_rpi module) ***")
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    # from fake_rpi.RPi import GPIO as GPIO
except RuntimeError:
    logger.error("""Error importing RPi.GPIO!  This is probably because you 
                 need superuser privileges.  You can achieve this by using
                 'sudo' to run your script""")


app = Flask(__name__)


pulse_length = 0.1
clear_sleep = 0.3
gpio_list = [12,16,18,22,32,36,38,40] #where 40 is reset
valid_input = '1,2,3,.'
segment_map = {
    '0': [12,16,18,22,32,36],
    '1': [16,18],
    '2': [12,16,22,32,38],
    '3': [12,16,18,22,38],
    '4': [16,18,36,38],
    '5': [12,18,22,36,38],
    '6': [12,18,22,32,36,38],
    '7': [12,16,18],
    '8': [12,16,18,22,32,36,38],
    '9': [12,16,18,36,38],
    'A': [12,16,18,32,36,38],
    'B': [18,22,32,36,38],
    'C': [12,22,32,36],
    'D': [16,18,22,32,38],
    'E': [12,16,18,22,38],
    'F': [12,32,36,38],
    '.': [40],
    ' ': [40],
}
active = ' '

def enable(hex, duration):
    global active
    segments = segment_map.get(hex)
    if segments != None:
        active = hex
        GPIO.output(segments, GPIO.HIGH)
        sleep(duration)
        GPIO.output(segments, GPIO.LOW)
    else:
        logging.info("Unknown character '%s'", hex)

@app.route('/clear')
def clear():
    enable('.', 1) #pulse_length)
    sleep(clear_sleep)
    return "cleared"

@app.route('/activate/<hex>')
def hello(hex):
    hex = hex.upper()
    matchObj = re.match( r'[1-3\.]', hex)
    if matchObj:
        clear()
        enable(hex, pulse_length)
        return "Activated %s" % hex
    else:
        return "invalid input. Only %s are accepted" % valid_input

@app.route('/')
def index():
    global active
    mac = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    return '{mac:"%s",active:"%s"}' % (mac,active)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/shutdown', methods=['POST','GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    os.system('sudo shutdown -r now')
    return 'Server shutting down...'

def bootup():
    sleepSec = 0.3

    clear()
    enable('3', pulse_length)
    sleep(sleepSec)
    clear()
    enable('2', pulse_length)
    sleep(sleepSec)
    clear()
    enable('1', pulse_length)
    sleep(sleepSec)
    clear()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_list, GPIO.OUT)
    bootup()
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
