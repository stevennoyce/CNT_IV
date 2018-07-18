default_parameters = {
	'ParametersFormatVersion': 3,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'isFastSweep': False,
		'isAlternatingSweep': False,
		'pulsedMeasurementOnTime': 0,
		'pulsedMeasurementOffTime': 0,
		'stepsInVGSPerDirection': 100,
		'pointsPerVGS': 1,
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
		'totalBiasTime': 60,
		'measurementTime': 10,
		'complianceCurrent': 100e-6,
		'delayBeforeApplyingVoltage': 0,
		'delayBeforeMeasurementsBegin': 0,
		'gateVoltageSetPoint': 	-15,
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
		'doInitialGateSweep': True,
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
	'Results':{

	},
	'SensorData':{

	},
	'MeasurementSystem': ['B2912A','PCB2v14'][0],
	'NPLC':1,
	'deviceRange': [],
	'dataFolder': 'data/',
}

import copy

def get():
	return copy.deepcopy(default_parameters)

def with_added(additional_parameters):
	default = get()
	combined = merge(default, additional_parameters)
	return combined

def merge(a, b):
	for key in b:
		if( (key in a) and (isinstance(a[key], dict)) and (isinstance(b[key], dict)) ):
			merge(a[key], b[key])
		else:
			a[key] = b[key]
	return a


