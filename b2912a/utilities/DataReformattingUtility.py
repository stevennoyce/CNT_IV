import glob
import os
import numpy as np

import DataLoggerUtility as dlu

directory = '../data/C131D/'

gateSweepFileName = 'GateSweep.json'
burnOutFileName = 'BurnOut.json'
staticBiasFileName = 'StaticBias.json'

def main():
	for deviceSubdirectory in [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]:
		deviceDirectory = directory + deviceSubdirectory + '/'

		# Load device history for GateSweep, BurnOut, and StaticBias
		gateSweepHistory = dlu.loadJSON(deviceDirectory, gateSweepFileName)
		try:
			burnOutHistory = dlu.loadJSON(deviceDirectory, burnOutFileName)
			burnedout = True
		except:
			print('Device: ' + deviceSubdirectory + ' no burn-out')
			burnedout = False
		try:
			staticBiasHistory = dlu.loadJSON(deviceDirectory, staticBiasFileName)
			staticed = True
		except:
			print('Device: ' + deviceSubdirectory + ' no static bias')
			staticed = False
		# *************************************************************


		# Delete GateSweep.json, BurnOut.json, and StaticBias.json from device directory
		if os.path.exists(deviceDirectory):
			fileNames = glob.glob(deviceDirectory + '*')
			for fileName in fileNames:
				if((gateSweepFileName in fileName) or (burnOutFileName in fileName) or (staticBiasFileName in fileName)):
					os.remove(fileName)
		# *************************************************************


		# *************************************************************
		# ****************** BEGIN DATA MODIFICATION ******************
		# *************************************************************

		# GATE SWEEP
		for deviceRun in gateSweepHistory:
			if(deviceRun['ParametersFormatVersion'] >= 3):
				continue
			else:
				deviceRun['ParametersFormatVersion'] = 3

			if('current1s' in deviceRun):
				deviceRun['Results'] = {}
				deviceRun['Results']['id_data'] = deviceRun['current1s']
				deviceRun['Results']['ig_data'] = deviceRun['current2s']
				deviceRun['Results']['vds_data'] = deviceRun['voltage1s']
				deviceRun['Results']['vgs_data'] = deviceRun['voltage2s']
				deviceRun['Results']['timestamps'] = deviceRun['timestamps']
				deviceRun['Results']['gateVoltages'] = deviceRun['gateVoltages']
				deviceRun['Results']['onOffRatio'] = onOffRatio(deviceRun['Results']['id_data'])
				deviceRun['Results']['onCurrent'] = onCurrent(deviceRun['Results']['id_data'])
				deviceRun['Results']['offCurrent'] = offCurrent(deviceRun['Results']['id_data'])
				del deviceRun['current1s']
				del deviceRun['current2s']
				del deviceRun['voltage1s']
				del deviceRun['voltage2s']
				del deviceRun['timestamps']
				del deviceRun['gateVoltages']
				if('onOffRatio' in deviceRun):
					del deviceRun['onOffRatio']
				if('onCurrent' in deviceRun):
					del deviceRun['onCurrent']
				if('offCurrent' in deviceRun):
					del deviceRun['offCurrent']

		# BURN OUT
		if(burnedout):
			for deviceRun in burnOutHistory:
				if(deviceRun['ParametersFormatVersion'] >= 3):
					continue
				else:
					deviceRun['ParametersFormatVersion'] = 3

				if('current1s' in deviceRun):
					deviceRun['Results'] = {}
					deviceRun['Results']['id_data'] = deviceRun['current1s']
					deviceRun['Results']['ig_data'] = deviceRun['current2s']
					deviceRun['Results']['vds_data'] = deviceRun['voltage1s']
					deviceRun['Results']['vgs_data'] = deviceRun['voltage2s']
					deviceRun['Results']['timestamps'] = deviceRun['timestamps']
					deviceRun['Results']['drainVoltages'] = deviceRun['drainVoltages']
					del deviceRun['current1s']
					del deviceRun['current2s']
					del deviceRun['voltage1s']
					del deviceRun['voltage2s']
					del deviceRun['timestamps']
					del deviceRun['drainVoltages']
					if('didBurnOut' in deviceRun):
						deviceRun['Results']['didBurnOut'] = deviceRun['didBurnOut']
						del deviceRun['didBurnOut']
					else:
						deviceRun['Results']['didBurnOut'] = True
					if('thresholdCurrent' in deviceRun):
						deviceRun['Results']['thresholdCurrent'] = deviceRun['thresholdCurrent']
						del deviceRun['thresholdCurrent']
					else:
						deviceRun['Results']['thresholdCurrent'] = 0

		# STATIC BIAS
		if(staticed):			
			for deviceRun in staticBiasHistory:
				if(deviceRun['ParametersFormatVersion'] >= 3):
					continue
				else:
					deviceRun['ParametersFormatVersion'] = 3

				if('current1s' in deviceRun):
					deviceRun['Results'] = {}
					deviceRun['Results']['id_data'] = deviceRun['current1s']
					deviceRun['Results']['ig_data'] = deviceRun['current2s']
					deviceRun['Results']['vds_data'] = deviceRun['voltage1s']
					deviceRun['Results']['vgs_data'] = deviceRun['voltage2s']
					deviceRun['Results']['timestamps'] = deviceRun['timestamps']
					del deviceRun['current1s']
					del deviceRun['current2s']
					del deviceRun['voltage1s']
					del deviceRun['voltage2s']
					del deviceRun['timestamps']

		# *************************************************************
		# ******************  END DATA MODIFICATION  ******************
		# *************************************************************

				
		# Save device history for GateSweep, BurnOut, and StaticBias
		for deviceRun in gateSweepHistory:
			dlu.saveJSON(deviceDirectory, 'GateSweep', deviceRun, incrementIndex=False)
		if(burnedout):
			for deviceRun in burnOutHistory:
				dlu.saveJSON(deviceDirectory, 'BurnOut', deviceRun, incrementIndex=False)
		if(staticed):
			for deviceRun in staticBiasHistory:
				dlu.saveJSON(deviceDirectory, 'StaticBias', deviceRun, incrementIndex=False)
		# *************************************************************

def onOffRatio(drainCurrent):
	return onCurrent(drainCurrent)/offCurrent(drainCurrent)

def onCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return np.percentile(absDrainCurrent, 99)

def offCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return (np.percentile(absDrainCurrent, 5))

main()

