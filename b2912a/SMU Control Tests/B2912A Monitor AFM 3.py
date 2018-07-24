import visa
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import json

saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
saveFileName = 'SMU3_Testing.csv'

saveFolder = 'data/'

def startTriggers(smu, points):
	# smu.write(":source1:voltage:mode sweep")
	# smu.write(":source2:voltage:mode sweep")
	
	# smu.write(":source1:voltage:start {}".format(src1start))
	# smu.write(":source1:voltage:stop {}".format(src1stop)) 
	# smu.write(":source1:voltage:points {}".format(points))
	# smu.write(":source2:voltage:start {}".format(src2start))
	# smu.write(":source2:voltage:stop {}".format(src2stop)) 
	# smu.write(":source2:voltage:points {}".format(points))
	
	smu.write(":trig1:source aint")
	smu.write(":trig1:count {}".format(points))
	smu.write(":trig2:source aint")
	smu.write(":trig2:count {}".format(points))
	smu.write(":init (@1:2)")
	
	sleepTime = 1.5 * points*NPLC/60
	
	return sleepTime

def endTriggers(smu):
	current1s = smu.query_ascii_values(":fetch:array:curr? (@1)")
	voltage1s = smu.query_ascii_values(":fetch:array:voltage? (@1)")
	current2s = smu.query_ascii_values(":fetch:array:curr? (@2)")
	voltage2s = smu.query_ascii_values(":fetch:array:voltage? (@2)")
	times = smu.query_ascii_values(":fetch:array:time? (@2)")
	
	return {
		'voltage1s': voltage1s,
		'current1s': current1s,
		'voltage2s': voltage2s,
		'current2s': current2s,
		'times': times
	}

rm = visa.ResourceManager()
print(rm.list_resources())
# inst1 = rm.open_resource(rm.list_resources()[0])
# inst2 = rm.open_resource(rm.list_resources()[1])
inst1 = rm.open_resource('USB0::0x0957::0x8E18::MY51141244::INSTR', timeout=1e5)
inst2 = rm.open_resource('USB0::0x0957::0x8E18::MY51141241::INSTR', timeout=1e5)

#Noyce-Dell
chip = 'C127D'
device = '6-7'

NPLC = 0.2
scanRate = 0.2
ScanRateInverse = 1/scanRate
NpointsPerSec = 60/4
SecondsPerLine = 2*ScanRateInverse
lines = 32
Npoints = int(lines*SecondsPerLine*NpointsPerSec)
complianceCurrent = 50e-6
complianceVoltage = 10
Vds = -0.5
Vgs = 0

Npoints = 60*10

# inst1.write("*RST") # Reset
# inst2.write("*RST") # Reset

inst1.write(':system:lfrequency 60')
inst2.write(':system:lfrequency 60')

#1: inst1 is for source, drain, and gate (channel 1 is source/drain)

inst1.write(":source2:function:mode voltage")
inst2.write(":source2:function:mode current")
inst1.write(":source1:function:mode voltage")#1
# inst1.write(":source1:function:mode current")#2
inst2.write(":source1:function:mode current")

inst1.write(":source1:voltage {}".format(Vds))#1
# inst1.write(":source1:current 0.0")#2
inst1.write(":source2:voltage {}".format(Vgs))

inst1.write(":sense1:function \"curr\"")#1
# inst1.write(":sense1:function \"volt\"")#2
inst2.write(":sense1:function \"volt\"")
# inst1.write(":sense:curr:nplc {} (@1:2)".format(NPLC))#1
# inst1.write(":sense:volt:nplc {} (@1:2)".format(NPLC))#2
# inst2.write(":sense:volt:nplc {} (@1:2)".format(NPLC))
# inst2.write(":sense:curr:nplc {} (@1:2)".format(NPLC))
inst1.write(":sense1:curr:prot {}".format(complianceCurrent))#1
# inst1.write(":sense1:volt:prot {}".format(complianceVoltage))#2
inst2.write(":sense1:volt:prot {}".format(complianceVoltage))

inst1.write(":sense2:function \"curr\"")
inst2.write(":sense2:function \"volt\"")
# inst1.write(":sense2:curr:nplc {}".format(NPLC))
# inst2.write(":sense2:curr:nplc {}".format(NPLC))
inst1.write(":sense2:curr:prot {}".format(complianceCurrent))
inst2.write(":sense2:volt:prot {}".format(complianceVoltage))


inst1.write(":sense1:curr:nplc {}".format(NPLC))
inst1.write(":sense2:curr:nplc {}".format(NPLC))
inst2.write(":sense1:volt:nplc {}".format(NPLC))
inst2.write(":sense2:volt:nplc {}".format(NPLC))


voltage1_1s = []
current1_1s = []
voltage1_2s = []
current1_2s = []
voltage2_1s = []
current2_1s = []
voltage2_2s = []
current2_2s = []
timestamps1 = []
timestamps2 = []

# Begin main portion -----------------------------------------------------

startTime = time.time()

sleepTime = startTriggers(inst1, Npoints)
sleepTime = startTriggers(inst2, Npoints)

print('Sleep time is {}'.format(sleepTime))

# time.sleep(sleepTime)

print('Sleep time elapsed')

data1 = endTriggers(inst1)
data2 = endTriggers(inst2)

print('Elapsed time is {}'.format(time.time() - startTime))

voltage1_1s = data1['voltage1s']
current1_1s = data1['current1s']
voltage1_2s = data1['voltage2s']
current1_2s = data1['current2s']
timestamps1 = data1['times']

voltage2_1s = data2['voltage1s']
current2_1s = data2['current1s']
voltage2_2s = data2['voltage2s']
current2_2s = data2['current2s']
timestamps2 = data2['times']


# plt.cla()
# plt.clf()
# plt.plot(timestamps, voltage1_1s, 'b-')
# plt.plot(timestamps, voltage1_2s, 'b--')
# plt.twinx()
# plt.plot(timestamps, current1_1s, 'g-')
# plt.plot(timestamps, current1_2s, 'g--')
# plt.draw()
# plt.pause(0.001)

saveDictionary = {
	'voltage1_1s':voltage1_1s,
	'current1_1s':current1_1s,
	'voltage1_2s':voltage1_2s,
	'current1_2s':current1_2s,
	'voltage2_1s':voltage2_1s,
	'current2_1s':current2_1s,
	'voltage2_2s':voltage2_2s,
	'current2_2s':current2_2s,
	'timestamps1':timestamps1,
	'timestamps2':timestamps2,
	'chip':chip,
	'device':device
}

print('Save dictionary is:')
print(saveDictionary)

with open(saveFolder + saveFileName[:-4] + '.json', 'a') as file:
	json.dump(saveDictionary, file)
	file.write('\r\n')

print('done')


plt.plot(timestamps, voltage2_1s, 'b--')
plt.plot(timestamps, voltage2_2s, 'b-')
plt.ylabel('Voltage [V] (Blue)')
plt.xlabel('Time [s]')
plt.twinx()
plt.plot(timestamps, current1_1s, 'g-')
# plt.plot(timestamps, current1_2s, 'g--')
plt.ylabel('Current [A] (Green)')
plt.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
plt.tight_layout()
plt.show()


plt.plot(voltage2_1s, current1_1s, 'o')
plt.xlabel('Horizontal Position [V]')
plt.ylabel('Drain Current [A]')
plt.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
plt.tight_layout()
plt.show()

plt.plot(voltage2_2s, current1_1s, 'o')
plt.xlabel('Horizontal Position [V]')
plt.ylabel('Drain Current [A]')
plt.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
plt.tight_layout()
plt.show()

# plt.scatter(voltage2_1s, voltage2_2s, c=current1_1s, cmap='viridis')
# plt.colorbar()
# plt.show()


c, a, b = zip(*sorted(zip(current1_1s, voltage2_1s, voltage2_2s), reverse=True))
plt.scatter(a, b, c=c, cmap='viridis')
plt.colorbar()
plt.show()

# c, a, b = zip(*sorted(zip(current1_1s, voltage2_1s, voltage2_2s), reverse=False))
# plt.scatter(a, b, c=c, cmap='viridis')
# plt.colorbar()
# plt.show()

# temp = zip(*sorted(zip(current1_1s, voltage2_1s, voltage2_2s), reverse=False))
# temp = [x for x in temp if x[0] < np.mean(current1_1s)]
# print(temp)
# c, a, b = temp
# plt.scatter(a, b, c=c, cmap='viridis')
# plt.colorbar()
# plt.show()

# c, a, b = zip(*sorted(zip(current1_2s, voltage2_1s, voltage2_2s), reverse=True))
# plt.scatter(a, b, c=c, cmap='viridis')
# plt.colorbar()
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(voltage2_1s, voltage2_2s, current1_1s)
# plt.show()


