# === Imports ===
from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu

import time


# === Optional External Interface ===
def makePlots(default_parameters, waferID, chipID, deviceID, startExperimentNumber=0, endExperimentNumber=float('inf'), specificPlot='', figureSize=None, saveFolder=None, fileName='', save=False, startRelativeIndex=0, endRelativeIndex=float('inf'), mode_parameters={}, showFigures=True):
	parameters = default_parameters
	
	parameters['runType'] = 'DeviceHistory'
	parameters['waferID'] = waferID
	parameters['chipID'] = chipID
	parameters['deviceID'] = deviceID
	parameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = startExperimentNumber
	parameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] = endExperimentNumber
	parameters['DeviceHistory']['specificPlotToCreate'] = specificPlot
	parameters['DeviceHistory']['figureSizeOverride'] = figureSize
	parameters['DeviceHistory']['saveFiguresGenerated'] = save
	parameters['DeviceHistory']['excludeDataBeforeJSONRelativeIndex'] = startRelativeIndex
	parameters['DeviceHistory']['excludeDataAfterJSONRelativeIndex'] = endRelativeIndex
	parameters['DeviceHistory']['postFiguresGenerated'] = False
	parameters['DeviceHistory']['plotInRealTime'] = True
	parameters['DeviceHistory']['gateSweepDirection'] = 'reverse'
	
	if(saveFolder is not None):
		parameters['plotsFolder'] = saveFolder + '/'
	
	mode_parameters['fileName'] = fileName
	
	return run(parameters, showFigures=showFigures, plot_mode_parameters=mode_parameters)



# === Main ===
def run(parameters, showFigures=True, plot_mode_parameters={}):
	plotList = []

	gateSweepFileName = 'GateSweep.json'
	burnOutFileName = 'BurnOut.json'
	staticBiasFileName = 'StaticBias.json'
	
	p = parameters['DeviceHistory']
	plot_mode_parameters['saveFigures'] = p['saveFiguresGenerated']
	plot_mode_parameters['showFigures'] = showFigures
	
	if(p['plotGateSweeps']):
		try:			
			gateSweepHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), gateSweepFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if p['specificPlotToCreate'] in ['FullSubthresholdCurveHistory','']:
				plot1 = dpu.plotFullSubthresholdCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=plot_mode_parameters)
				plotList.append(plot1)
			if p['specificPlotToCreate'] in ['FullTransferCurveHistory','']:
				plot2 = dpu.plotFullTransferCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=plot_mode_parameters)
				plotList.append(plot2)
			if p['specificPlotToCreate'] in ['FullGateCurrentHistory','']:
				plot3 = dpu.plotFullGateCurrentHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=plot_mode_parameters)
				plotList.append(plot3)
			if p['specificPlotToCreate'] in ['OnAndOffCurrentHistory','']:
				plot4 = dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], mode_params=plot_mode_parameters)
				plotList.append(plot4)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(p['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), burnOutFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if(p['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			
			if p['specificPlotToCreate'] in ['FullBurnOutHistory','']:
				plot = dpu.plotFullBurnOutHistory(burnOutHistory, parameters, mode_params=plot_mode_parameters)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Burnout history.")

	if(p['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), staticBiasFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])
			
			if p['specificPlotToCreate'] in ['FullStaticBiasHistory','']:
				plot = dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], mode_params=plot_mode_parameters)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias history.")

	if(showFigures):
		dpu.show()

	return plotList


if __name__ == '__main__':
    run(default_parameters)