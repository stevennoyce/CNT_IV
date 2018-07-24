import visa
import numpy as np
from matplotlib import pyplot as plt
import time
import os
import json

saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
saveFileName = 'SMU2.csv'

if not os.path.exists(saveFolder):
	os.makedirs(saveFolder)


rm = visa.ResourceManager()
print(rm.list_resources())
inst  = rm.open_resource(rm.list_resources()[0])

print(inst.query('*IDN?'))

NPLC = 1
Npoints = (1.0/0.1)*60*32*2
Npoints = 100
voltageStart = 0.1
voltageStop = 0.1
complianceCurrent = 50e-6
complianceVoltage = 10
measurements = 2

inst.write("*RST") # Reset

inst.write(':system:lfrequency 60')
print(inst.query(':system:lfrequency?'))

inst.write(":source1:function:mode current")
inst.write(":source2:function:mode voltage")

inst.write(":source2:voltage 0.5")

# inst.write(":sense2:function \"curr\"")
inst.write(":sense2:curr:nplc {} (@2)".format(NPLC))
inst.write(":sense2:curr:prot {}".format(complianceCurrent))

# inst.write(":sense1:function \"volt\"")
inst.write(":sense1:volt:nplc {}".format(NPLC))
inst.write(":sense1:volt:prot {}".format(complianceVoltage))

voltage1s = []
current1s = []
voltage2s = []
current2s = []
timestamps = []

for i in range(Npoints):
	measurement = inst.query_ascii_values(':MEAS? (@1:2)')
	
	voltage1 = measurement[0]
	current1 = measurement[1]
	voltage2 = measurement[6]
	current2 = measurement[7]
	timestamp = time.time()
	
	with open(saveFolder + saveFileName, 'a') as file:
		line = "[{},{},{},{},{}]\n"
		line = line.format(timestamp, voltage1, current1, voltage2, current2)
		file.write(line)
	
	timestamps.append(timestamp)
	voltage1s.append(voltage1)
	current1s.append(current1)
	voltage2s.append(voltage2)
	current2s.append(current2)
	
	# plt.cla()
	# plt.clf()
	# plt.plot(timestamps, voltage1s, 'b-')
	# plt.plot(timestamps, voltage2s, 'b--')
	# plt.twinx()
	# plt.plot(timestamps, current1s, 'g-')
	# plt.plot(timestamps, current2s, 'g--')
	# plt.draw()
	# plt.pause(0.001)

# print(globals())
# print(dir())

saveDictionary = {
	'voltage1s':voltage1s,
	'current1s':current1s,
	'voltage2s':voltage2s,
	'current2s':current2s,
	'timestamps':timestamps
}

with open(saveFolder + saveFileName[:-4] + '.json', 'a') as file:
	json.dump(saveDictionary, file)
	file.write('\r\n')

print('done')
plt.show()

