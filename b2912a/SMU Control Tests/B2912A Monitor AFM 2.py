import visa
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import json

saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
saveFileName = 'SMU2.csv'

saveFolder = 'data/'

if not os.path.exists(saveFolder):
	saveFolder = '/home/pi/Desktop/Testing'
	# os.makedirs(saveFolder)


rm = visa.ResourceManager()
print(rm.list_resources())
# inst1 = rm.open_resource(rm.list_resources()[0])
# inst2 = rm.open_resource(rm.list_resources()[1])
inst1 = rm.open_resource('USB0::0x0957::0x8E18::MY51141244::INSTR')
inst2 = rm.open_resource('USB0::0x0957::0x8E18::MY51141241::INSTR')

print(inst1.query('*IDN?'))
print(inst2.query('*IDN?'))

chip = 'C127E'
device = '7-8'

#Noyce-Dell
chip = 'C127D'
device = '6-7'

NPLC = 1
scanRate = 0.2
ScanRateInverse = 1/scanRate
NpointsPerSec = 60/4
SecondsPerLine = 2*ScanRateInverse
lines = 32
Npoints = int(lines*SecondsPerLine*NpointsPerSec)
complianceCurrent = 50e-6
complianceVoltage = 10

# inst1.write("*RST") # Reset
# inst2.write("*RST") # Reset

inst1.write(':system:lfrequency 60')
inst2.write(':system:lfrequency 60')
print(inst1.query(':system:lfrequency?'))
print(inst2.query(':system:lfrequency?'))

#1: inst1 is for source, drain, and gate (channel 1 is source/drain)

inst1.write(":source2:function:mode voltage")
inst2.write(":source2:function:mode current")
inst1.write(":source1:function:mode voltage")#1
# inst1.write(":source1:function:mode current")#2
inst2.write(":source1:function:mode current")

inst1.write(":source1:voltage -0.5")#1
# inst1.write(":source1:current 0.0")#2
inst1.write(":source2:voltage 0.0")

inst1.write(":sense1:function \"curr\"")#1
# inst1.write(":sense1:function \"volt\"")#2
inst2.write(":sense1:function \"volt\"")
inst1.write(":sense1:curr:nplc {} (@2)".format(NPLC))#1
inst1.write(":sense1:volt:nplc {} (@2)".format(NPLC))#2
inst2.write(":sense1:volt:nplc {} (@2)".format(NPLC))
inst1.write(":sense1:curr:prot {}".format(complianceCurrent))#1
# inst1.write(":sense1:volt:prot {}".format(complianceVoltage))#2
inst2.write(":sense1:volt:prot {}".format(complianceVoltage))

inst1.write(":sense2:function \"curr\"")
inst2.write(":sense2:function \"volt\"")
inst1.write(":sense2:curr:nplc {}".format(NPLC))
inst2.write(":sense2:volt:nplc {}".format(NPLC))
inst1.write(":sense2:curr:prot {}".format(complianceCurrent))
inst2.write(":sense2:volt:prot {}".format(complianceVoltage))

voltage1_1s = []
current1_1s = []
voltage1_2s = []
current1_2s = []
voltage2_1s = []
current2_1s = []
voltage2_2s = []
current2_2s = []
timestamps = []

for i in range(Npoints):
	measurement1 = inst1.query_ascii_values(':MEAS? (@1:2)')
	measurement2 = inst2.query_ascii_values(':MEAS? (@1:2)')
	
	voltage1_1 = measurement1[0]
	current1_1 = measurement1[1]
	voltage1_2 = measurement1[6]
	current1_2 = measurement1[7]
	
	voltage2_1 = measurement2[0]
	current2_1 = measurement2[1]
	voltage2_2 = measurement2[6]
	current2_2 = measurement2[7]
	
	timestamp = time.time()
	
	with open(saveFolder + saveFileName, 'a') as file:
		line = "[{},{},{},{},{},{},{},{},{}]\n"
		line = line.format(timestamp, voltage1_1, current1_1, voltage1_2, current1_2, voltage2_1, current2_1, voltage2_2, current2_2)
		file.write(line)
	
	timestamps.append(timestamp)
	voltage1_1s.append(voltage1_1)
	current1_1s.append(current1_1)
	voltage1_2s.append(voltage1_2)
	current1_2s.append(current1_2)
	
	voltage2_1s.append(voltage2_1)
	current2_1s.append(current2_1)
	voltage2_2s.append(voltage2_2)
	current2_2s.append(current2_2)
	
	# plt.cla()
	# plt.clf()
	# plt.plot(timestamps, voltage1_1s, 'b-')
	# plt.plot(timestamps, voltage1_2s, 'b--')
	# plt.twinx()
	# plt.plot(timestamps, current1_1s, 'g-')
	# plt.plot(timestamps, current1_2s, 'g--')
	# plt.draw()
	# plt.pause(0.001)
	
	message = '{:.6f}%   -   {:.2f} minutes left'.format(i/Npoints*100, (Npoints-i)/NpointsPerSec/60)
	message = message + '	Ids = {:.2e} A	Igs = {:.2e} A'.format(current1_1, current1_2)
	message = message + '	Vds = {:.2f} V'.format(voltage1_1)
	print(message)

# print(globals())
# print(dir())

saveDictionary = {
	'voltage1_1s':voltage1_1s,
	'current1_1s':current1_1s,
	'voltage1_2s':voltage1_2s,
	'current1_2s':current1_2s,
	'voltage2_1s':voltage2_1s,
	'current2_1s':current2_1s,
	'voltage2_2s':voltage2_2s,
	'current2_2s':current2_2s,
	'timestamps':timestamps,
	'chip':chip,
	'device':device
}

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


