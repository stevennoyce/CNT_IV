import visa
import time
import random as rand
import numpy as np

def getConnectionFromVisa(NPLC, defaultComplianceCurrent, smuTimeout=60000):
	rm = visa.ResourceManager()
	instance = rm.open_resource(rm.list_resources()[0])
	instance.timeout = smuTimeout
	print(instance.query('*IDN?'))
	return B2912A(instance, NPLC, defaultComplianceCurrent)


class PCB:
	def setParameter(self, parameter):
		raise NotImplementedError("Please implement PCB.setParameter()")

	def takeMeasurement(self):
		raise NotImplementedError("Please implement PCB.takeMeasurement()")

	def rampGateVoltage(self, voltageStart, voltageSetPoint, steps):
		gateVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for gateVoltage in gateVoltages:
			self.setParameter(":source2:voltage {}".format(gateVoltage))

	def rampGateVoltageTo(self, voltageSetPoint, steps):
		voltageStart = self.takeMeasurement()[6]
		self.rampGateVoltage(voltageStart, voltageSetPoint, steps)

	def rampGateVoltageDown(self, steps):
		voltageStart = self.takeMeasurement()[6]
		self.rampGateVoltage(voltageStart, 0, steps)

	def rampDrainVoltage(self, voltageStart, voltageSetPoint, steps):
		drainVoltages = np.linspace(voltageStart, voltageSetPoint, steps).tolist()
		for drainVoltage in drainVoltages:
			self.setParameter(":source1:voltage {}".format(drainVoltage))

	def rampDrainVoltageTo(self, voltageSetPoint, steps):
		voltageStart = self.takeMeasurement()[0]
		self.rampDrainVoltage(voltageStart, voltageSetPoint, steps)

	def rampDrainVoltageDown(self, steps):
		voltageStart = self.takeMeasurement()[0]
		self.rampDrainVoltage(voltageStart, 0, steps)

	def rampDownVoltages(self):
		source1_voltage = self.takeMeasurement()[0]
		source2_voltage = self.takeMeasurement()[6]
		self.rampDrainVoltage(source1_voltage, 0, 40)
		self.rampGateVoltage(source2_voltage, 0, 40)


class PCB2v14(PCB):
	smu = None

	def __init__(self, instance, NPLC, defaultComplianceCurrent):
		self.smu = instance
		self.initialize(NPLC)
		self.setComplianceCurrent(defaultComplianceCurrent)

	def initialize(self, NPLC):
		self.smu.write("*RST") # Reset
		self.smu.write(':system:lfrequency 60')
		
		self.smu.write(':SENS:CURR:RANGE:AUTO ON')
		self.smu.write(':SENS:CURR:RANGE:AUTO:LLIM 1e-8')
		
		self.smu.write(":source1:function:mode voltage")
		self.smu.write(":source2:function:mode voltage")
		
		self.smu.write(":source1:voltage 0.0")
		self.smu.write(":source2:voltage 0.0")
		
		self.smu.write(":sense1:curr:nplc {}".format(NPLC))
		self.smu.write(":sense2:curr:nplc {}".format(NPLC))
		
		self.smu.write(":outp1 ON")
		self.smu.write(":outp2 ON")
		
		self.smu.write("*WAI") # Explicitly wait for all of these commands to finish before handling new commands

	def setParameter(self, parameter):
		self.smu.write(parameter)

	def takeMeasurement(self):
		return self.smu.query_ascii_values(':MEAS? (@1:2)')

	def setComplianceCurrent(self, complianceCurrent):
		self.smu.write(":sense1:curr:prot {}".format(complianceCurrent))
		self.smu.write(":sense2:curr:prot {}".format(complianceCurrent))

	def takeSweep(self, src1start, src1stop, src2start, src2stop, points, NPLC):
		self.smu.write(":source1:voltage:mode sweep")
		self.smu.write(":source2:voltage:mode sweep")

		self.smu.write(":source1:voltage:start {}".format(src1start))
		self.smu.write(":source1:voltage:stop {}".format(src1stop)) 
		self.smu.write(":source1:voltage:points {}".format(points))
		self.smu.write(":source2:voltage:start {}".format(src2start))
		self.smu.write(":source2:voltage:stop {}".format(src2stop)) 
		self.smu.write(":source2:voltage:points {}".format(points))

		self.smu.write(":trig1:source aint")
		self.smu.write(":trig1:count {}".format(points))
		self.smu.write(":trig2:source aint")
		self.smu.write(":trig2:count {}".format(points))
		self.smu.write(":init (@1:2)")

		time.sleep(1.5 * points*NPLC/60)

		current1s = self.smu.query_ascii_values(":fetch:arr:curr? (@1)")
		voltage1s = self.smu.query_ascii_values(":fetch:arr:voltage? (@1)")
		current2s = self.smu.query_ascii_values(":fetch:arr:curr? (@2)")
		voltage2s = self.smu.query_ascii_values(":fetch:arr:voltage? (@2)")

		return {
			'voltage1s': voltage1s,
			'current1s': current1s,
			'voltage2s': voltage2s,
			'current2s': current2s
		}





