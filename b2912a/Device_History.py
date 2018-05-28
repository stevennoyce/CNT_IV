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
	
	p = parameters['DeviceHistory']
	
	if(p['plotGateSweeps']):
		try:
			gateSweepHistory = dlu.loadFullDeviceHistory(parameters['deviceDirectory'], gateSweepFileName, parameters['deviceID'])
			
			if(p['excludeDataBeforeJSONIndex'] > 0):
				gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'index', p['excludeDataBeforeJSONIndex'])
			if(p['excludeDataAfterJSONIndex'] < float('inf')):
				gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'index', p['excludeDataAfterJSONIndex'])
			
			if(p['excludeDataBeforeJSONExperimentNumber'] > 0):
				gateSweepHistory = dlu.filterHistoryGreaterThan(gateSweepHistory, 'experimentNumber', p['excludeDataBeforeJSONExperimentNumber'])
			if(p['excludeDataAfterJSONExperimentNumber'] < float('inf')):		
				gateSweepHistory = dlu.filterHistoryLessThan(gateSweepHistory, 'experimentNumber', p['excludeDataAfterJSONExperimentNumber'])

			if p['specificPlotToCreate'] in ['FullSubthresholdCurveHistory','']:
				dpu.plotFullSubthresholdCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
			if p['specificPlotToCreate'] in ['FullTransferCurveHistory','']:
				dpu.plotFullTransferCurveHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
			if p['specificPlotToCreate'] in ['FullGateCurrentHistory','']:
				dpu.plotFullGateCurrentHistory(gateSweepHistory, parameters, sweepDirection=p['gateSweepDirection'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
			if p['specificPlotToCreate'] in ['OnAndOffCurrentHistory','']:
				dpu.plotOnAndOffCurrentHistory(gateSweepHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Gate Sweep history.")

	if(p['plotBurnOuts']):
		try:
			burnOutHistory = dlu.loadFullDeviceHistory(parameters['deviceDirectory'], burnOutFileName, parameters['deviceID'])
			
			if(p['excludeDataBeforeJSONIndex'] > 0):
				burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'index', p['excludeDataBeforeJSONIndex'])
			if(p['excludeDataAfterJSONIndex'] < float('inf')):			
				burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'index', p['excludeDataAfterJSONIndex'])
			
			if(p['excludeDataBeforeJSONExperimentNumber'] > 0):
				burnOutHistory = dlu.filterHistoryGreaterThan(burnOutHistory, 'experimentNumber', p['excludeDataBeforeJSONExperimentNumber'])
			if(p['excludeDataAfterJSONExperimentNumber'] < float('inf')):		
				burnOutHistory = dlu.filterHistoryLessThan(burnOutHistory, 'experimentNumber', p['excludeDataAfterJSONExperimentNumber'])

			if(p['showOnlySuccessfulBurns']):
				burnOutHistory = dlu.filterHistory(burnOutHistory, 'didBurnOut', True)
			
			if p['specificPlotToCreate'] in ['FullBurnOutHistory','']:
				dpu.plotFullBurnOutHistory(burnOutHistory, parameters, saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Burnout History")

	if(p['plotStaticBias']):
		try:
			staticBiasHistory = dlu.loadFullDeviceHistory(parameters['deviceDirectory'], staticBiasFileName, parameters['deviceID'])
			
			if(p['excludeDataBeforeJSONIndex'] > 0):
				staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'index', p['excludeDataBeforeJSONIndex'])
			if(p['excludeDataAfterJSONIndex'] < float('inf')):
				staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'index', p['excludeDataAfterJSONIndex'])
			
			if(p['excludeDataBeforeJSONExperimentNumber'] > 0):
				staticBiasHistory = dlu.filterHistoryGreaterThan(staticBiasHistory, 'experimentNumber', p['excludeDataBeforeJSONExperimentNumber'])
			if(p['excludeDataAfterJSONExperimentNumber'] < float('inf')):	
				staticBiasHistory = dlu.filterHistoryLessThan(staticBiasHistory, 'experimentNumber', p['excludeDataAfterJSONExperimentNumber'])
			
			if p['specificPlotToCreate'] in ['FullStaticBiasHistory','']:
				dpu.plotFullStaticBiasHistory(staticBiasHistory, parameters, timescale=p['timescale'], plotInRealTime=p['plotInRealTime'], includeDualAxis=p['includeBiasVoltageSubplot'], saveFigure=p['saveFiguresGenerated'], showFigure=showFigures)
		except FileNotFoundError:
			print("Error: Unable to find Static Bias History")

	if(showFigures):
		dpu.show()


if __name__ == '__main__':
    run(default_parameters)