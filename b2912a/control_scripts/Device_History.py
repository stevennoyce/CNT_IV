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
def makePlots(waferID, chipID, deviceID, startExperimentNumber=0, endExperimentNumber=float('inf'), specificPlot='', figureSize=None, dataFolder=None, saveFolder=None, plotSaveName='', saveFigures=False, showFigures=True, sweepDirection='reverse', plotInRealTime=True, startRelativeIndex=0, endRelativeIndex=float('inf'), plot_mode_parameters=None):
	parameters = {}	
	mode_parameters = {}
	if(plot_mode_parameters is not None):
		mode_parameters.update(plot_mode_parameters)
	
	parameters['waferID'] = waferID
	parameters['chipID'] = chipID
	parameters['deviceID'] = deviceID

	if(dataFolder is not None):
		parameters['dataFolder'] = dataFolder

	parameters['showFiguresGenerated'] = showFigures
	parameters['saveFiguresGenerated'] = saveFigures
	parameters['postFiguresGenerated'] = False
	parameters['specificPlotToCreate'] = specificPlot
	parameters['excludeDataBeforeJSONExperimentNumber'] = startExperimentNumber
	parameters['excludeDataAfterJSONExperimentNumber'] = endExperimentNumber
	parameters['excludeDataBeforeJSONRelativeIndex'] = startRelativeIndex
	parameters['excludeDataAfterJSONRelativeIndex'] = endRelativeIndex
	parameters['gateSweepDirection'] = sweepDirection
	parameters['plotInRealTime'] = plotInRealTime
	
	if(saveFolder is not None):
		mode_parameters['plotSaveFolder'] = saveFolder
	mode_parameters['plotSaveName'] = plotSaveName
	mode_parameters['figureSizeOverride'] = figureSize
	
	return run(parameters, plot_mode_parameters=mode_parameters)



# === Main ===
def run(additional_parameters, plot_mode_parameters=None):
	parameters = default_dh_parameters.copy()
	parameters.update(additional_parameters)

	p = parameters
	plotList = []

	mode_parameters = {}
	if(plot_mode_parameters != None):
		mode_parameters.update(plot_mode_parameters)
	mode_parameters['showFigures'] = p['showFiguresGenerated']
	mode_parameters['saveFigures'] = p['saveFiguresGenerated']

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
	#makePlots('C127', 'X', '15-16', 145, 145, 'FullStaticBiasHistory', (2.2 *3.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S6 floating - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'staticBiasSegmentDividers':True, 'plotGradient':True})
	#makePlots('C127', 'X', '15-16', 118, 118, 'FullStaticBiasHistory', (2.2 *3.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S5 Grounded Between - ', saveFigures=True, showFigures=False, startRelativeIndex=9, endRelativeIndex=16, plot_mode_parameters={'publication_mode':True,'staticBiasSegmentDividers':True, 'plotGradient':True})
	#makePlots('C127', 'E', '27-28', 3, 4, 'FullTransferCurveHistory', (1.48 *2.24/1.74,1.74 *2.24/1.74), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S1 Comparison - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'enableColorBar':False})
	#makePlots('C127', 'X', '15-16', 137, 137, 'FullStaticBiasHistory', (2.2 *3.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S8 Light - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'plotGradient':False})
	#makePlots('C127', 'X', '15-16', 127, 127, 'FullStaticBiasHistory', (2.2 *3.25/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S9a Light - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'plotGradient':True})
	#makePlots('C127', 'X', '15-16', 125, 125, 'FullStaticBiasHistory', (2.2 *3.25/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S9b Light - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'plotGradient':True})
	#makePlots('C127', 'X', '15-16', 127, 127, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S10a Light - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True})
	#makePlots('C127', 'X', '15-16', 125, 125, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S10b Light - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True})
	#makePlots('C127', 'X', '15-16', 104, 104, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S12a - ', saveFigures=True, showFigures=False, sweepDirection='both', plot_mode_parameters={'publication_mode':True, 'errorBarsOn':False}) 
	#makePlots('C127', 'X', '15-16', 91, 91, 'FullTransferCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S12b - ', saveFigures=True, showFigures=False, sweepDirection='both', startRelativeIndex=9, plot_mode_parameters={'publication_mode':True, 'errorBarsOn':False}) 
	#makePlots('C127', 'X', '15-16', 24, 24, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S11a - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True,'errorBarsOn':False})
	#makePlots('C127', 'X', '15-16', 24, 24, 'FullTransferCurveHistory', (1.48 *2.24/1.74,1.74 *2.24/1.74), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S11b - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True,'errorBarsOn':False})
	#makePlots('C127', 'X', '15-16', 0, float('inf'), 'FullStaticBiasHistory', (2.2 *5.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S10 full - ', saveFigures=True, showFigures=False, plotInRealTime=False, plot_mode_parameters={'publication_mode':True,'staticBiasChangeDividers':False,'plotGradient':True})
	#makePlots('C127', 'X', '15-16', 155, 155, 'FullStaticBiasHistory', (2.2 *3.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S7 no grounding or floating - ', saveFigures=True, showFigures=False, plotInRealTime=True, plot_mode_parameters={'publication_mode':True,'staticBiasChangeDividers':False,'plotGradient':True})
	#makePlots('C127', 'X', '15-16', 3, 6, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S4a - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True,'errorBarsOn':False,'legendLabels':['Initial','After 1 week']})
	#makePlots('C127', 'X', '15-16', 3, 6, 'FullTransferCurveHistory', (1.48 *2.24/1.74,1.74 *2.24/1.74), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S4b - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True,'errorBarsOn':False,'legendLabels':['Initial','After 1 week']})
	#makePlots('C127', 'E', '15-16', 1, 1, 'FullBurnOutHistory', (2.2 *4.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S3 burnout - ', saveFigures=True, showFigures=True, startRelativeIndex=5, plot_mode_parameters={'publication_mode':True})
	#makePlots('C127', 'E', '15-16', 1, 1, 'FullSubthresholdCurveHistory', (1.48 *2.24/1.74,1.74 *2.24/1.74), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S3 burnout gs - ', saveFigures=True, showFigures=True, plot_mode_parameters={'publication_mode':True, 'errorBarsOn':False, 'legendLabels':['Initial','After Burn-out']})
	#makePlots('C127', 'P', '1-2', 8, 8, 'FullStaticBiasHistory', (2.2 *4.5/2.2,1.408 *3.5/2.2), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure - ', saveFigures=False, showFigures=True, startRelativeIndex=20, endRelativeIndex=70, plot_mode_parameters={'publication_mode':True})
	#makePlots('C127', 'X', '15-16', 105, 125, 'FullSubthresholdCurveHistory', (1.45 *2.24/1.55,1.55 *2.24/1.55), dataFolder='../data', saveFolder='../CurrentPlots', plotSaveName='Figure S14 - ', saveFigures=True, showFigures=False, plot_mode_parameters={'publication_mode':True, 'errorBarsOn':False})
	pass





