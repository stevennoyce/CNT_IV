import numpy as np
from matplotlib import pyplot as plt
import serial as pySerial
import time
import ast
import os


saveFolder = 'Testing/'
saveFileName = '102.csv'

if not os.path.exists(saveFolder):
	os.makedirs(saveFolder)

ser = pySerial.Serial('/dev/tty.usbmodem1411', 115200, timeout=0.1)
# ser = pySerial.Serial('/dev/tty.HC-05-DevB', 115200, timeout=0.1)
# ser = pySerial.Serial('COM7', 115200, timeout=0.1)

ser.write(b'connect-intermediates !')
time.sleep(0.1)
ser.write(b'set-vds-rel 20!')
time.sleep(0.1)
ser.write(b'set-vgs-rel 0!')
time.sleep(0.1)
ser.write(b'connect 1 1!')
time.sleep(0.1)
ser.write(b'connect 2 2!')
time.sleep(0.1)

time.sleep(0.1)

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)

data = None
devicei = 9

while ser.in_waiting:
	ser.write(b'measure !')
	
	line = ser.readline().decode(encoding='UTF-8')
	print(line)
	
	with open(saveFolder + saveFileName, 'a') as file:
		file.write(line)
		# json.dump(x, file)
	
	# if line[0] == '[':
	# 	dataline = np.array(ast.literal_eval(line))
	# 	# dataline = np.genfromtxt(line)
		
	# 	if data is None:
	# 		data = np.copy(dataline)
	# 	else:
	# 		data = np.column_stack([data, dataline])
	# 		plt.cla()
	# 		plt.plot(data[1], abs(data[0]))
		
		
	# 	# fig2 = plt.figure()
	# 	# fig2.add_subplot(1,1,1)
	# 	# fig2.axes[0].semilogy(sweep)
	# 	# fig2.show()
	# 	devicei = devicei + 1
	# 	plt.draw()
	# 	plt.pause(0.0001)
	
	time.sleep(0.1)


ser.close()

# ax.legend(loc='best')
plt.show()




