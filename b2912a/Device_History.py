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
	gateSweepFileName = 'GateSweep_' + parameters['chipID'] + '.json'
	burnOutFileName = 'BurnOut_' + parameters['chipID'] + '.json'

	gateSweepHistory = dlu.loadFullDeviceHistory(parameters['saveFolder'], gateSweepFileName, parameters['deviceID'])
	burnOutHistory = dlu.loadFullDeviceHistory(parameters['saveFolder'], burnOutFileName, parameters['deviceID'])

	gateSweepHistory = gateSweepHistory[parameters['numberOfOldestPlotsToExclude']:max(0,(len(gateSweepHistory)-parameters['numberOfNewestPlotsToExclude']))]
	burnOutHistory = burnOutHistory[parameters['numberOfOldestPlotsToExclude']:max(0,(len(burnOutHistory)-parameters['numberOfNewestPlotsToExclude']))]

	if(parameters['showOnlySuccessfulBurns']):
		burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)

	dpu.plotFullGateSweepHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)
	dpu.plotFullBurnOutHistory(burnOutHistory, parameters['saveFiguresGenerated'], showFigures)
	dpu.plotOnCurrentHistory(gateSweepHistory, parameters['saveFiguresGenerated'], showFigures)

	if(showFigures):
		dpu.show()


if __name__ == '__main__':
    run(default_parameters)