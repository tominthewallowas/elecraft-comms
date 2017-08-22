#!/usr/bin/python
# -*- coding: utf-8 -*-

# serialcommands.py

import logging
import serial

logger = logging.getLogger('SERIALCOMMANDS')
logger.setLevel(logging.ERROR)
log_format = '%(asctime)s:%(lineno)s:%(levelname)s:%(name)s:%(message)s'
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('serialcommands.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class SerialCommands(object):

    def __init__(self, ports=None):
        '''
                Given a list of a list of port names and baud rates
                will attempt to open the ports and place in a dictionary.
        '''
        self.openports = {}
        if ports:
            self.openPorts(ports)

    def openPorts(self, ports):
        '''
                Given a list of ports with port names and baud rate,
                attempt to open each port and place in the openports
                dictionary. If an exception encountered ignore that
                port.
        '''
        for comm, baudrate in ports.iteritems():
            try:
                ser = serial.Serial(port=comm, baudrate=baudrate, timeout=1)
            except serial.SerialException:
				logger.exception('SerialException')
            else:
                self.openports[comm] = ser

    def openPort(self, port, baudrate):
        '''
                Given a single port name and baud rate, attempt to open it and place
                it in the openports dictionary. If successful, return
                true, if not, return false.
        '''
        try:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        except serial.SerialException:
			logger.exception('SerialException')
        else:
            self.openports[port] = ser
            return True

    def checkPort(self, port=None):
        '''
                Assumes the ports that are open are contained within
                the self.openports list.  If not raises exception.
                Otherwise checks if the port is open.
        '''
        serialport = self.openports.get(port, None)
        if serialport:
            return serialport.is_open
        else:
            return False

    def checkPorts(self):
        '''
                Check the status on all ports in the openports dictionary
                and return each port status as a list of tuples.
        '''
        portsstatus = []
        for portname, port in self.openports.iteritems():
            portsstatus.append((portname, port.is_open))
        return portsstatus

    def closePorts(self):
        '''
                Close ports stored in openports dictionary, and destroy
                the objects.
        '''
        for portname, port in self.openports.iteritems():
            port.close()
        self.openports.clear()

    def runCommand(self, command):
        '''
                Given a list containing a named comm port and a command
                write to the port and return the result.
        '''
        #print('Command:', command)
        return self.openports[command[0]].write(command[1])
        #result = self.openports[command[0]].write(command[1])
        #print('runCommand:', result)
        # return result

    def readPort(self, command, howmany=40):
        '''
                Given a list containing a named comm port and command,
                read the number of characters requested. Defaults to 40.
        '''
        response = self.runCommand(command)
        # print(response)
        self.openports[command[0]].reset_input_buffer()
        return self.openports[command[0]].read(howmany)


if __name__ == '__main__':
	import elecraft
	commands = {
		'DATAMODE': 'COM13|MD6;',
		'POWER50': 'COM13|PC050;',
		'DATASUBMODEA': 'COM13|DT0;',
		'WWV': 'COM13|FA00010000000;',
		'TESTTOGGLE': 'COM13|SWH18;',
		'VOX': 'COM13|SWH09;'
	}
	command_sequences = {
		'SETDATAMODE': 'DATAMODE|DATASUBMODEA|POWER50',
		'WWV': 'WWV',
		'VOX': 'VOX',
		'TESTTOGGLE': 'TESTTOGGLE'
	}
	logger.debug('In Main')
	#sc = SerialCommands({'COM13':38400, 'COM4':38400, 'COM6':38400})
	sc = SerialCommands({'COM13':38400})
	#command = ['COM13', 'PC001;']
	#command = ['COM13', 'MD;']
	command = ['COM13', 'IC;']
	#sc.runCommand(command)
	response = sc.readPort(command)
	status = elecraft.listifyHexstring(response)
	print status
	sc.closePorts()
