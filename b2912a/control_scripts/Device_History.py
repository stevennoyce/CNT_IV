# === Make this script runnable ===
if(__name__ == '__main__'):
	import sys
	sys.path.append(sys.path[0] + '/..')

# === Imports ===
from utilities import DataPlotterUtility as dpu
from utilities import DataLoggerUtility as dlu
from utilities import PlotPostingUtility as plotPoster



# === Defaults ===
default_dh_parameters = {
	'dataFolder': 'data/',
	'postFolder': 'CurrentPlots/',
	'showFiguresGenerated': True,
	'saveFiguresGenerated': True,
	'postFiguresGenerated': False,
	'plotGateSweeps': True,
	'plotBurnOuts':   True,
	'plotStaticBias': True,
	'specificPlotToCreate': '',
	'excludeDataBeforeJSONIndex': 0,
	'excludeDataAfterJSONIndex':  float('inf'),
	'excludeDataBeforeJSONExperimentNumber': 0,
	'excludeDataAfterJSONExperimentNumber':  float('inf'),
	'excludeDataBeforeJSONRelativeIndex': 0,
	'excludeDataAfterJSONRelativeIndex':  float('inf'),
	'gateSweepDirection': ['both','forward','reverse'][0],
	'showOnlySuccessfulBurns': False,
	'timescale': ['','seconds','minutes','hours','days','weeks'][0],
	'plotInRealTime': True,
	'includeBiasVoltageSubplot': True
}

plots_for_experiment = {
	'GateSweep' : {
		'primary':[	
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory'
		]
	},
	'BurnOut' : {	
		'primary':[	
			'FullBurnOutHistory'
		]
	},
	'AutoBurnOut' : {
		'primary':[
			'FullBurnOutHistory',
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory',
			'OnAndOffCurrentHistory'
		]
	},
	'StaticBias' : {
		'primary':[
			'FullStaticBiasHistory'
		]
	},
	'AutoGateSweep' : {
		'primary':[
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory',
			'OnAndOffCurrentHistory'
		],
		'secondary':[
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory',
			'OnAndOffCurrentHistory',
			'FullStaticBiasHistory'
		]
	},
	'AutoStaticBias' : {
		'primary':[
			'FullStaticBiasHistory',
			
		],
		'secondary':[
			'FullStaticBiasHistory',
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory',
			'OnAndOffCurrentHistory'
		]
	}
}

def getPossiblePlotNames(parameters):
	try:
		p = parameters
		
		plotsType = 'primary'
		if(p['runType'] == 'AutoStaticBias'):
			plotsType = 'secondary' if((('doInitialGateSweep' in p['AutoStaticBias']) and p['AutoStaticBias']['doInitialGateSweep']) or p['AutoStaticBias']['applyGateSweepBetweenBiases']) else 'primary' 
		if(p['runType'] == 'AutoGateSweep'):
			plotsType = 'secondary' if(p['AutoGateSweep']['applyStaticBiasBetweenSweeps']) else 'primary' 
		
		return plots_for_experiment[p['runType']][plotsType]
	except Exception as e:
		print('Exception raised in getPossiblePlotNames')
		print(e)
		return [
			'FullStaticBiasHistory',
			'FullSubthresholdCurveHistory',
			'FullTransferCurveHistory',
			'FullGateCurrentHistory',
			'OnAndOffCurrentHistory',
			'FullBurnOutHistory'
		]



# === Optional External Interface ===
def makePlots(waferID, chipID, deviceID, startExperimentNumber=0, endExperimentNumber=float('inf'), specificPlot='', figureSize=None, dataFolder=None, saveFolder=None, plotSaveName='', saveFigures=False, showFigures=True, startRelativeIndex=0, endRelativeIndex=float('inf'), mode_parameters=None):
	parameters = {}	
	mode_parameters = {}
	
	parameters['waferID'] = waferID
	parameters['chipID'] = chipID
	parameters['deviceID'] = deviceID

	parameters['showFiguresGenerated'] = showFigures
	parameters['saveFiguresGenerated'] = saveFigures
	parameters['postFiguresGenerated'] = False
	parameters['specificPlotToCreate'] = specificPlot
	parameters['excludeDataBeforeJSONExperimentNumber'] = startExperimentNumber
	parameters['excludeDataAfterJSONExperimentNumber'] = endExperimentNumber
	parameters['excludeDataBeforeJSONRelativeIndex'] = startRelativeIndex
	parameters['excludeDataAfterJSONRelativeIndex'] = endRelativeIndex
	parameters['gateSweepDirection'] = 'reverse'
	parameters['plotInRealTime'] = True
	
	if(dataFolder is not None):
		parameters['dataFolder'] = dataFolder
	if(saveFolder is not None):
		mode_parameters['plotSaveFolder'] = saveFolder
	
	mode_parameters['plotSaveName'] = plotSaveName
	mode_parameters['figureSizeOverride'] = figureSize
	
	return run(parameters, plot_mode_parameters=mode_parameters)



# === Main ===
def run(additional_parameters, plot_mode_parameters=None):
	parameters = default_dh_parameters.copy()
	parameters.update(additional_parameters)

	mode_parameters = {}
	if(plot_mode_parameters != None):
		mode_parameters.update(plot_mode_parameters)

	p = parameters

	mode_parameters['showFigures'] = p['showFiguresGenerated']
	mode_parameters['saveFigures'] = p['saveFiguresGenerated']

	plotList = []
	
	# Print information about the device and experiment being plotted
	print('  ' + parameters['waferID'] + parameters['chipID'] + ':' + parameters['deviceID'])
	'' if((p['excludeDataBeforeJSONExperimentNumber'] == 0) and (p['excludeDataAfterJSONExperimentNumber'] == float('inf'))) else (print('  Experiment #{:}'.format(p['excludeDataAfterJSONExperimentNumber'])) if(p['excludeDataBeforeJSONExperimentNumber'] == p['excludeDataAfterJSONExperimentNumber']) else (print('  Experiments #{:} to #{:}'.format(p['excludeDataBeforeJSONExperimentNumber'],p['excludeDataAfterJSONExperimentNumber'])))) 
	'' if((p['excludeDataBeforeJSONRelativeIndex'] == 0) and (p['excludeDataAfterJSONRelativeIndex'] == float('inf'))) else (print('  Rel. Index #{:}'.format(p['excludeDataAfterJSONRelativeIndex'])) if(p['excludeDataBeforeJSONRelativeIndex'] == p['excludeDataAfterJSONRelativeIndex']) else (print('  Rel. Indices #{:} to #{:}'.format(p['excludeDataBeforeJSONRelativeIndex'],p['excludeDataAfterJSONRelativeIndex']))))
	'' if((p['excludeDataBeforeJSONIndex'] == 0) and (p['excludeDataAfterJSONIndex'] == float('inf'))) else (print('  Abs. Index #{:}'.format(p['excludeDataAfterJSONIndex'])) if(p['excludeDataBeforeJSONIndex'] == p['excludeDataAfterJSONIndex']) else (print('  Abs. Indices #{:} to #{:}'.format(p['excludeDataBeforeJSONIndex'],p['excludeDataAfterJSONIndex']))))

	if(p['plotGateSweeps'] and (p['specificPlotToCreate'] in ['FullSubthresholdCurveHistory','FullTransferCurveHistory','FullGateCurrentHistory','OnAndOffCurrentHistory',''])):
		try:			
			gateSweepHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), 'GateSweep.json', minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if p['specificPlotToCreate'] in ['FullSubthresholdCurveHistory','']:
				plot1 = dpu.plotFullSubthresholdCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=mode_parameters)
				plotList.append(plot1)
			if p['specificPlotToCreate'] in ['FullTransferCurveHistory','']:
				plot2 = dpu.plotFullTransferCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=mode_parameters)
				plotList.append(plot2)
			if p['specificPlotToCreate'] in ['FullGateCurrentHistory','']:
				plot3 = dpu.plotFullGateCurrentHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], mode_params=mode_parameters)
				plotList.append(plot3)
			if p['specificPlotToCreate'] in ['OnAndOffCurrentHistory','']:
				plot4 = dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], mode_params=mode_parameters)
				plotList.append(plot4)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(p['plotBurnOuts'] and (p['specificPlotToCreate'] in ['FullBurnOutHistory',''])):
		try:
			burnOutHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), 'BurnOut.json', minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])

			if(p['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			
			if p['specificPlotToCreate'] in ['FullBurnOutHistory','']:
				plot = dpu.plotFullBurnOutHistory(burnOutHistory, parameters, mode_params=mode_parameters)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Burnout history.")

	if(p['plotStaticBias'] and (p['specificPlotToCreate'] in ['FullStaticBiasHistory',''])):
		try:
			staticBiasHistory = dlu.loadSpecificDeviceHistory(dlu.getDeviceDirectory(parameters), 'StaticBias.json', minIndex=p['excludeDataBeforeJSONIndex'], maxIndex=p['excludeDataAfterJSONIndex'], minExperiment=p['excludeDataBeforeJSONExperimentNumber'], maxExperiment=p['excludeDataAfterJSONExperimentNumber'], minRelativeIndex=p['excludeDataBeforeJSONRelativeIndex'], maxRelativeIndex=p['excludeDataAfterJSONRelativeIndex'])
			
			if p['specificPlotToCreate'] in ['FullStaticBiasHistory','']:
				plot = dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], mode_params=mode_parameters)
				plotList.append(plot)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias history.")

	if(p['showFiguresGenerated']):
		dpu.show()
	
	if(p['postFiguresGenerated']):
		parameters['startIndexes'] = {
			'index': max( parameters['excludeDataBeforeJSONIndex'], min(loadIndexesOfExperiementRange(directory, parameters['excludeDataBeforeJSONExperimentNumber'], parameters['excludeDataAfterJSONExperimentNumber'])) ),
			'experimentNumber': parameters['excludeDataBeforeJSONExperimentNumber']
		}
		parameters['endIndexes'] = {
			'index': min( parameters['excludeDataAfterJSONIndex'], max(loadIndexesOfExperiementRange(directory, parameters['excludeDataBeforeJSONExperimentNumber'], parameters['excludeDataAfterJSONExperimentNumber'])) ),
			'experimentNumber': min(parameters['excludeDataAfterJSONExperimentNumber'], dlu.loadJSONIndex(dlu.getDeviceDirectory(parameters))['experimentNumber'])
		} 

		dlu.makeFolder(parameters['postFolder'])
		dlu.emptyFolder(parameters['postFolder'])

		print('Posting plots online...')
		plotPoster.postPlots(parameters)

	return plotList





if __name__ == '__main__':
    makePlots('C127', 'X', '15-16', startExperimentNumber=24, endExperimentNumber=24, dataFolder='../data', saveFolder='../CurrentPlots', saveFigures=True)


