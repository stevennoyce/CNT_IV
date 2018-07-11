default_parameters = {
		'ParametersFormatVersion': 3,
		'GateSweep':{
			'saveFileName': 'GateSweep',
			'isFastSweep': False,
			'isAlternatingSweep': False,
			'pulsedMeasurementOnTime': 0,
			'pulsedMeasurementOffTime': 0,
			'stepsInVGSPerDirection': 100,
			'pointsPerVGS': 3,
			'complianceCurrent':	100e-6,
			'drainVoltageSetPoint':	-0.5,
			'gateVoltageMinimum': 	-15,
			'gateVoltageMaximum': 	15
		},
		'BurnOut':{
			'saveFileName': 'BurnOut',
			'pointsPerRamp': 50,
			'pointsPerHold': 50,
			'complianceCurrent':	2e-3,
			'thresholdProportion':	0.8,
			'minimumAppliedDrainVoltage': 1.1,
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
			'totalBiasTime': 60*60,
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
			'numberOfSweeps': 1,
			'applyStaticBiasBetweenSweeps': False,
		},
		'AutoStaticBias':{
			'numberOfStaticBiases': 1,
			'applyGateSweepBetweenBiases': False,
			'turnChannelsOffBetweenBiases': False,
			'channelsOffTime': 0,
			'firstDelayBeforeMeasurementsBegin': 0,
			'numberOfBiasesBetweenIncrements': 1,
			'incrementStaticGateVoltage': 0,
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
			'plotBurnOuts':   True,
			'plotStaticBias': True,
			'specificPlotToCreate': '',
			'figureSizeOverride': None,
			'excludeDataBeforeJSONIndex': 0,
			'excludeDataAfterJSONIndex':  float('inf'),
			'excludeDataBeforeJSONExperimentNumber': 0,
			'excludeDataAfterJSONExperimentNumber':  float('inf'),
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
		'deviceRange':[],
		'dataFolder': 'data/',
		'plotsFolder': 'CurrentPlots/',
		'postFigures':	True,
		'NPLC':1
	}

def get():
	return default_parameters.copy()

def with_added(additional_parameters):
	defaults = get()
	combined = merge(defaults, additional_parameters)
	return combined

def merge(a, b):
	for key in b:
		if( (key in a) and (isinstance(a[key], dict)) and (isinstance(b[key], dict)) ):
			merge(a[key], b[key])
		else:
			a[key] = b[key]
	return a


