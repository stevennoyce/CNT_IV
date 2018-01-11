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
			gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			try:
				gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
				gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])
			except:
				print("Gate Sweep data doesn't contain Experiment Numbers")

			dpu.plotFullGateSweepHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
			dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(parameters['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadFullDeviceHistory(workingDirectory, burnOutFileName, parameters['deviceID'])
			burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			try:
				burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
				burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])
			except:
				print("Burn Out data doesn't contain Experiment Numbers")

			if(parameters['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			dpu.plotFullBurnOutHistory(burnOutHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Burnout History")

	if(parameters['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadFullDeviceHistory(workingDirectory, staticBiasFileName, parameters['deviceID'])
			staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'index', parameters['excludeDataBeforeJSONIndex'])
			staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'index', parameters['excludeDataAfterJSONIndex'])
			
			try:
				staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'experimentNumber', parameters['excludeDataBeforeJSONExperimentNumber'])
				staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'experimentNumber', parameters['excludeDataAfterJSONExperimentNumber'])
			except:
				print("Static bias data doesn't contain Experiment Numbers")
			
			dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias History")

	if(showFigures):
		dpu.show()


if __name__ == '__main__':
    run(default_parameters)