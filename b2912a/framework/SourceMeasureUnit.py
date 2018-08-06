import ast
import serial as pySerial
import serial.tools.list_ports as pySerialPorts
import glob
import visa

import time
import re
import random as rand
import numpy as np
import json

import copy

smu_system_configurations = {
	'single': {
		'SMU': {
			'uniqueID': '',
			'type': 'B2912A',
			'settings': {}
		}
	},
	'standalone': {
		'PCB': {
			'uniqueID': '',
			'type': 'PCB2v14',
			'settings': {}
		}
	},
	'double': {
		'deviceSMU':{
			'uniqueID': 'USB0::0x0957::0x8E18::MY51141244::INSTR',
			'type': 'B2912A',
			'settings': {}
		},
		'secondarySMU':{
			'uniqueID': 'USB0::0x0957::0x8E18::MY51141241::INSTR',
			'type': 'B2912A',
			'settings': {}
		}
	}
}

def getSystemConfiguration(systemType):
	return copy.deepcopy(smu_system_configurations[systemType])

def getConnectionToVisaResource(uniqueIdentifier='', system_settings=None, defaultComplianceCurrent=100e-6, smuTimeout=60000):
	rm = visa.ResourceManager()
	if(uniqueIdentifier == ''):
		uniqueIdentifier = rm.list_resources()[0]
	instance = rm.open_resource(uniqueIdentifier)
	instance.timeout = smuTimeout
	print(instance.query('*IDN?'))
	return B2912A(instance, uniqueIdentifier, defaultComplianceCurrent)

def getConnectionToPCB(pcb_port='', system_settings=None):
	if(pcb_port == ''):
		active_ports = [port for port in pySerialPorts.comports() if(port.description != 'n/a')]
		if(len(active_ports) == 0):
			raise Exception('Unable to find any active serial ports to connect to PCB.')
		else:
			pcb_port = active_ports[0].device
		#pcb_port = '/dev/tty.HC-05-DevB'
		#pcb_port = '/dev/tty.usbmodem1411'
	ser = pySerial.Serial(pcb_port, 115200)
	return PCB2v14(ser, pcb_port)



# class SimulationSMU(SourceMeasureUnit):
# 	source1_voltage = 0
# 	source2_voltage = 0
# 	source1_current = 0
# 	source2_current = 1e-10
# 	mu_Cox_WL = 50e-6
# 	thresholdVoltage = 1
# 	modelError = 0.15

# 	def setParameter(self, parameter):
# 		if(":source1:voltage" in str(parameter)):
# 			self.source1_voltage = float(parameter.split('voltage ')[1])
# 		if(":source2:voltage" in str(parameter)):
# 			self.source2_voltage = float(parameter.split('voltage ')[1])
# 		self.updateModelCurrent(self.source1_voltage, self.source2_voltage, self.mu_Cox_WL, self.thresholdVoltage)

# 	def takeMeasurement(self):
# 		return [self.source1_voltage,self.source1_current,'-','-','-','-',self.source2_voltage,self.source2_current,'-','-']

# 	def updateModelCurrent(self, v_ds, v_gs, kN, v_tn):
# 		if(v_gs > v_tn):
# 			if(v_ds < (v_gs - v_tn)):
# 				self.source1_current = self.withError(kN * ((v_gs - v_tn)*v_ds + (v_ds*v_ds/2)))
# 			else:
# 				self.source1_current = self.withError((kN/2) * ((v_gs - v_tn)*(v_gs - v_tn)))
# 		else:
# 			self.source1_current = self.withError(1e-10)

# 	def withError(self, measurement):
# 		return measurement * (1.0 + self.modelError*(2.0*rand.random() - 1.0))

class SourceMeasureUnit:
	system_id = ''
	measurementsPerSecond = None
	stepsPerRamp = 15
	
	def turnChannelsOn(self):
		raise NotImplementedError("Please implement SourceMeasureUnit.turnChannelsOn()")
	
	def turnChannelsOff(self):
		raise NotImplementedError("Please implement SourceMeasureUnit.turnChannelsOff()")
	
	def setComplianceCurrent(self, complianceCurrent):
		raise NotImplementedError("Please implement SourceMeasureUnit.setComplianceCurrent()")

	def setDevice(self, deviceID):
		raise NotImplementedError("Please implement SourceMeasureUnit.setDevice()")

	def setParameter(self, parameter):
		raise NotImplementedError("Please implement SourceMeasureUnit.setParameter()")

	def setVds(self, voltage):
		raise NotImplementedError("Please implement SourceMeasureUnit.setVds()")

	def setVgs(self, voltage):
		raise NotImplementedError("Please implement SourceMeasureUnit.setVgs()")

	def takeMeasurement(self):
		raise NotImplementedError("Please implement SourceMeasureUnit.takeMeasurement()")

	def takeSweep(self, src1start, src1stop, src2start, src2stop, points):
		raise NotImplementedError("Please implement SourceMeasureUnit.takeSweep()")
	
	def disconnect(self):
		raise NotImplementedError("Please implement SourceMeasureUnit.disconnect()")

	def getVds(self):
		return self.takeMeasurement()['V_ds']

	def getVgs(self):
		return self.takeMeasurement()['V_gs']

	def rampGateVoltage(self, voltageStart, voltageSetPoint, steps=None):
		if(steps == None):
			steps = self.stepsPerRamp
		gateVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for gateVoltage in gateVoltages:
			self.setVgs(gateVoltage)

	def rampGateVoltageTo(self, voltageSetPoint, steps=None):
		voltageStart = self.getVgs()
		self.rampGateVoltage(voltageStart, voltageSetPoint, steps)

	def rampGateVoltageDown(self, steps=None):
		self.rampGateVoltageTo(0, steps)

	def rampDrainVoltage(self, voltageStart, voltageSetPoint, steps=None):
		if(steps == None):
			steps = self.stepsPerRamp
		drainVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for drainVoltage in drainVoltages:
			self.setVds(drainVoltage)

	def rampDrainVoltageTo(self, voltageSetPoint, steps=None):
		voltageStart = self.getVds()
		self.rampDrainVoltage(voltageStart, voltageSetPoint, steps)

	def rampDrainVoltageDown(self, steps=None):
		self.rampDrainVoltageTo(0, steps)

	def rampDownVoltages(self, steps=None):
		print('Ramping down SMU channels.')
		self.rampDrainVoltageDown(steps)
		self.rampGateVoltageDown(steps)
	
class B2912A(SourceMeasureUnit):
	smu = None
	system_id = ''
	measurementsPerSecond = 40
	nplc = 1
	stepsPerRamp = 20
	
	def __init__(self, visa_instance, visa_id, defaultComplianceCurrent):
		self.smu = visa_instance
		self.system_id = visa_id
		self.initialize()
		self.setComplianceCurrent(defaultComplianceCurrent)
	
	def initialize(self):
		self.smu.write("*RST") # Reset
		self.smu.write(':system:lfrequency 60')
		
		self.smu.write(':sense1:curr:range:auto ON')
		self.smu.write(':sense1:curr:range:auto:llim 1e-8')

		self.smu.write(':sense2:curr:range:auto ON')
		self.smu.write(':sense2:curr:range:auto:llim 1e-8')
		
		self.smu.write(":source1:function:mode voltage")
		self.smu.write(":source2:function:mode voltage")
		
		self.smu.write(":source1:voltage 0.0")
		self.smu.write(":source2:voltage 0.0")
		
		self.smu.write(":sense1:curr:nplc 1")
		self.smu.write(":sense2:curr:nplc 1")
		
		self.smu.write(":outp1 ON")
		self.smu.write(":outp2 ON")
		
		self.smu.write("*WAI") # Explicitly wait for all of these commands to finish before handling new commands

	def setDevice(self, deviceID):
		pass

	def setParameter(self, parameter):
		self.smu.write(parameter)

	def turnChannelsOn(self):
		self.setParameter(":outp1 ON")
		self.setParameter(":outp2 ON")
	
	def turnChannelsOff(self):
		self.setParameter(":outp1 OFF")
		self.setParameter(":outp2 OFF")

	def turnAutoRangingOn(self):
		self.setParameter(':sense1:curr:range:auto ON')
		self.setParameter(':sense2:curr:range:auto ON')

	def turnAutoRangingOff(self):
		self.setParameter(':sense1:curr:range:auto OFF')
		self.setParameter(':sense2:curr:range:auto OFF')

	def setComplianceCurrent(self, complianceCurrent=100e-6):
		self.setParameter(":sense1:curr:prot {}".format(complianceCurrent))
		self.setParameter(":sense2:curr:prot {}".format(complianceCurrent))

	def setComplianceVoltage(self, complianceVoltage):
		self.setParameter(":sense1:volt:prot {}".format(complianceVoltage))
		self.setParameter(":sense2:volt:prot {}".format(complianceVoltage))

	def setChannel1SourceMode(self, mode="voltage"):
		self.setParameter(":source1:function:mode {}".format(mode))

	def setChannel2SourceMode(self, mode="voltage"):
		self.setParameter(":source2:function:mode {}".format(mode))

	def setVds(self, voltage):
		self.setParameter(":source1:voltage {}".format(voltage))

	def setVgs(self, voltage):
		self.setParameter(":source2:voltage {}".format(voltage))

	def takeMeasurement(self):
		data = self.smu.query_ascii_values(':MEAS? (@1:2)')
		return {
			'V_ds': data[0],
			'I_d':  data[1],
			'V_gs': data[6],
			'I_g':  data[7]
		}
	
	def startSweep(self, src1start, src1stop, src2start, src2stop, points, triggerInterval=None):
		points = int(points)
		
		self.smu.write(":source1:voltage:mode sweep")
		self.smu.write(":source2:voltage:mode sweep")
		
		self.smu.write(":source1:voltage:start {}".format(src1start))
		self.smu.write(":source1:voltage:stop {}".format(src1stop)) 
		self.smu.write(":source1:voltage:points {}".format(points))
		self.smu.write(":source2:voltage:start {}".format(src2start))
		self.smu.write(":source2:voltage:stop {}".format(src2stop)) 
		self.smu.write(":source2:voltage:points {}".format(points))
		
		if triggerInterval is None:
			self.smu.write(":trig1:source aint")
			self.smu.write(":trig1:count {}".format(points))
			self.smu.write(":trig2:source aint")
			self.smu.write(":trig2:count {}".format(points))
			timeToTakeMeasurements = (self.nplc)*(points/self.measurementsPerSecond)
		else:
			self.smu.write(":trig1:source timer")
			self.smu.write(":trig1:timer {}".format(triggerInterval))
			self.smu.write(":trig1:count {}".format(points))
			self.smu.write(":trig2:source timer")
			self.smu.write(":trig2:timer {}".format(triggerInterval))
			self.smu.write(":trig2:count {}".format(points))
			timeToTakeMeasurements = (triggerInterval*points)
		
		self.smu.write(":init (@1:2)")
		self.smu.write("*WAI")
		
		return timeToTakeMeasurements
	
	def endSweep(self, endMode=None):
		current1s = self.smu.query_ascii_values(":fetch:arr:curr? (@1)")
		voltage1s = self.smu.query_ascii_values(":fetch:arr:voltage? (@1)")
		current2s = self.smu.query_ascii_values(":fetch:arr:curr? (@2)")
		voltage2s = self.smu.query_ascii_values(":fetch:arr:voltage? (@2)")
		
		if endMode is not None:
			self.smu.write(":source1:voltage:mode {}".format(endMode))
			self.smu.write(":source2:voltage:mode {}".format(endMode))
		
		return {
			'Vds_data': voltage1s,
			'Id_data':  current1s,
			'Vgs_data': voltage2s,
			'Ig_data':  current2s
		}
	
	def takeSweep(self, src1start, src1stop, src2start, src2stop, points, triggerInterval=None):
		timeToTakeMeasurements = self.startSweep(src1start, src1stop, src2start, src2stop, points, triggerInterval=triggerInterval)
		
		time.sleep(timeToTakeMeasurements)
		
		return self.endSweep(endMode='fixed')
	
	def disconnect(self):
		pass
		


class PCB2v14(SourceMeasureUnit):
	ser = None
	system_id = ''
	measurementsPerSecond = 10
	nplc = 1
	stepsPerRamp = 5
	
	# Communication times seem to be quite fast, but just to be safe delay for 1 ms
	wait_sending = 0.001
	wait_recieving = 0.001
	
	# The DAC has much more to do than the ADC, so it gets more time to do its work
	wait_DAC = 0.35
	wait_ADC = 0.001
	
	# These delays are used for rare communication patterns that we don't mind giving a little extra time
	wait_long = 0.5
	wait_calibration = 2.0

	def __init__(self, pySerial, pcb_port):
		self.ser = pySerial
		self.system_id = pcb_port
		self.setParameter('connect-intermediates !')
		time.sleep(self.wait_long)

	def setComplianceCurrent(self, complianceCurrent):
		pass

	def setParameter(self, parameter):
		self.ser.write( str(parameter).encode('UTF-8') )
		time.sleep(self.wait_sending)

	def getResponse(self, startsWith=''):
		time.sleep(self.wait_recieving)
		response = self.ser.readline().decode(encoding='UTF-8')
		if(startsWith != ''):
			while(response[0] != startsWith):
				print('SKIPPED: ' + str(response))
				time.sleep(self.wait_long)
				response = self.ser.readline().decode(encoding='UTF-8')
		return response

	def formatMeasurement(self, measurement):
		data = json.loads(str(measurement))
		return {
			'V_ds':float(data[2]),
			'I_d': float(data[0]),
			'V_gs':float(data[1]),
			'I_g': 0.0
		}

	def setDevice(self, deviceID):
		self.setParameter('disconnect-all-from-all !')
		time.sleep(self.wait_long)
		contactPad1 = int(deviceID.split('-')[0])
		contactPad2 = int(deviceID.split('-')[1])
		intermediate1 = (1) if(contactPad1 <= 32) else (3)
		intermediate2 = (2) if(contactPad2 <= 32) else (4)
		self.setParameter("connect {} {}!".format(contactPad1, intermediate1))
		time.sleep(self.wait_long)
		self.setParameter("connect {} {}!".format(contactPad2, intermediate2))
		time.sleep(self.wait_long)
		while (self.ser.in_waiting):
			print(self.getResponse(), end='')
		self.setParameter("calibrate-offset !")
		time.sleep(self.wait_calibration)
		while (self.ser.in_waiting):
			print(self.getResponse(), end='')

	def setVds(self, voltage):
		self.setParameter("set-vds-mv {:.0f}!".format(voltage*1000))
		time.sleep(self.wait_DAC)
		response = self.getResponse(startsWith='#')
		print(str(response), end='')

	def setVgs(self, voltage):
		self.setParameter("set-vgs-mv {:.0f}!".format(voltage*1000))
		time.sleep(self.wait_DAC)
		response = self.getResponse(startsWith='#')
		print(str(response), end='')

	def takeMeasurement(self):
		self.setParameter('measure !')
		time.sleep(self.wait_ADC)
		response = self.getResponse(startsWith='[')
		print('MEASURE: ' + str(response), end='')
		return self.formatMeasurement(response)

	def takeSweep(self, src1start, src1stop, src2start, src2stop, points):
		vds_data = []
		id_data = []
		vgs_data = []
		ig_data = []
		points = int(points)

		if(src1start == src1stop and src2start == src2stop):
			self.setParameter('measure-multiple {:d}!'.format(points))

			timeToTakeMeasurements = (self.nplc)*(points/self.measurementsPerSecond)
			time.sleep(1.5 * timeToTakeMeasurements)

			while(self.ser.in_waiting):
				response = self.getResponse()
				data = self.formatMeasurement(response)
				vds_data.append(data['V_ds'])
				id_data.append(data['I_d'])
				vgs_data.append(data['V_gs'])
				ig_data.append(data['I_g'])

			return {
				'Vds_data': vds_data,
				'Id_data': id_data,
				'Vgs_data': vgs_data,
				'Ig_data': ig_data
			}


		raise NotImplementedError('PCB2v14 general sweep not implemented.')

		return {
			'Vds_data': vds_data,
			'Id_data': id_data,
			'Vgs_data': vgs_data,
			'Ig_data': ig_data
		}
	
	def disconnect(self):
		self.ser.close()









