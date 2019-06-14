# seven_segment_controller
Controller software for the 7-segment display. This normally run on a RaspberryPI 3

Setup instructions
------------------
To install all dependencies of this server and be ready to run it, all you have to do is
    python setup.py install

In case the line above fails because you don't have python installed: [https://docs.python-guide.org/starting/installation/]
If you are hitting some 'source/py_gpio.c' exceptions during the setup, open setup.py & seven-segment.py to use the 'dev mode' dependencies.

Running Server
------------------
The server can easily be started by using either one of the commands below:
    python seven-segment.py
    ./seven-segment.py

Development mode
------------------
RaspberryPI libraries for GPIO are not available on non-raspberry pi computer. Fortunately, Kevin J. Walchko created a 'fake_rpi' project: <https://github.com/MomsFriendlyRobotCompany/fake_rpi/> that emulates the RaspberryPI libraries for GPIO without needing them. Thank you Kevin! If you are trying to develop against this codebase on any other computer, open 'setup.py' & 'seven-segment.py' to switch the dependencies from 'RPi' to 'fake_rpi'.

Communication protocol
------------------
The following API are available to talk to the seven-segment controller:

## Rest API
A REST server running on port 5000 is surfacing the following routes: 
* [/](/) -> Returns a string representing the current status of the controller
* [/ping](/ping) -> Respond with 'pong'. Useful for testing that the controller is up & running
* [/clear](/clear)  -> Reset all vanes of the 7-segment in 'off' position and returns 'cleared'
* [/activate/[1-3]](/activate/1) -> Activate the set of vanes needed to represent the character 1, 2 or 3 (Do not send the square bracket!)
* [/shutdown](/shutdown) -> Shuts down the raspberry pi controller. RPi have a tendency of corrupting their microSD so use this for a clean shutdown

## NMEA 0183 API
* RXSSC: Activate the set of vanes needed to represent the character 1, 2 or 3 (Do not send the square bracket!). 
  * Format: '$RXSSC,[A-C],[1-3]*CC'
  * Example: '$RXSSC,A,1*39'
* RXSTA: Ask for the active character on the seven segment. 
  * Format: '$RXSTA,A*CC'
  * Example: '$RXSTA,A*21'

  