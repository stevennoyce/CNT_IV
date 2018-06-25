from utilities import DataLoggerUtility as dlu
from utilities import DataPlotterUtility as dpu

# Chip Specifier
waferID = 'C139'
chipID = 'D'
deviceID = '1'

# Run Specifier
Run_Num = 1

# Model Fit Specifier for Data Range
Transconductance_Lower_Bound = 0
Transconductance_Upper_Bound = 18

default_parameters = {
	'ParametersFormatVersion': 3,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'isFastSweep': False,
		'isAlternatingSweep': False,
		'pulsedMeasurementOnTime': 0,
		'pulsedMeasurementOffTime': 0,
		'stepsInVGSPerDirection': 50,
		'pointsPerVGS': 1,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	-0.5,
		'gateVoltageMinimum':	-20,
		'gateVoltageMaximum': 	20
	},
	'BurnOut':{
		'saveFileName': 'BurnOut',
		'pointsPerRamp': 50,
		'pointsPerHold': 50,
		'complianceCurrent':	2e-3,
		'thresholdProportion':	0.8,
		'minimumAppliedDrainVoltage': 1.2,
		'gateVoltageSetPoint':	15.0,
		'drainVoltageMaxPoint':	10,
		'drainVoltagePlateaus': 10
	},
	'AutoBurnOut':{
		'targetOnOffRatio': 300,
		'limitBurnOutsAllowed': 8,
		'limitOnOffRatioDegradation': 0.7
	},
	'StaticBias':{
		'saveFileName': 'StaticBias',
		'totalBiasTime': 6*60*60,
		'measurementTime': 10,
		'complianceCurrent': 100e-6,
		'delayBeforeApplyingVoltage': 0,
		'delayBeforeMeasurementsBegin': 0,
		'gateVoltageSetPoint': 	15,
		'drainVoltageSetPoint':	-0.5,
		'gateVoltageWhenDone':  0,
		'drainVoltageWhenDone': 0
	},
	'AutoGateSweep':{
		'numberOfSweeps': 5,
		'applyStaticBiasBetweenSweeps': False,
		'usePreciseTimeBetweenSweepStarts': False,
		'timeBetweenSweepStarts': 5*60
	},
	'AutoStaticBias':{
		'numberOfStaticBiases': 31,
		'applyGateSweepBetweenBiases': True,
		'firstDelayBeforeMeasurementsBegin': 0,
		'numberOfBiasesBetweenIncrements': 1,
		'incrementStaticGateVoltage': -1,
		'incrementStaticDrainVoltage': 0,
		'incrementGateVoltageWhenDone': 0,
		'incrementDrainVoltageWhenDone': 0,
		'incrementDelayBeforeReapplyingVoltage': 0,
		'shuffleDelaysBeforeReapplyingVoltage': False
	},
	'DeviceHistory':{
		'showFiguresGenerated': True,
		'saveFiguresGenerated': True,
		'postFiguresGenerated': False,
		'plotGateSweeps': True,
		'plotBurnOuts':   False,
		'plotStaticBias': True,
		'specificPlotToCreate': '',
		'figureSizeOverride': None,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': 26,
		'excludeDataAfterJSONExperimentNumber':  28,
		'gateSweepDirection': ['both','forward','reverse'][0],
		'showOnlySuccessfulBurns': False,
		'timescale': ['','seconds','minutes','hours','days','weeks'][0],
		'plotInRealTime': True,
		'includeBiasVoltageSubplot': True
	},
	'ChipHistory':{
		
	},
	'Results':{

	},
	'SensorData':{

	},
	'MeasurementSystem':['B2912A','PCB2v14'][0],
	'waferID':waferID,
	'chipID':chipID,
	'deviceID':deviceID,
	'deviceRange':[],#devicesInRange(2,32,skip=False),
	'dataFolder':'data/',
	'plotsFolder':'CurrentPlots/',
	'postFigures':	True,
	'NPLC':1
}

jsonData = dlu.loadJSON('data/' + waferID + '/' + chipID + '/' + deviceID + '/', 'GateSweep.json')[Run_Num]
parameters = dict(default_parameters)
id_data = jsonData['Results']['id_data'][0]
vgs_data = jsonData['Results']['vgs_data'][0]
fit = dpu.linearFit(vgs_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound], id_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound]);
print('gm = ' + str(fit['slope']))
VT = fit['intercept'] / fit['slope']
print('VT = ' + str(VT))
fig, axes = dpu.initFigure(parameters, 1, 1, 'TransferCurve', 'Transconductance Model')
dpu.axisLabels(axes, "$V_{GS}$ (V)", "$I_{D}$ (A)")
data_line = dpu.scatter(axes, vgs_data, id_data, '#00009c', lineWidth=1)
dpu.setLabel(data_line, ' $I_{D}$ Data')
fit_line = dpu.scatter(axes, vgs_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound], fit['fitted_data'], '#ffa500', lineWidth=1)
dpu.setLabel(fit_line, ' Model')
axes.legend(loc='best', borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
saveName = waferID + "_" + chipID + "_" + deviceID + "_" + "Transfer_Curve"
dpu.adjustFigure(fig, saveName, parameters, saveFigure=True, showFigure=True)
dpu.show()


