import serial as pySerial
import time
import numpy as np

def getConnection(port, baud):
	ser = pySerial.Serial(port, baud, timeout=0.5)
	return ArduinoSerial(ser)

class ArduinoSerial:
	ser = None
	measurementsPerSecond = 1

	def __init__(self, pySerial):
		self.ser = pySerial
		time.sleep(0.5)

	def close(self):
		self.ser.close()

	def writeSerial(self, message):
		self.ser.write( str(message).encode('UTF-8') )
		time.sleep(0.15)

	def getResponse(self, startsWith=''):
		response = self.ser.readline().decode(encoding='UTF-8')
		if(startsWith != ''):
			while(response[0] != startsWith):
				response = self.ser.readline().decode(encoding='UTF-8')
				print('SKIP')
		return response