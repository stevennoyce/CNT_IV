# === Imports ===
from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters):
	gateSweepFileName = 'GateSweep.json'
	chipDirectory = parameters['dataFolder'] + parameters['waferID'] + '/' + parameters['chipID'] + '/'

	firstRunChipHistory = dlu.loadFirstRunChipHistory(chipDirectory, gateSweepFileName, parameters['chipID'])
	recentRunChipHistory = dlu.loadMostRecentRunChipHistory(chipDirectory, gateSweepFileName, parameters['chipID'])

	dpu.plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory)
	dpu.show()