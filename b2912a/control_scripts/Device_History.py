from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu



## === Main ===

def run(parameters, showFigures=True):
	plotList = []

	gateSweepFileName = 'GateSweep.json'
	burnOutFileName = 'BurnOut.json'
	staticBiasFileName = 'StaticBias.json'
	
	p = parameters['DeviceHistory']
	
	if(p['plotGateSweeps']):
		try:			
			gateSweepHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), gateSweepFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if p['specificPlotToCreate'] in ['FullSubthresholdCurveHistory','']:
				plot1 = dpu.plotFullSubthresholdCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
				plotList.append(plot1)
			if p['specificPlotToCreate'] in ['FullTransferCurveHistory','']:
				plot2 = dpu.plotFullTransferCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
				plotList.append(plot2)
			if p['specificPlotToCreate'] in ['FullGateCurrentHistory','']:
				plot3 = dpu.plotFullGateCurrentHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
				plotList.append(plot3)
			if p['specificPlotToCreate'] in ['OnAndOffCurrentHistory','']:
				plot4 = dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures, includeDualAxis=p['includeBiasVoltageSubplot'])
				plotList.append(plot4)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(p['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), burnOutFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if(p['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			
			if p['specificPlotToCreate'] in ['FullBurnOutHistory','']:
				plot = dpu.plotFullBurnOutHistory(burnOutHistory, parameters, saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Burnout history.")

	if(p['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), staticBiasFileName, parameters['deviceID'], minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])
			
			if p['specificPlotToCreate'] in ['FullStaticBiasHistory','']:
				plot = dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias history.")

	if(showFigures):
		dpu.show()

	return plotList


if __name__ == '__main__':
    run(default_parameters)