import serial as pySerial
import time
import numpy as np

def getConnection(port, baud):
	ser = pySerial.Serial(port, baud, timeout=0.5)
	return ArduinoNanoBoard(ser)

class ArduinoNanoBoard:
	ser = None
	measurementsPerSecond = 1

	def __init__(self, pySerial):
		self.ser = pySerial
		time.sleep(0.5)

	def close(self):
		self.ser.close()