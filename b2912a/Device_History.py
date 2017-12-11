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
			gateSweepHistory = gateSweepHistory[parameters['numberOfOldestPlotsToExclude']:max(0,(len(gateSweepHistory)-parameters['numberOfNewestPlotsToExclude']))]
			dpu.plotFullGateSweepHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
			dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(parameters['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadFullDeviceHistory(workingDirectory, burnOutFileName, parameters['deviceID'])
			burnOutHistory = burnOutHistory[parameters['numberOfOldestPlotsToExclude']:max(0,(len(burnOutHistory)-parameters['numberOfNewestPlotsToExclude']))]
			if(parameters['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			dpu.plotFullBurnOutHistory(burnOutHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Burnout History")

	if(parameters['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadFullDeviceHistory(workingDirectory, staticBiasFileName, parameters['deviceID'])
			staticBiasHistory = staticBiasHistory[parameters['numberOfOldestPlotsToExclude']:max(0,(len(staticBiasHistory)-parameters['numberOfNewestPlotsToExclude']))]
			dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters['saveFiguresGenerated'], showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias History")

	if(showFigures):
		dpu.show()


if __name__ == '__main__':
    run(default_parameters)