from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Matplotlib Parameters **********

plt.style.use('seaborn-paper')

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial'
plt.rcParams['mathtext.bf'] = 'Arial:bold'

plt.rcParams["font.family"] = 'Times New Roman'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman'
plt.rcParams['mathtext.bf'] = 'Times New Roman'

plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['font.size'] = 8

plt.rcParams['axes.labelsize'] = 10*2
plt.rcParams['axes.titlesize'] = 10*2
plt.rcParams['legend.fontsize'] = 6*2
plt.rcParams['xtick.labelsize'] = 6*2
plt.rcParams['ytick.labelsize'] = 6*2
plt.rcParams['font.size'] = 6*2

plt.rcParams['xtick.major.size'] = 6
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['figure.figsize'] = [8,6]
plt.rcParams['figure.titlesize'] = 8
plt.rcParams['axes.formatter.use_mathtext'] = True
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.axisbelow'] = False
# plt.rcParams['figure.autolayout'] = True
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['axes.formatter.limits'] = [-2, 3]

# ********** Constants **********

publication_mode = False

plot_parameters = {
	'SubthresholdCurve': {
		'titles':[''],#['Subthreshold Curve'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}$ [V]',
		'ylabel':'$I_d$ [A]',
		'legend_title':'$V_{DS} = 0.5V$'
	},
	'TransferCurve':{
		'titles':[''],#['Transfer Curve'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}$ [V]',
		'ylabel':'$I_d$ [$\mu$A]',
		'legend_title':'$V_{DS} = 0.5V$'
	},
	'GateCurrent':{
		'titles':[''],#['Gate Leakage'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}$ [V]',
		'ylabel':'$I_g$ [A]',
		'legend_title':'$V_{DS} = 0.5V$'
	},
	'BurnOut':{
		'titles':['Metallic CNT Burnout', 'Current Measured', 'Applied Voltage'],
		'figsize':(8,6),
		'subplot_height_ratio':[1],
		'subplot_width_ratio':[1,1],
		'colorMap':'Blues',
		'vds_label':'Drain Voltage, $V_{DS}$ [V]',
		'id_micro_label':'$I_d$ [$\mu$A]',
		'time_label':'Time, [sec]',
		'id_annotation':'burn current',
		'legend_title':'$V_{gs} = +15V$'
	},
	'StaticBias':{
		'titles':[''],#['Static Bias'],
		'figsize':(2*2.2,2*1.6),#(5,4),
		'colorMap':'plasma',
		'xlabel':'Time, [{:}]',
		'ylabel':'$I_d$ [$\mu$A]',
		'vds_label': '$V_{DS}$ [V]',
		'vgs_label': '$V_{GS}$ [V]',
		'subplot_height_ratio':[3,1],
		'subplot_width_ratio': [1],
		'subplot_spacing': 0.03
	},
	'OnCurrent':{
		'titles':[''],#['On/Off-Current'],
		'figsize':(2*2.2,2*1.7),#(5,4),
		'time_label':'Time, [{:}]',
		'index_label':'Time Index of Gate Sweep [#]',
		'ylabel':'On-Current [A]',
		'ylabel_dual_axis':'Off-Current [A]'
	},
	'ChipHistory':{
		'titles':['Chip History'],
		'figsize':(5,4),
		'subplot_size_ratio':[1],
		'xlabel':'Device',
		'ylabel':'On/Off Ratio, (Order of Mag)'
	}
}



# ********** API **********

def plotJSON(jsonData, parameters, lineColor):
	if(jsonData['runType'] == 'GateSweep'):
		plotFullSubthresholdCurveHistory([jsonData], parameters, saveFigure=True, showFigure=True)
	elif(jsonData['runType'] == 'BurnOut'):
		plotFullBurnOutHistory([jsonData], parameters, saveFigure=True, showFigure=True)
	elif(jsonData['runType'] == 'StaticBias'):
		plotFullStaticBiasHistory([jsonData], parameters, timescale='', plotInRealTime=True, saveFigure=True, showFigure=True)
	else:
		raise NotImplementedError("Error: Unable to determine plot type")

def plotFullSubthresholdCurveHistory(deviceHistory, parameters, sweepDirection='both', saveFigure=False, showFigure=True):
	# Init Figure
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax = initFigure(1, 1, 'SubthresholdCurve', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax.set_title(plot_parameters['SubthresholdCurve']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['SubthresholdCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		colorBar(fig, colorMap['smap'])
	
	# Plot
	for i in range(len(deviceHistory)):
		plotSubthresholdCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection, includeLabel=False)			
	
	# Add Legend and save figure
	ax.legend([],[], loc='lower left', title=plot_parameters['SubthresholdCurve']['legend_title'], labelspacing=0)
	adjustFigure(fig, 'FullSubthresholdCurves', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotFullTransferCurveHistory(deviceHistory, parameters, sweepDirection='both', saveFigure=False, showFigure=True):
	# Init Figure
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax = initFigure(1, 1, 'TransferCurve', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax.set_title(plot_parameters['TransferCurve']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['TransferCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		colorBar(fig, colorMap['smap'])

	# If first segment of device history is all negative current, flip data
	if((len(deviceHistory) > 0) and (np.mean(deviceHistory[0]['current1s']) < 0)):
		deviceHistory = scaledData(deviceHistory, 'current1s', -1)
		plot_parameters['TransferCurve']['ylabel'] = '$-I_d$ [$\mu$A]'
	
	# Plot
	for i in range(len(deviceHistory)):
		plotTransferCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection)	

	# Add Legend and save figure	
	ax.legend([],[], loc='best', title=plot_parameters['TransferCurve']['legend_title'], labelspacing=0)
	adjustFigure(fig, 'FullTransferCurves', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotFullGateCurrentHistory(deviceHistory, parameters, sweepDirection='both', saveFigure=False, showFigure=True):
	# Init Figure
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax = initFigure(1, 1, 'GateCurrent', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax.set_title(plot_parameters['GateCurrent']['titles'][0])
	if(len(deviceHistory) <= 0):
		return

	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['GateCurrent']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		colorBar(fig, colorMap['smap'])

	# Plot
	for i in range(len(deviceHistory)):
		plotGateCurrent(ax, deviceHistory[i], colors[i], sweepDirection)
	
	# Add Legend and save figure
	ax.legend([],[], loc='best', title=plot_parameters['GateCurrent']['legend_title'], labelspacing=0)
	adjustFigure(fig, 'FullGateCurrents', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotFullBurnOutHistory(deviceHistory, parameters, saveFigure=False, showFigure=True):
	# Init Figure	
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, (ax1, ax2) = initFigure(1, 2, 'BurnOut', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(224)
	ax1.set_title(plot_parameters['BurnOut']['titles'][0])
	ax2.set_title(plot_parameters['BurnOut']['titles'][1])
	ax3.set_title(plot_parameters['BurnOut']['titles'][2])
	if(len(deviceHistory) <= 0):
		return

	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['BurnOut']['colorMap'], 0.6, 1.0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	else:
		plt.sca(ax1)
		colorBar(fig, colorMap['smap'])

	# Plot
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i])

	# Add Legend and save figure
	ax3.legend([],[], loc='lower right', title=plot_parameters['BurnOut']['legend_title'], labelspacing=0)
	adjustFigure(fig, 'FullBurnOut', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotFullStaticBiasHistory(deviceHistory, parameters, timescale='', plotInRealTime=True, includeDualAxis=True, saveFigure=False, showFigure=True):
	# Init Figure
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	if(includeDualAxis):
		fig, (ax1, ax2) = initFigure(2, 1, 'StaticBias', parameters['chipID'], parameters['deviceID'], titleNumbers, shareX=True)
		ax = ax1
		ax3 = ax2.twinx()
	else:
		fig, ax = initFigure(1, 1, 'StaticBias', parameters['chipID'], parameters['deviceID'], titleNumbers)
	if(plot_parameters['StaticBias']['titles'][0] != ''):
		ax.set_title(plot_parameters['StaticBias']['titles'][0])
	if(len(deviceHistory) <= 0):
		return

	# Build Color Map
	colors = colorsFromMap(plot_parameters['StaticBias']['colorMap'], 0, 0.87, len(deviceHistory))['colors']

	# If timescale is unspecified, choose an appropriate one based on the data range
	if(timescale == '' and (len(deviceHistory) > 0)):
		timerange = deviceHistory[-1]['timestamps'][-1] - deviceHistory[0]['timestamps'][0]
		if(timerange < 2*60):
			timescale = 'seconds'
		elif(timerange < 2*60*60):
			timescale = 'minutes'
		elif(timerange < 2*60*60*24):
			timescale = 'hours'
		elif(timerange < 2*60*60*24*7):
			timescale = 'days'
		else:
			timescale = 'weeks'

	# Rescale timestamp data by factor related to the time scale
	deviceHistory = scaledData(deviceHistory, 'timestamps', 1/secondsPer(timescale))
	
	# If first segment of device history is all negative current, flip data
	if((len(deviceHistory) > 0) and (np.mean(deviceHistory[0]['current1s']) < 0)):
		deviceHistory = scaledData(deviceHistory, 'current1s', -1)
		plot_parameters['StaticBias']['ylabel'] = '$-I_d$ [$\mu$A]'
	
	time_offset = 0
	dotted_lines = []
	parameter_labels = {'drainVoltageSetPoint':[],'gateVoltageSetPoint':[]}
	for i in range(len(deviceHistory)):
		# Plot
		if(plotInRealTime):
			time_offset = (deviceHistory[i]['timestamps'][0] - deviceHistory[0]['timestamps'][0])
		else:
			time_offset = (0) if(i == 0) else (time_offset + (deviceHistory[i-1]['timestamps'][-1] - deviceHistory[i-1]['timestamps'][0]))
		
		plotStaticBias(ax, deviceHistory[i], colors[i], time_offset, timescale, addLabel=False)
		if(includeDualAxis):
			vds_line = plotOverTime(ax2, deviceHistory[i]['timestamps'], [deviceHistory[i]['StaticBias']['drainVoltageSetPoint']]*len(deviceHistory[i]['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][0], time_offset)
			vgs_line = plotOverTime(ax3, deviceHistory[i]['timestamps'], [deviceHistory[i]['StaticBias']['gateVoltageSetPoint']]*len(deviceHistory[i]['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][1], time_offset)

		# Compare current plot's parameters to the next ones, and save any differences
		if('drainVoltageSetPoint' in deviceHistory[i] and 'drainVoltageSetPoint' in deviceHistory[i-1]):
			# backwards compatibility for old parameters format
			if (i == 0) or deviceHistory[i]['drainVoltageSetPoint'] != deviceHistory[i-1]['drainVoltageSetPoint']:
				dotted_lines.append({'x':time_offset})
				parameter_labels['drainVoltageSetPoint'].append({'x':time_offset, 'drainVoltageSetPoint':deviceHistory[i]['drainVoltageSetPoint']})
				parameter_labels['gateVoltageSetPoint'].append({'x':time_offset, 'gateVoltageSetPoint':deviceHistory[i]['gateVoltageSetPoint']})
		else:
			if((i == 0) or (deviceHistory[i]['StaticBias'] != deviceHistory[i-1]['StaticBias'])):
				dotted_lines.append({'x':time_offset})
				for key in set(deviceHistory[i]['StaticBias'].keys()).intersection(deviceHistory[i-1]['StaticBias'].keys()):
					if((i == 0) or deviceHistory[i]['StaticBias'][key] != deviceHistory[i-1]['StaticBias'][key]):
						if(key not in parameter_labels):
							parameter_labels[key] = []
						parameter_labels[key].append({'x':time_offset, key:deviceHistory[i]['StaticBias'][key]})
	
	# Increase height of the plot to give more room for labels
	if len(dotted_lines) > 1:
		x0, x1, y0, y1 = ax.axis()
		ax.axis((x0,x1,y0,1.2*y1))
	
		# Draw dotted lines between ANY plots that have different parameters
		for i in range(len(dotted_lines)):
			ax.annotate('', xy=(dotted_lines[i]['x'], ax.get_ylim()[0]), xytext=(dotted_lines[i]['x'], ax.get_ylim()[1]), xycoords='data', arrowprops=dict(arrowstyle='-', color=(0,0,0,0.3), ls=':', lw=1))
		
		if(not includeDualAxis):
			# Add V_ds annotation
			for i in range(len(parameter_labels['drainVoltageSetPoint'])):
				ax.annotate(' $V_{DS} = $'+'{:.1f}V'.format(parameter_labels['drainVoltageSetPoint'][i]['drainVoltageSetPoint']), xy=(parameter_labels['drainVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.99 - 0*0.03*i)), xycoords='data', ha='left', va='top', rotation=-90)

			# Add V_gs annotation
			for i in range(len(parameter_labels['gateVoltageSetPoint'])):
				ax.annotate(' $V_{GS} = $'+'{:.0f}V'.format(parameter_labels['gateVoltageSetPoint'][i]['gateVoltageSetPoint']), xy=(parameter_labels['gateVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.09 - 0*0.03*i)), xycoords='data', ha='left', va='bottom', rotation=-90)
			
	else:
		legend_title = ''
		legend_title += '$V_{DS}$ = ' + '{:.2f}V\n'.format(parameter_labels['drainVoltageSetPoint'][0]['drainVoltageSetPoint'])
		legend_title += '$V_{GS}$ = ' + '{:.1f}V'.format(parameter_labels['gateVoltageSetPoint'][0]['gateVoltageSetPoint'])
		ax.legend([],[], loc='best', title=legend_title, labelspacing=0)
	
	# Add Grounding annotation
	# for i in range(len(parameter_labels['groundDrainWhenDone'])):
	# 	ax.annotate(' Grounded Drain: {:}'.format(parameter_labels['groundDrainWhenDone'][i]['groundDrainWhenDone']), xy=(parameter_labels['groundDrainWhenDone'][i]['x'], ax.get_ylim()[1]*(0.94 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')
	# for i in range(len(parameter_labels['groundGateWhenDone'])):
	# 	ax.annotate(' Grounded Gate: {:}'.format(parameter_labels['groundGateWhenDone'][i]['groundGateWhenDone']), xy=(parameter_labels['groundGateWhenDone'][i]['x'], ax.get_ylim()[1]*(0.92 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')

	# Add legend and axis labels and save figure
	if(includeDualAxis):
		# Adjust y-axis limits
		includeOriginOnYaxis(ax2)
		includeOriginOnYaxis(ax3)
		# Axis labels
		ax1.set_ylabel(plot_parameters['StaticBias']['ylabel'])
		ax2.set_xlabel(plot_parameters['StaticBias']['xlabel'].format(timescale))
		ax2.set_ylabel(plot_parameters['StaticBias']['vds_label'])
		ax3.set_ylabel(plot_parameters['StaticBias']['vgs_label'])
		# Legend
		setLabel(vds_line, '$V_{DS}$')
		setLabel(vgs_line, '$V_{GS}$')
		lines1, labels1 = ax2.get_legend_handles_labels()
		lines2, labels2 = ax3.get_legend_handles_labels()
		ax2.legend(lines1 + lines2, labels1 + labels2, loc='best', ncol=2, borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1, columnspacing=0.1)
		# Adjust tick alignment
		[tick.set_verticalalignment('top') for tick in ax2.yaxis.get_majorticklabels()]
		adjustFigure(fig, 'FullStaticBias', parameters, saveFigure=saveFigure, showFigure=showFigure, subplotHeightPad=plot_parameters['StaticBias']['subplot_spacing'])
	else:
		axisLabels(ax, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])
		adjustFigure(fig, 'FullStaticBias', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotOnAndOffCurrentHistory(deviceHistory, parameters, timescale='', plotInRealTime=True, saveFigure=False, showFigure=True):
	# Init Figure
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax1 = initFigure(1, 1, 'OnCurrent', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax2 = ax1.twinx()
	ax1.set_title(plot_parameters['OnCurrent']['titles'][0])
	if(len(deviceHistory) <= 0):
		return

	# If timescale is unspecified, choose an appropriate one based on the data range
	if(timescale == '' and (len(deviceHistory) > 0)):
		timerange = flatten(deviceHistory[-1]['timestamps'])[-1] - flatten(deviceHistory[0]['timestamps'])[0]
		if(timerange < 2*60):
			timescale = 'seconds'
		elif(timerange < 2*60*60):
			timescale = 'minutes'
		elif(timerange < 2*60*60*24):
			timescale = 'hours'
		elif(timerange < 2*60*60*24*7):
			timescale = 'days'
		else:
			timescale = 'weeks'

	# Rescale timestamp data by factor related to the time scale
	deviceHistory = scaledData(deviceHistory, 'timestamps', 1/secondsPer(timescale))

	# Build On/Off Current lists
	onCurrents = []
	offCurrents = []
	timestamps = []
	for deviceRun in deviceHistory:
		onCurrents.append(deviceRun['onCurrent'])
		offCurrents.append(deviceRun['offCurrent'])
		timestamps.append(flatten(deviceRun['timestamps'])[0])

	# Plot On Current
	if(plotInRealTime):
		line = plotOverTime(ax1, timestamps, onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=0, makerSize=6, lineWidth=0)
		axisLabels(ax1, x_label=plot_parameters['OnCurrent']['time_label'].format(timescale), y_label=plot_parameters['OnCurrent']['ylabel'])
	else:
		line = scatter(ax1, range(len(onCurrents)), onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], 6)
		axisLabels(ax1, x_label=plot_parameters['OnCurrent']['index_label'].format(timescale), y_label=plot_parameters['OnCurrent']['ylabel'])
	setLabel(line, 'On-Currents')
	ax1.set_ylim(bottom=0)

	# Plot Off Current
	if(plotInRealTime):
		line = plotOverTime(ax2, timestamps, offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], offset=0, makerSize=2, lineWidth=0)
	else:
		line = scatter(ax2, range(len(offCurrents)), offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 2)
	setLabel(line, 'Off-Currents')
	ax2.set_ylabel(plot_parameters['OnCurrent']['ylabel_dual_axis'])
	
	# Add Legend and save figure
	lines1, labels1 = ax1.get_legend_handles_labels()
	lines2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower left')
	adjustFigure(fig, 'OnAndOffCurrents', parameters, saveFigure=saveFigure, showFigure=showFigure)

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory, parameters):
	# Init Figure
	fig, ax = initFigure(1, 1, 'ChipHistory', parameters['chipID'], parameters['deviceID'], '')
	ax.set_title(plot_parameters['ChipHistory']['titles'][0])

	# Build On/Off Ratio lists
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['onOffRatio'])

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	# Plot First Run
	line = scatter(ax, range(len(devices)), firstOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 6)
	setLabel(line, 'First Run')
	
	# Plot Most Recent Run
	line = scatter(ax, range(len(devices)), lastOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][0], 4)
	setLabel(line, 'Most Recent Run')

	# Label axes
	axisLabels(ax, x_label=plot_parameters['ChipHistory']['xlabel'], y_label=plot_parameters['ChipHistory']['ylabel'])
	tickLabels(ax, devices, rotation=90)
	
	# Add Legend and save figure
	ax.legend(loc='best')
	adjustFigure(fig, 'ChipHistory', parameters, saveFigure=False, showFigure=True)

def show():
	plt.show()



# ***** Device Plots *****
def plotGateSweepCurrent(axis, jsonData, lineColor, direction='both', currentSource='drain', logScale=True, scaleCurrentBy=1):
	if(currentSource == 'gate'):
		currentData = 'current2s'
	elif(currentSource == 'drain'):
		currentData = 'current1s'
	
	x = jsonData['gateVoltages']
	y = jsonData[currentData]

	# Sort data if it was collected in an unordered fashion
	try:
		if(jsonData['GateSweep']['isAlternatingSweep']):
			forward_x, forward_y = zip(*sorted(zip(x[0], y[0])))
			reverse_x, reverse_y = zip(*reversed(sorted(zip(x[1], y[1]))))
			x = [list(forward_x), list(reverse_x)]
			y = [list(forward_y), list(reverse_y)]
	except:
		pass

	# Plot only forward or reverse sweeps of the data (also backwards compatible to old format)
	if(direction == 'forward'):
		if(isinstance(x[0], list)):	
			x = x[0]
			y = y[0]
		else:
			x = x[0:int(len(x)/2)]
			y = y[0:int(len(x)/2)]
	elif(direction == 'reverse'):
		if(isinstance(x[0], list)):	
			x = x[1]
			y = y[1]
		else:
			x = x[int(len(x)/2):]
			y = y[int(len(y)/2):]
	else:
		x = flatten(x)
		y = flatten(y)

	# Make y-axis a logarithmic scale
	if(logScale):
		y = abs(np.array(y))
		semiLogScale(axis)

	# Scale the data by a given factor
	y = np.array(y)*scaleCurrentBy

	# data contains multiple y-values per x-value
	if(x[0] == x[1]):
		line = plotWithErrorBars(axis, x, y, lineColor)
	else:
		line = scatter(axis, x, y, lineColor, markerSize=2, lineWidth=1)

	return line

def plotSubthresholdCurve(axis, jsonData, lineColor, direction='both', includeLabel=False, fitSubthresholdSwing=False):
	line = plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=True, scaleCurrentBy=1)
	axisLabels(axis, x_label=plot_parameters['SubthresholdCurve']['xlabel'], y_label=plot_parameters['SubthresholdCurve']['ylabel'])
	if(includeLabel): 
		#setLabel(line, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])))
		setLabel(line, 'max $|I_{g}|$'+': {:.2e}'.format(max(abs(np.array(flatten(jsonData['current2s']))))))
	if(fitSubthresholdSwing):
		startIndex, endIndex = steepestRegion(np.log10(np.abs(jsonData['current1s'][0])), 10)
		vgs_region = jsonData['voltage2s'][0][startIndex:endIndex]
		id_region = jsonData['current1s'][0][startIndex:endIndex]
		fitted_region = semilogFit(vgs_region, id_region)['fitted_data']
		print(avgSubthresholdSwing(vgs_region, fitted_region))
		plot(axis, vgs_region, fitted_region, lineColor='b', lineStyle='--')

def plotTransferCurve(axis, jsonData, lineColor, direction='both'):
	plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=False, scaleCurrentBy=1e6)
	axisLabels(axis, x_label=plot_parameters['TransferCurve']['xlabel'], y_label=plot_parameters['TransferCurve']['ylabel'])

def plotGateCurrent(axis, jsonData, lineColor, direction='both'):
	plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='gate', logScale=False, scaleCurrentBy=1)
	axisLabels(axis, x_label=plot_parameters['GateCurrent']['xlabel'], y_label=plot_parameters['GateCurrent']['ylabel'])

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor):
	plot(axis1, jsonData['voltage1s'], (np.array(jsonData['current1s'])*10**6), lineColor)
	axisLabels(axis1, x_label=plot_parameters['BurnOut']['vds_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	# Add burn threshold annotation
	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['BurnOut']['thresholdProportion'] * 10**6
	axis1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, linestyle='--', linewidth=1)
	axis1.annotate(plot_parameters['BurnOut']['id_annotation'], xy=(0, currentThreshold), xycoords='data', horizontalalignment='left', verticalalignment='bottom', color=lineColor)
	
	plotOverTime(axis2, jsonData['timestamps'], (np.array(jsonData['current1s'])*10**6), lineColor)	
	axisLabels(axis2, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	plotOverTime(axis3, jsonData['timestamps'], jsonData['voltage1s'], lineColor)
	axisLabels(axis3, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['vds_label'])

def plotStaticBias(axis, jsonData, lineColor, timeOffset, timescale='seconds', addLabel=True):
	plotOverTime(axis, jsonData['timestamps'], (np.array(jsonData['current1s'])*(10**6)), lineColor, timeOffset)	
	if(addLabel):
		axisLabels(axis, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])




# ***** Figures *****

def initFigure(rows, columns, type, chipID, deviceID, testLabel, shareX=False):
	if(rows > 1 or columns > 1):
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[type]['figsize'], sharex=shareX, gridspec_kw={'width_ratios':plot_parameters[type]['subplot_width_ratio'], 'height_ratios':plot_parameters[type]['subplot_height_ratio']})
	else:
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[type]['figsize'])
	title = chipID + ':' + deviceID + testLabel
	if(not publication_mode):
		fig.suptitle(title)
	return fig, axes

def adjustFigure(figure, saveName, parameters, saveFigure, showFigure, subplotWidthPad=0.5, subplotHeightPad=0.5):
	# figure.set_size_inches(2.2,1.6) # Static Bias
	# figure.set_size_inches(1.4,1.6) # Subthreshold Curve
	# figure.set_size_inches(2.2,1.7) # On/Off-Current
	figure.tight_layout()
	plt.subplots_adjust(wspace=subplotWidthPad, hspace=subplotHeightPad)
	if(saveFigure):
		plt.savefig(parameters['plotsFolder'] + saveName + '.png', transparent=True)
		plt.savefig(parameters['plotsFolder'] + saveName + '.pdf', transparent=True)
	if(not showFigure):
		plt.close(figure)

def colorsFromMap(mapName, colorStartPoint, colorEndPoint, numberOfColors):
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=mapName)
	return {'colors':[scalarColorMap.to_rgba(i) for i in np.linspace(colorStartPoint, colorEndPoint, numberOfColors)], 'smap':scalarColorMap}

def scaledData(deviceHistory, dataToScale, scalefactor):
	data = list(deviceHistory)
	for i in range(len(data)):
		if(isinstance(data[i][dataToScale][0], list)):
			for j in range(len(data[i][dataToScale])):
				data[i][dataToScale][j] = list(np.array(data[i][dataToScale][j])*scalefactor)
		else:
			data[i][dataToScale] = list(np.array(data[i][dataToScale])*scalefactor)
	return data



# ***** Plots ***** 

def plot(axis, x, y, lineColor, lineStyle=None):
	return axis.plot(x, y, color=lineColor, linestyle=lineStyle)[0]

def scatter(axis, x, y, lineColor, markerSize, lineWidth=0):
	return axis.plot(x, y, color=lineColor, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=lineWidth)[0]

def plotWithErrorBars(axis, x, y, lineColor):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	return axis.errorbar(x_unique, avg, yerr=std, color=lineColor, capsize=4, capthick=0.5, elinewidth=0.5)[0]

def plotOverTime(axis, timestamps, y, lineColor, offset=0, makerSize=1, lineWidth=1):
	zeroed_timestamps = list( np.array(timestamps) - timestamps[0] + offset )
	return axis.plot(zeroed_timestamps, y, color=lineColor, marker='o', markersize=makerSize, linewidth=lineWidth)[0]

def colorBar(fig, scalarMappableColorMap, ticks=[0,1], tick_labels=['End','Start'], axisLabel='Time $\\rightarrow$'):
	scalarMappableColorMap._A = []
	cbar = fig.colorbar(scalarMappableColorMap, pad=0.02, aspect=50)
	cbar.set_ticks(ticks)
	cbar.ax.set_yticklabels(tick_labels, rotation=270)
	cbar.ax.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
	cbar.ax.yaxis.get_majorticklabels()[1].set_verticalalignment('top')
	cbar.set_label(axisLabel, rotation=270)



# ***** Labels *****

def setLabel(line, label):
	line.set_label(label)

def semiLogScale(axis):
	axis.set_yscale('log')

def axisLabels(axis, x_label, y_label):
	axis.set_xlabel(x_label)
	axis.set_ylabel(y_label)

def tickLabels(axis, labelList, rotation=0):
	axis.set_xticklabels(labelList)
	axis.set_xticks(range(len(labelList)))
	axis.xaxis.set_tick_params(rotation=rotation)

def includeOriginOnYaxis(axis):
	if(axis.get_ylim()[1] < 0):
		axis.set_ylim(top=0)
	elif(axis.get_ylim()[0] > 0):
		axis.set_ylim(bottom=0)



# ***** Curve Fitting *****

def linearFit(x, y):
	slope, intercept = np.polyfit(x, y, 1)
	fitted_data = [slope*x[i] + intercept for i in range(len(x))]
	return {'fitted_data': fitted_data,'slope':slope, 'intercept':intercept}

def quadraticFit(x, y):
	a, b, c = np.polyfit(x, y, 2)
	fitted_data = [(a*(x[i]**2) + b*x[i] + c) for i in range(len(x))]
	return {'fitted_data': fitted_data, 'a':a, 'b':b, 'c':c}

def semilogFit(x, y):
	fit_results = linearFit(x, np.log10(np.abs(y)))
	fitted_data = [10**(fit_results['fitted_data'][i]) for i in range(len(fit_results['fitted_data']))]
	return {'fitted_data': fitted_data}

def steepestRegion(data, numberOfPoints):
	maxSlope = 0
	index = 0
	for i in range(len(data) - 1):
		diff = abs(data[i] - data[i+1])
		if(diff > maxSlope):
			maxSlope = diff
			index = i
	regionStart = max(0, index - numberOfPoints/2)
	regionEnd = min(len(data)-1, index + numberOfPoints/2)
	return (int(regionStart), int(regionEnd))



# ***** Metrics *****
def avgSubthresholdSwing(vgs_data, id_data):
	return abs( vgs_data[0] - vgs_data[-1] / (np.log10(np.abs(id_data[0])) - np.log10(np.abs(id_data[-1]))) ) 


# ***** Statistics *****

def avgAndStdAtEveryPoint(x, y):
	x_uniques = []
	y_averages = []
	y_standardDeviations = []
	i = 0
	while (i < len(y)):
		j = nextIndexToBeDifferent(x, i)
		x_uniques.append(x[i])
		y_averages.append(np.mean(y[i:j]))
		y_standardDeviations.append(np.std(y[i:j]))
		i = j

	return (x_uniques, y_averages, y_standardDeviations)

def nextIndexToBeDifferent(data, i):
	value = data[i]
	while((i < len(data)) and (data[i] == value)):
		i += 1
	return i

def secondsPer(amountOfTime):
	if(amountOfTime == 'seconds'):
		return 1
	elif(amountOfTime == 'minutes'):
		return 60
	elif(amountOfTime == 'hours'):
		return 3600
	elif(amountOfTime == 'days'):
		return 3600*24
	elif(amountOfTime == 'weeks'):
		return 3600*24*7
	else: 
		return 0

# ***** Array Manipulation *****

def flatten(dataList):
	data = list([dataList])
	while(isinstance(data[0], list)):
		data = [(item) for sublist in data for item in sublist]
	return data

def getTitleTestNumbersLabel(deviceHistory):
	titleNumbers = ''
	if len(deviceHistory) > 0:
		test1Num = deviceHistory[0]['experimentNumber']
		test2Num = deviceHistory[-1]['experimentNumber']
		if test1Num == test2Num:
			titleNumbers = ', Test {:}'.format(test1Num)
		else:
			titleNumbers = ', Tests {:}-{:}'.format(test1Num, test2Num)
	return titleNumbers

