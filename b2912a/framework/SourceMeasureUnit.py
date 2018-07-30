import ast
import serial as pySerial
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
	return B2912A(instance, defaultComplianceCurrent)

def getConnectionToPCB(port='', system_settings=None):
	if(port == ''):
		#port = 'COM7'
		port = '/dev/tty.HC-05-DevB'
	ser = pySerial.Serial(port, 115200, timeout=0.5)
	return PCB2v14(ser)



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

	def getVds(self):
		return self.takeMeasurement()['V_ds']

	def getVgs(self):
		return self.takeMeasurement()['V_gs']

	def rampGateVoltage(self, voltageStart, voltageSetPoint, steps=stepsPerRamp):
		gateVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for gateVoltage in gateVoltages:
			self.setVgs(gateVoltage)

	def rampGateVoltageTo(self, voltageSetPoint, steps=stepsPerRamp):
		voltageStart = self.getVgs()
		self.rampGateVoltage(voltageStart, voltageSetPoint, steps)

	def rampGateVoltageDown(self, steps=stepsPerRamp):
		voltageStart = self.getVgs()
		self.rampGateVoltage(voltageStart, 0, steps)

	def rampDrainVoltage(self, voltageStart, voltageSetPoint, steps=stepsPerRamp):
		drainVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for drainVoltage in drainVoltages:
			self.setVds(drainVoltage)

	def rampDrainVoltageTo(self, voltageSetPoint, steps=stepsPerRamp):
		voltageStart = self.getVds()
		self.rampDrainVoltage(voltageStart, voltageSetPoint, steps)

	def rampDrainVoltageDown(self, steps=stepsPerRamp):
		voltageStart = self.getVds()
		self.rampDrainVoltage(voltageStart, 0, steps)

	def rampDownVoltages(self, steps=stepsPerRamp):
		print('Ramping down SMU channels.')
		source1_voltage = self.getVds()
		source2_voltage = self.getVgs()
		self.rampDrainVoltage(source1_voltage, 0, steps)
		self.rampGateVoltage(source2_voltage, 0, steps)

class B2912A(SourceMeasureUnit):
	smu = None
	measurementsPerSecond = 60
	nplc = 1
	
	def __init__(self, visa_instance, defaultComplianceCurrent):
		self.smu = visa_instance
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
			timeToTakeMeasurements = 1.5*(self.nplc)*(points/self.measurementsPerSecond)
		else:
			self.smu.write(":trig1:source timer")
			self.smu.write(":trig1:timer {}".format(triggerInterval))
			self.smu.write(":trig1:count {}".format(points))
			self.smu.write(":trig2:source timer")
			self.smu.write(":trig2:timer {}".format(triggerInterval))
			self.smu.write(":trig2:count {}".format(points))
			timeToTakeMeasurements = (triggerInterval*points)
		
		self.smu.write(":init (@1:2)")
		
		return timeToTakeMeasurements
	
	def endSweep(endMode=None):
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
		timeToTakeMeasurements = startSweep(self, src1start, src1stop, src2start, src2stop, points, triggerInterval)
		
		time.sleep(timeToTakeMeasurements)
		
		endSweep(endMode='fixed')


class PCB2v14(SourceMeasureUnit):
	ser = None
	measurementsPerSecond = 10
	nplc = 1

	def __init__(self, pySerial):
		self.ser = pySerial
		self.setParameter('connect-intermediates !')
		time.sleep(0.5)

	def setComplianceCurrent(self, complianceCurrent):
		pass

	def setParameter(self, parameter):
		self.ser.write( str(parameter).encode('UTF-8') )
		time.sleep(0.2)

	def getResponse(self, startsWith=''):
		response = self.ser.readline().decode(encoding='UTF-8')
		if(startsWith != ''):
			while(response[0] != startsWith):
				print('SKIP')
				if(not self.ser.in_waiting):
					time.sleep(0.5)
				response = self.ser.readline().decode(encoding='UTF-8')

		return response

	def formatMeasurement(self, measurement):
		data = json.loads(str(measurement))
		return {
			'V_ds':data[2],
			'I_d': data[0],
			'V_gs':data[1],
			'I_g': 0
		}

	def setDevice(self, deviceID):
		self.setParameter('disconnect-all-from-all !')
		time.sleep(0.5)
		contactPad1 = int(deviceID.split('-')[0])
		contactPad2 = int(deviceID.split('-')[1])
		intermediate1 = (1) if(contactPad1 <= 32) else (3)
		intermediate2 = (2) if(contactPad2 <= 32) else (4)
		self.setParameter("connect {} {}!".format(contactPad1, intermediate1))
		time.sleep(0.5)
		self.setParameter("connect {} {}!".format(contactPad2, intermediate2))
		time.sleep(0.5)
		while (self.ser.in_waiting):
			print(self.getResponse(), end='')
			time.sleep(0.1)

	def setVds(self, voltage):
		self.setParameter("set-vds-mv {:.0f}!".format(voltage*1000))
		response = self.getResponse(startsWith='#')
		print('VDS: ' + str(response), end='')

	def setVgs(self, voltage):
		self.setParameter("set-vgs-mv {:.0f}!".format(voltage*1000))
		response = self.getResponse(startsWith='#')
		print('VGS: ' + str(response), end='')

	def takeMeasurement(self):
		self.setParameter('measure !')
		response = self.getResponse(startsWith='[')
		print('MEAS: ' + str(response), end='')
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









