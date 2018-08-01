if(__name__ == '__main__'):
	import sys
	sys.path.append(sys.path[0] + '/..')

# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu
from framework import SourceMeasureUnit as smu

import matplotlib as mpl
from matplotlib import pyplot as plt


# === Main ===
def run(isSavingResults=False, isPlottingResults=True):
	parameters = {
		'waferID': 'C127',
		'chipID': 'P',
		'deviceID': '31-32'
	}

	NPLC = 1
	compliance = 100e-6
	smu_instance = smu.getConnectionToVisaResource(defaultComplianceCurrent=100e-6, smuTimeout=60*1000)
	smu_instance.setComplianceCurrent(compliance)
	
	print('Beginning sandbox.')

	# === START ===
	smu_instance.rampDownVoltages()
	results = runSandBox(smu_instance)
	smu_instance.rampDownVoltages()

	# Copy parameters and add in the test results
	jsonData = parameters.copy()
	jsonData['Results'] = results
	
	# Save results as a JSON object
	if(isSavingResults):
		print('Saving JSON.')
		#dlu.saveJSON(dlu.getDeviceDirectory(parameters), parameters['StaticBias']['saveFileName'], jsonData)
	
	# Show plots to the user
	if(isPlottingResults):
		print('Plotting results.')
		#deviceHistoryScript.run(deviceHistoryParameters)
		#plt.plot(jsonData['Results']['timestamps'], jsonData['Results']['vds_data'])
		#plt.plot(jsonData['Results']['timestamps'], -np.array(jsonData['Results']['id_data']))
		#plt.plot(jsonData['Results']['timestamps'], jsonData['Results']['vgs_data'])
		#plt.show()
	
	return jsonData

# === Data Collection ===
def runSandBox(smu_instance):
	vds_data = []
	id_data = []
	vgs_data = []
	ig_data = []
	timestamps = []

	steps = 1
	vgs_setpoint = -15
	vds_setpoint = -0.5
	smu_instance.setVgs(vgs_setpoint)
	smu_instance.setVds(vds_setpoint)
		
	start = time.time()

	for i in range(steps):
		measurement = smu_instance.takeSweep(vds_setpoint, vds_setpoint, vgs_setpoint, vgs_setpoint, 300)
		
	end = time.time()

	print('TOTAL: ' + str(end - start))
	print('RATE: ' + str(300*steps/(end - start)))

	return {
		'vds_data':vds_data,
		'id_data':id_data,
		'vgs_data':vgs_data,
		'ig_data':ig_data,
		'timestamps':timestamps
	}


if(__name__ == '__main__'):
	run()

