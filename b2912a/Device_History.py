from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu


# ## ********** Parameters **********

# chipID = 'C127M'
# deviceID = '1-2'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/b2912a/data/'

# default_parameters = {
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# }

## ********** Main **********

def run(parameters, showFigures=True):
	gateSweepFileName = 'GateSweep.json'
	burnOutFileName = 'BurnOut.json'
	staticBiasFileName = 'StaticBias.json'
	workingDirectory = parameters['saveFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'

	if(parameters['plotGateSweeps']):
		try:
			gateSweepHistory = dlu.loadFullDeviceHistory(workingDirectory, gateSweepFileName, parameters['deviceID'])
			
			if(parameters['excludeDataBeforeJSONIndex'] > 0):
				gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			if(parameters['excludeDataAfterJSONIndex'] < float('inf')):
				gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			
			if(parameters['excludeDataBeforeJSONExperimentNumber'] > 0):
				gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
			if(parameters['excludeDataAfterJSONExperimentNumber'] < float('inf')):		
				gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])

			dpu.plotFullGateSweepHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
			dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(parameters['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadFullDeviceHistory(workingDirectory, burnOutFileName, parameters['deviceID'])
			
			if(parameters['excludeDataBeforeJSONIndex'] > 0):
				burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			if(parameters['excludeDataAfterJSONIndex'] < float('inf')):			
				burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			
			if(parameters['excludeDataBeforeJSONExperimentNumber'] > 0):
				burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
			if(parameters['excludeDataAfterJSONExperimentNumber'] < float('inf')):		
				burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])

			if(parameters['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			dpu.plotFullBurnOutHistory(burnOutHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Burnout History")

	if(parameters['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadFullDeviceHistory(workingDirectory, staticBiasFileName, parameters['deviceID'])
			
			if(parameters['excludeDataBeforeJSONIndex'] > 0):
				staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			if(parameters['excludeDataAfterJSONIndex'] < float('inf')):
				staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			
			if(parameters['excludeDataBeforeJSONExperimentNumber'] > 0):
				staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
			if(parameters['excludeDataAfterJSONExperimentNumber'] < float('inf')):	
				staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])
			
			dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias History")

	if(showFigures):
		dpu.show()


if __name__ == '__main__':
    run(default_parameters)