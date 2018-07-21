import glob
import os
import numpy as np

import DataLoggerUtility as dlu

load_directory = '../data0/C127/X/'
save_directory = '../data_reformatted/C127/X/'

def main():
	for deviceSubdirectory in [name for name in os.listdir(load_directory) if os.path.isdir(os.path.join(load_directory, name))]:
		deviceLoadDirectory = os.path.join(load_directory, deviceSubdirectory)
		deviceSaveDirectory = os.path.join(save_directory, deviceSubdirectory)

		# Load device history for GateSweep, BurnOut, and StaticBias
		gateSweepHistory = dlu.loadJSON(deviceLoadDirectory, 'GateSweep.json')
		try:
			burnOutHistory = dlu.loadJSON(deviceLoadDirectory, 'BurnOut.json')
			burnedout = True
		except:
			print('Device: ' + deviceSubdirectory + ' no burn-out')
			burnedout = False
		try:
			staticBiasHistory = dlu.loadJSON(deviceLoadDirectory, 'StaticBias.json')
			staticed = True
		except:
			print('Device: ' + deviceSubdirectory + ' no static bias')
			staticed = False
		# *************************************************************


		

		# *************************************************************
		# ****************** BEGIN DATA MODIFICATION ******************
		# *************************************************************

		# GATE SWEEP
		for deviceRun in gateSweepHistory:
			if(deviceRun['ParametersFormatVersion'] > 4):
				continue
			else:
				deviceRun['ParametersFormatVersion'] = 4

			deviceRun['Identifiers'] = {}
			deviceRun['Identifiers']['user'] = 'stevenjay'
			deviceRun['Identifiers']['project'] = 'BiasStress1'
			deviceRun['Identifiers']['wafer'] = deviceRun['waferID']
			deviceRun['Identifiers']['chip'] = deviceRun['chipID']
			deviceRun['Identifiers']['device'] = deviceRun['deviceID']
			deviceRun['Identifiers']['step'] = None
			deviceRun['deviceDirectory'] = 'data/stevenjay/BiasStress1/' + deviceRun['Identifiers']['wafer'] + '/' + deviceRun['Identifiers']['chip'] + '/' + deviceRun['Identifiers']['device'] + '/'
			del deviceRun['waferID']
			del deviceRun['chipID']
			del deviceRun['deviceID']

			system = deviceRun['MeasurementSystem'] if('MeasurementSystem' in deviceRun) else 'B2912A'
			deviceRun['MeasurementSystem'] = {}
			deviceRun['MeasurementSystem']['system'] = system
			deviceRun['MeasurementSystem']['NPLC'] = deviceRun['NPLC'] if('NPLC' in deviceRun) else 1
			deviceRun['MeasurementSystem']['deviceRange'] = deviceRun['deviceRange'] if('deviceRange' in deviceRun) else []
			if('NPLC' in deviceRun):
				del deviceRun['NPLC']
			if('deviceRange' in deviceRun):
				del deviceRun['deviceRange']

		# BURN OUT
		if(burnedout):
			for deviceRun in burnOutHistory:
				if(deviceRun['ParametersFormatVersion'] > 4):
					continue
				else:
					deviceRun['ParametersFormatVersion'] = 4

				deviceRun['Identifiers'] = {}
				deviceRun['Identifiers']['user'] = 'stevenjay'
				deviceRun['Identifiers']['project'] = 'BiasStress1'
				deviceRun['Identifiers']['wafer'] = deviceRun['waferID']
				deviceRun['Identifiers']['chip'] = deviceRun['chipID']
				deviceRun['Identifiers']['device'] = deviceRun['deviceID']
				deviceRun['Identifiers']['step'] = None
				deviceRun['deviceDirectory'] = 'data/stevenjay/BiasStress1/' + deviceRun['Identifiers']['wafer'] + '/' + deviceRun['Identifiers']['chip'] + '/' + deviceRun['Identifiers']['device'] + '/'
				del deviceRun['waferID']
				del deviceRun['chipID']
				del deviceRun['deviceID']

				system = deviceRun['MeasurementSystem'] if('MeasurementSystem' in deviceRun) else 'B2912A'
				deviceRun['MeasurementSystem'] = {}
				deviceRun['MeasurementSystem']['system'] = system
				deviceRun['MeasurementSystem']['NPLC'] = deviceRun['NPLC'] if('NPLC' in deviceRun) else 1
				deviceRun['MeasurementSystem']['deviceRange'] = deviceRun['deviceRange'] if('deviceRange' in deviceRun) else []
				if('NPLC' in deviceRun):
					del deviceRun['NPLC']
				if('deviceRange' in deviceRun):
					del deviceRun['deviceRange']

		# STATIC BIAS
		if(staticed):			
			for deviceRun in staticBiasHistory:
				if(deviceRun['ParametersFormatVersion'] > 4):
					continue
				else:
					deviceRun['ParametersFormatVersion'] = 4

				deviceRun['Identifiers'] = {}
				deviceRun['Identifiers']['user'] = 'stevenjay'
				deviceRun['Identifiers']['project'] = 'BiasStress1'
				deviceRun['Identifiers']['wafer'] = deviceRun['waferID']
				deviceRun['Identifiers']['chip'] = deviceRun['chipID']
				deviceRun['Identifiers']['device'] = deviceRun['deviceID']
				deviceRun['Identifiers']['step'] = None
				deviceRun['deviceDirectory'] = 'data/stevenjay/BiasStress1/' + deviceRun['Identifiers']['wafer'] + '/' + deviceRun['Identifiers']['chip'] + '/' + deviceRun['Identifiers']['device'] + '/'
				del deviceRun['waferID']
				del deviceRun['chipID']
				del deviceRun['deviceID']

				system = deviceRun['MeasurementSystem'] if('MeasurementSystem' in deviceRun) else 'B2912A'
				deviceRun['MeasurementSystem'] = {}
				deviceRun['MeasurementSystem']['system'] = system
				deviceRun['MeasurementSystem']['NPLC'] = deviceRun['NPLC'] if('NPLC' in deviceRun) else 1
				deviceRun['MeasurementSystem']['deviceRange'] = deviceRun['deviceRange'] if('deviceRange' in deviceRun) else []
				if('NPLC' in deviceRun):
					del deviceRun['NPLC']
				if('deviceRange' in deviceRun):
					del deviceRun['deviceRange']


		# *************************************************************
		# ******************  END DATA MODIFICATION  ******************
		# *************************************************************



		# Save device history for GateSweep, BurnOut, and StaticBias
		for deviceRun in gateSweepHistory:
			dlu.saveJSON(deviceSaveDirectory, 'GateSweep', deviceRun, incrementIndex=False)
		if(burnedout):
			for deviceRun in burnOutHistory:
				dlu.saveJSON(deviceSaveDirectory, 'BurnOut', deviceRun, incrementIndex=False)
		if(staticed):
			for deviceRun in staticBiasHistory:
				dlu.saveJSON(deviceSaveDirectory, 'StaticBias', deviceRun, incrementIndex=False)
		# *************************************************************



if(__name__ == '__main__'):
	main()




