from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu


# ## ********** Parameters **********

# chipID = 'C127M'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/b2912a/data/'

# default_parameters = {
# 	'chipID':chipID,
# 	'saveFolder':saveFolder,
# }

## ********** Main **********

def run(parameters):
	burnOutFileName = 'BurnOut.json'
	gateSweepFileName = 'GateSweep.json'
	chipDirectory = parameters['saveFolder'] + parameters['chipID'] + '/'

	firstRunChipHistory = dlu.loadFirstRunChipHistory(chipDirectory, gateSweepFileName, parameters['chipID'])
	recentRunChipHistory = dlu.loadMostRecentRunChipHistory(chipDirectory, gateSweepFileName, parameters['chipID'])

	dpu.plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory)
	dpu.show()


if __name__ == '__main__':
    run(default_parameters)