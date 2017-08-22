#!/usr/bin/env python

import sys
import serial

ports = {'COM3':{'baudrate':38400, 'timeout':1}, 'COM4':{'baudrate':38400, 'timeout':1}, 'COM6':{'baudrate':38400, 'timeout':1}}

commands = {
	'DATAMODE':{'commport':'COM3', 'command':'MD6;'},
	'POWER20':{'commport':'COM3', 'command':'PC020;'},
	'AMPSTANDBY':{'commport':'COM6', 'command':'^OS0;'},
	'AMPOPERATE':{'commport':'COM6', 'command':'^OS1;'},
	'USB':{'commport':'COM3', 'command':'MD2;'},
	'VOX':{'commport':'COM3', 'command':'SWH09;'},
	'PTT':{'commport':'COM3', 'command':'SWH09;'},
	'DATASUBMODEA':{'commport':'COM3', 'command':'DT0;'},
	'DUMMYLOAD':{'commport':'COM4', 'command':'AN2;'},
	'ANTENNA1':{'commport':'COM4', 'command':'AN1;'},
}

command_sequences = {
	'SETDATAMODE':['DATAMODE', 'DATASUBMODEA', 'POWER20', 'AMPSTANDBY'],
	'SETMARS':['AMPOPERATE', 'POWER20', 'PTT', 'USB'],
	'DUMMYLOAD':['DUMMYLOAD'],
	'ANTENNA1':['ANTENNA1'],
}

openports = {}

def openCommPorts(ports):
	for k1, v1 in ports.iteritems():
		ser = serial.Serial(port=k1, baudrate=v1['baudrate'], timeout=v1['timeout'])
		openports[k1] = ser

def closeCommPorts(openports):
	for k, v in openports.iteritems():
		v.close()

def runCommands(command_sequence):
	command_names = command_sequences[command_sequence]
	for command_name in command_names:
		print(commands[command_name])
		openports[commands[command_name]['commport']].write(commands[command_name]['command'])

def runComms(command_sequence):
	openCommPorts(ports)
	runCommands(command_sequence)
	closeCommPorts(openports)

if __name__ == "__main__":
   runComms(sys.argv[1])
