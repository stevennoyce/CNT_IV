# === Make this script runnable ===
if(__name__ == '__main__'):
	import sys
	sys.path.append(sys.path[0] + '/..')

# === Imports ===
from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu



# === Defaults ===
default_ch_parameters = {
	'dataFolder': 'data/',
	'showFiguresGenerated': True,
	'saveFiguresGenerated': True,
	'specificPlotToCreate': ''
}



# === Optional External Interface ===
def makePlots(waferID, chipID, specificPlot='', dataFolder=None, saveFolder=None, plotSaveName='', showFigures=True, saveFigures=True, mode_parameters={}):
	parameters = {}	
	parameters['waferID'] = waferID
	parameters['chipID'] = chipID

	if(dataFolder is not None):
		parameters['dataFolder'] = dataFolder
	parameters['showFiguresGenerated'] = showFigures
	parameters['saveFiguresGenerated'] = saveFigures
	parameters['specificPlotToCreate'] = specificPlot
	
	if(saveFolder is not None):
		mode_parameters['plotSaveFolder'] = saveFolder

	return run(parameters, mode_parameters)



# === Main ===
def run(additional_parameters, plot_mode_parameters={}):
	parameters = default_ch_parameters.copy()
	parameters.update(additional_parameters)

	plot_mode_parameters['showFigures'] = parameters['showFiguresGenerated']
	plot_mode_parameters['saveFigures'] = parameters['saveFiguresGenerated']

	plotList = []

	if(parameters['specificPlotToCreate'] in ['', 'ChipHistogram']):
		chipIndexes = dlu.loadChipIndexes(dlu.getChipDirectory(parameters))
		plot = dpu.plotChipHistogram(chipIndexes, mode_params=plot_mode_parameters)
		plotList.append(plot)

	if(parameters['specificPlotToCreate'] in ['', 'ChipOnOffRatios']):
		firstRunChipHistory = dlu.loadFirstRunChipHistory(dlu.getChipDirectory(parameters), 'GateSweep.json', parameters['chipID'])
		recentRunChipHistory = dlu.loadMostRecentRunChipHistory(dlu.getChipDirectory(parameters), 'GateSweep.json', parameters['chipID'])
		plot = dpu.plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory, mode_params=plot_mode_parameters)
		plotList.append(plot)

	if(parameters['showFiguresGenerated']):
		dpu.show()

	return plotList





if(__name__ == '__main__'):
	makePlots('C127', 'X', dataFolder='../data', saveFolder='../CurrentPlots')


