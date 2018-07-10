import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Matplotlib Parameters **********

plt.style.use('seaborn-paper')

# plt.rcParams['mathtext.fontset'] = 'custom'
# plt.rcParams['mathtext.rm'] = 'Arial'
# plt.rcParams['mathtext.it'] = 'Arial'
# plt.rcParams['mathtext.bf'] = 'Arial:bold'

# plt.rcParams["font.family"] = 'Times New Roman'
# plt.rcParams['mathtext.rm'] = 'Times New Roman'
# plt.rcParams['mathtext.it'] = 'Times New Roman'
# plt.rcParams['mathtext.bf'] = 'Times New Roman'

# Used for the DRC Abstract
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['font.size'] = 8

# Minimum Sizes based on Dr. Franklin's Publications (Body text is 10 pt)
plt.rcParams['axes.labelsize'] = 6
plt.rcParams['axes.titlesize'] = 6
plt.rcParams['legend.fontsize'] = 4.5
plt.rcParams['xtick.labelsize'] = 4.5
plt.rcParams['ytick.labelsize'] = 4.5
plt.rcParams['font.size'] = 4.5

# Sizes based on Nature Nanotechnology (Body text is 9 pt)
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['font.size'] = 7

# Steven's preferences loosely based on Nature Nanotechnology (Body text is 9 pt)
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 7
plt.rcParams['legend.fontsize'] = 6
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rcParams['font.size'] = 6

plt.rcParams['axes.labelpad'] = 0
plt.rcParams['axes.titlepad'] = 6
plt.rcParams['ytick.major.pad'] = 2
plt.rcParams['xtick.major.pad'] = 2

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

plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5
plt.rcParams['xtick.major.size'] = 3
plt.rcParams['ytick.major.size'] = 3

plt.rcParams['xtick.minor.width'] = 0.5
plt.rcParams['ytick.minor.width'] = 0.5
plt.rcParams['xtick.minor.size'] = 1
plt.rcParams['ytick.minor.size'] = 1

plt.rcParams['axes.formatter.limits'] = [-2, 3]

# Change to Type 2/TrueType fonts (editable text)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# ********** Constants **********

publication_mode = False
default_png_dpi = 120
plotGradient = False
errorBarsOn = True
autoStaticBiasSegmentDividers = False
plotOffCurrent = True


plot_parameters = {
	'SubthresholdCurve': {
		'titles':[''],#['Subthreshold Curve'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}^{Sweep}$ [V]',
		'ylabel':'$I_{D}$ [A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}}$\n  = {:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'TransferCurve':{
		'titles':[''],#['Transfer Curve'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}^{{Sweep}}$ [V]',
		'ylabel':'$I_{D}$ [$\mu$A]',
		'neg_label':'$-I_{D}$ [$\mu$A]',
		'ii_label':'$I_{D}$, $I_{G}$ [$\mu$A]',
		'neg_ii_label':'$-I_{D}$, $I_{G}$ [$\mu$A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}}$\n  = {:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'GateCurrent':{
		'titles':[''],#['Gate Leakage'],
		'figsize':(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{GS}^{{Sweep}}$ [V]',
		'ylabel':'$I_{G}$ [A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}} = ${:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'BurnOut':{
		'titles':['Metallic CNT Burnout', 'Current Measured', 'Applied Voltage'],
		'figsize':(8,4.5),
		'subplot_height_ratio':[1],
		'subplot_width_ratio':[1,1],
		'colorMap':'Blues',
		'vds_label':'$V_{DS}$ [V]',
		'id_micro_label':'$I_{D}$ [$\mu$A]',
		'time_label':'Time [sec]',
		'id_annotation':'burn current',
		'legend_title':'$V_{GS} = +15V$'
	},
	'StaticBias':{
		'titles':[''],#['Static Bias'],
		'figsize':(2*2.2,2*1.6),#(5,4),
		'colorMap':'plasma',
		'xlabel':'Time [{:}]',
		'ylabel':'$I_{D}$ [$\mu$A]',
		'vds_label': '$V_{DS}^{{Hold}}$ [V]',
		'vgs_label': '$V_{GS}^{{Hold}}$ [V]',
		'subplot_height_ratio':[3,1],
		'subplot_width_ratio': [1],
		'subplot_spacing': 0.03
	},
	'OnCurrent':{
		'titles':[''],#['On/Off-Current'],
		'figsize':(2*2.2,2*1.7),#(5,4),
		'time_label':'Time [{:}]',
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



def timeToString(seconds):
	time = seconds
	unit = 's'
	threshold = 2
	
	if seconds >= 60*60*24*7:
		time = seconds/(60*60*24*7)
		unit = 'wk'
	elif seconds >= 60*60*24:
		time = seconds/(60*60*24)
		unit = 'day' if int(time) == 1 else 'days'
	elif seconds >= 60*60:
		time = seconds/(60*60)
		unit = 'hr'
	elif seconds >= 60:
		time = seconds/(60)
		unit = 'min'
	elif seconds >= 60:
		time = seconds/(1)
		unit = 's'
	
	return '{} {}'.format(int(time), unit)


# ********** API **********

def plotJSON(jsonData, parameters, lineColor):
	if(jsonData['runType'] == 'GateSweep'):
		plotFullSubthresholdCurveHistory([jsonData], parameters, saveFigure=True, showFigure=True)
		plotFullTransferCurveHistory([jsonData], parameters, includeGateCurrent=True, saveFigure=True, showFigure=True)
		#plotFullGateCurrentHistory([jsonData], parameters, saveFigure=True, showFigure=True)
	elif(jsonData['runType'] == 'BurnOut'):
		plotFullBurnOutHistory([jsonData], parameters, saveFigure=True, showFigure=True)
	elif(jsonData['runType'] == 'StaticBias'):
		plotFullStaticBiasHistory([jsonData], parameters, timescale='', plotInRealTime=True, saveFigure=True, showFigure=True)
	else:
		raise NotImplementedError("Error: Unable to determine plot type")

def plotFullSubthresholdCurveHistory(deviceHistory, parameters, sweepDirection='both', saveFigure=False, showFigure=True):
	# Init Figure
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	fig, ax = initFigure(parameters, 1, 1, 'SubthresholdCurve', testLabel)
	ax.set_title(plot_parameters['SubthresholdCurve']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['SubthresholdCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		elapsedTime = timeToString(deviceHistory[-1]['Results']['timestamps'][0][0] - deviceHistory[0]['Results']['timestamps'][-1][-1])
		
		axisLabel = 'Time'
		if len(deviceHistory) > 1:
			biasTimeSeconds = deviceHistory[1]['Results']['timestamps'][-1][-1] - deviceHistory[0]['Results']['timestamps'][0][0]
			axisLabel = '[$t_{{Hold}}$ = {}]'.format(timeToString(biasTimeSeconds))
		
		colorBar(fig, colorMap['smap'], ticks=[0,0.6,1], tick_labels=[elapsedTime, axisLabel, '$t_0$'], axisLabel='')
	
	# Plot
	for i in range(len(deviceHistory)):
		plotSubthresholdCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection, fitSubthresholdSwing=False, includeLabel=False, lineStyle=None)			
	
	ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=10))
	
	# Add Legend and save figure
	ax.legend([],[], loc='lower left', title=getLegendTitle(deviceHistory, 'SubthresholdCurve', 'GateSweep', includeVdsRange=True, includeSubthresholdSwing=False), labelspacing=0)
	adjustFigure(fig, 'FullSubthresholdCurves', parameters, saveFigure=saveFigure, showFigure=showFigure)

	return (fig, ax)

def plotFullTransferCurveHistory(deviceHistory, parameters, sweepDirection='both', includeGateCurrent=False, saveFigure=False, showFigure=True):
	# Init Figure
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	fig, ax = initFigure(parameters, 1, 1, 'TransferCurve', testLabel)
	ax.set_title(plot_parameters['TransferCurve']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['TransferCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		elapsedTime = timeToString(deviceHistory[-1]['Results']['timestamps'][0][0] - deviceHistory[0]['Results']['timestamps'][-1][-1])
		
		axisLabel = 'Time'
		if len(deviceHistory) > 1:
			biasTimeSeconds = deviceHistory[1]['Results']['timestamps'][-1][-1] - deviceHistory[0]['Results']['timestamps'][0][0]
			axisLabel = '[$t_{{Hold}}$ = {}]'.format(timeToString(biasTimeSeconds))
		
		colorBar(fig, colorMap['smap'], ticks=[0,0.6,1], tick_labels=[elapsedTime, axisLabel, '$t_0$'], axisLabel='')

	# If first segment of device history is all negative current, flip data
	if((len(deviceHistory) > 0) and (np.mean(deviceHistory[0]['Results']['id_data']) < 0)):
		deviceHistory = scaledData(deviceHistory, 'Results', 'id_data', -1)
		plot_parameters['TransferCurve']['ylabel'] = plot_parameters['TransferCurve']['neg_label']
	
	# Plot
	for i in range(len(deviceHistory)):
		plotTransferCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection, scaleCurrentBy=1e6, lineStyle=None)

	# Add gate current to axis
	if(includeGateCurrent):
		if(len(deviceHistory) == 1):
			gate_colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][2]]
			gate_linestyle = None
		else:	
			gate_colors = colors
			gate_linestyle = '--'
		for i in range(len(deviceHistory)):
			plotGateCurrent(ax, deviceHistory[i], gate_colors[i], direction=sweepDirection, scaleCurrentBy=1e6, lineStyle=gate_linestyle)
		if(plot_parameters['TransferCurve']['ylabel'] == plot_parameters['TransferCurve']['neg_label']):
			plot_parameters['TransferCurve']['ylabel'] = plot_parameters['TransferCurve']['neg_ii_label']
		else:
			plot_parameters['TransferCurve']['ylabel'] = plot_parameters['TransferCurve']['ii_label']
		axisLabels(ax, x_label=plot_parameters['TransferCurve']['xlabel'], y_label=plot_parameters['TransferCurve']['ylabel'])

	# Add Legend and save figure	
	ax.legend([],[], loc='best', title=getLegendTitle(deviceHistory, 'TransferCurve', 'GateSweep', includeVdsRange=True), labelspacing=0)
	adjustFigure(fig, 'FullTransferCurves', parameters, saveFigure=saveFigure, showFigure=showFigure)

	return (fig, ax)

def plotFullGateCurrentHistory(deviceHistory, parameters, sweepDirection='both', saveFigure=False, showFigure=True):
	# Init Figure
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	fig, ax = initFigure(parameters, 1, 1, 'GateCurrent', testLabel)
	ax.set_title(plot_parameters['GateCurrent']['titles'][0])
	if(len(deviceHistory) <= 0):
		return

	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['GateCurrent']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	else:
		elapsedTime = timeToString(deviceHistory[-1]['Results']['timestamps'][0][0] - deviceHistory[0]['Results']['timestamps'][-1][-1])
		colorBar(fig, colorMap['smap'], tick_labels=[elapsedTime, 'Start'])

	# Plot
	for i in range(len(deviceHistory)):
		plotGateCurrent(ax, deviceHistory[i], colors[i], direction=sweepDirection, scaleCurrentBy=1, lineStyle=None)
	
	# Add Legend and save figure
	ax.legend([],[], loc='best', title=getLegendTitle(deviceHistory, 'GateCurrent', 'GateSweep', includeVdsRange=True), labelspacing=0)
	adjustFigure(fig, 'FullGateCurrents', parameters, saveFigure=saveFigure, showFigure=showFigure)

	return (fig, ax)

def plotFullBurnOutHistory(deviceHistory, parameters, saveFigure=False, showFigure=True):
	# Init Figure	
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	fig, (ax1, ax2) = initFigure(parameters, 1, 2, 'BurnOut', testLabel)
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
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i], lineStyle=None)

	# Add Legend and save figure
	ax3.legend([],[], loc='lower right', title=plot_parameters['BurnOut']['legend_title'], labelspacing=0)
	adjustFigure(fig, 'FullBurnOut', parameters, saveFigure=saveFigure, showFigure=showFigure, subplotWidthPad=0.25, subplotHeightPad=0.8)

	return (fig, (ax1, ax2, ax3))

def plotFullStaticBiasHistory(deviceHistory, parameters, timescale='', plotInRealTime=True, includeDualAxis=True, saveFigure=False, showFigure=True):
	if len(deviceHistory) < 1:
		return
	
	vds_setpoint_values = [record['StaticBias']['drainVoltageSetPoint'] for record in deviceHistory]
	vgs_setpoint_values = [record['StaticBias']['gateVoltageSetPoint'] for record in deviceHistory]
	
	vds_setpoint_changes = min(vds_setpoint_values) != max(vds_setpoint_values)
	vgs_setpoint_changes = min(vgs_setpoint_values) != max(vgs_setpoint_values)
	
	if not (vds_setpoint_changes or vgs_setpoint_changes):
		includeDualAxis = False
	
	# Init Figure
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	if(includeDualAxis):
		fig, (ax1, ax2) = initFigure(parameters, 2, 1, 'StaticBias', testLabel, shareX=True)
		ax = ax1
		ax3 = None
		
		if vds_setpoint_changes and vgs_setpoint_changes:
			ax3 = ax2.twinx()
			vds_ax = ax2
			vgs_ax = ax3
		elif vds_setpoint_changes:
			vds_ax = ax2
		else:
			vgs_ax = ax2
	else:
		fig, ax = initFigure(parameters, 1, 1, 'StaticBias', testLabel)
		ax2 = None
		ax3 = None
	ax.set_title(plot_parameters['StaticBias']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# Build Color Map
	colors = colorsFromMap(plot_parameters['StaticBias']['colorMap'], 0, 0.87, len(deviceHistory))['colors']
	
	# If timescale is unspecified, choose an appropriate one based on the data range
	if(timescale == '' and (len(deviceHistory) > 0)):
		timerange = deviceHistory[-1]['Results']['timestamps'][-1] - deviceHistory[0]['Results']['timestamps'][0]
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
	deviceHistory = scaledData(deviceHistory, 'Results', 'timestamps', 1/secondsPer(timescale))
	
	# If first segment of device history is all negative current, flip data
	if((len(deviceHistory) > 0) and (np.mean(deviceHistory[0]['Results']['id_data']) < 0)):
		deviceHistory = scaledData(deviceHistory, 'Results', 'id_data', -1)
		plot_parameters['StaticBias']['ylabel'] = '$-I_{D}$ [$\mu$A]'
	
	time_offset = 0
	dotted_lines = []
	parameter_labels = {'drainVoltageSetPoint':[],'gateVoltageSetPoint':[]}
	for i in range(len(deviceHistory)):
		# Plot
		if(plotInRealTime):
			time_offset = (deviceHistory[i]['Results']['timestamps'][0] - deviceHistory[0]['Results']['timestamps'][0])
		else:
			time_offset = (0) if(i == 0) else (time_offset + (deviceHistory[i-1]['Results']['timestamps'][-1] - deviceHistory[i-1]['Results']['timestamps'][0]))
		
		plotStaticBias(ax, deviceHistory[i], colors[i], time_offset, timescale=timescale, includeLabel=False, lineStyle=None)
		if(includeDualAxis):
			if vds_setpoint_changes:
				vds_line = plotOverTime(vds_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['StaticBias']['drainVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][0], offset=time_offset)
			if vgs_setpoint_changes:
				vgs_line = plotOverTime(vgs_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['StaticBias']['gateVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=time_offset)
				
		# Compare current plot's parameters to the next ones, and save any differences
		#if('drainVoltageSetPoint' in deviceHistory[i] and 'drainVoltageSetPoint' in deviceHistory[i-1]):
		#	# backwards compatibility for old parameters format
		#	if (i == 0) or deviceHistory[i]['drainVoltageSetPoint'] != deviceHistory[i-1]['drainVoltageSetPoint']:
		#		dotted_lines.append({'x':time_offset})
		#		parameter_labels['drainVoltageSetPoint'].append({'x':time_offset, 'drainVoltageSetPoint':deviceHistory[i]['drainVoltageSetPoint']})
		#		parameter_labels['gateVoltageSetPoint'].append({'x':time_offset, 'gateVoltageSetPoint':deviceHistory[i]['gateVoltageSetPoint']})
		#else:
		if((i == 0) or (deviceHistory[i]['StaticBias'] != deviceHistory[i-1]['StaticBias']) or autoStaticBiasSegmentDividers):
			dotted_lines.append({'x':time_offset})
			for key in set(deviceHistory[i]['StaticBias'].keys()).intersection(deviceHistory[i-1]['StaticBias'].keys()):
				if((i == 0) or deviceHistory[i]['StaticBias'][key] != deviceHistory[i-1]['StaticBias'][key]):
					if(key not in parameter_labels):
						parameter_labels[key] = []
					parameter_labels[key].append({'x':time_offset, key:deviceHistory[i]['StaticBias'][key]})
	
	
	# Increase height of the plot to give more room for labels
	if (len(dotted_lines) > 1) or autoStaticBiasSegmentDividers:
		# Draw dotted lines between ANY plots that have different parameters
		for i in range(len(dotted_lines)):
			ax.annotate('', xy=(dotted_lines[i]['x'], ax.get_ylim()[0]), xytext=(dotted_lines[i]['x'], ax.get_ylim()[1]), xycoords='data', arrowprops=dict(arrowstyle='-', color=(0,0,0,0.3), ls=':', lw=0.5))
		
		if not includeDualAxis:
			if (len(parameter_labels['drainVoltageSetPoint']) > 1) or (len(parameter_labels['gateVoltageSetPoint']) > 1):
				# Make the data take up less of the vertical space to make room for the labels
				x0, x1, y0, y1 = ax.axis()
				ax.axis((x0,x1,y0,1.2*y1))
				
				# Add V_DS annotation
				for i in range(len(parameter_labels['drainVoltageSetPoint'])):
					ax.annotate(' $V_{DS} = $'+'{:.1f}V'.format(parameter_labels['drainVoltageSetPoint'][i]['drainVoltageSetPoint']), xy=(parameter_labels['drainVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.99 - 0*0.03*i)), xycoords='data', ha='left', va='top', rotation=-90)

				# Add V_GS annotation
				for i in range(len(parameter_labels['gateVoltageSetPoint'])):
					ax.annotate(' $V_{GS} = $'+'{:.0f}V'.format(parameter_labels['gateVoltageSetPoint'][i]['gateVoltageSetPoint']), xy=(parameter_labels['gateVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.09 - 0*0.03*i)), xycoords='data', ha='left', va='bottom', rotation=-90)
	
	totalBiasTimeKey = 'totalBiasTime'
	if deviceHistory[0]['ParametersFormatVersion'] < 2:
		totalBiasTimeKey = 'biasTime'
	
	biasTimes = [history['StaticBias'][totalBiasTimeKey] for history in deviceHistory]
	biasTimeSeconds = np.mean(biasTimes)
	
	legend_title = ''
	if not vds_setpoint_changes:	
		legend_title += '$V_{DS}^{{Hold}}$ = ' + '{:.2f}V'.format(vds_setpoint_values[0])
	if not vgs_setpoint_changes:
		if len(legend_title) > 0:
			legend_title += '\n'
		legend_title += '$V_{GS}^{{Hold}}$ = ' + '{:.1f}V'.format(vgs_setpoint_values[0])
	if min(biasTimes) == max(biasTimes):
		if len(legend_title) > 0:
			legend_title += '\n'
		legend_title += '$t_{{Hold}}$ = {}'.format(timeToString(biasTimeSeconds))
	
	if len(legend_title) > 0:
		ax.legend([],[], loc='best', title=legend_title, labelspacing=0)
	
	# Add Grounding annotation
	# for i in range(len(parameter_labels['groundDrainWhenDone'])):
	# 	ax.annotate(' Grounded Drain: {:}'.format(parameter_labels['groundDrainWhenDone'][i]['groundDrainWhenDone']), xy=(parameter_labels['groundDrainWhenDone'][i]['x'], ax.get_ylim()[1]*(0.94 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')
	# for i in range(len(parameter_labels['groundGateWhenDone'])):
	# 	ax.annotate(' Grounded Gate: {:}'.format(parameter_labels['groundGateWhenDone'][i]['groundGateWhenDone']), xy=(parameter_labels['groundGateWhenDone'][i]['x'], ax.get_ylim()[1]*(0.92 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')
	
	# Add legend and axis labels and save figure
	if(includeDualAxis):
		# Axis labels
		ax1.set_ylabel(plot_parameters['StaticBias']['ylabel'])
		ax2.set_xlabel(plot_parameters['StaticBias']['xlabel'].format(timescale))
		if vds_setpoint_changes:
			includeOriginOnYaxis(vds_ax)
			vds_ax.set_ylabel(plot_parameters['StaticBias']['vds_label'])
			setLabel(vds_line, '$V_{DS}^{{Hold}}$')
			if vds_setpoint_changes and vgs_setpoint_changes:
				vds_ax.legend(loc='best', borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
		if vgs_setpoint_changes:
			includeOriginOnYaxis(vgs_ax)
			vgs_ax.set_ylabel(plot_parameters['StaticBias']['vgs_label'])
			setLabel(vgs_line, '$V_{GS}^{{Hold}}$')
			if vds_setpoint_changes and vgs_setpoint_changes:
				vgs_ax.legend(loc='best', borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
		
		# Legend
		# lines1, labels1 = ax2.get_legend_handles_labels()
		# lines2, labels2 = ax3.get_legend_handles_labels()
		# ax2.legend(lines1 + lines2, labels1 + labels2, loc='best', ncol=2, borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1, columnspacing=0.1)
		
		fig.align_labels()
		
		# Adjust tick alignment
		[tick.set_verticalalignment('top') for tick in ax2.yaxis.get_majorticklabels()]
		adjustFigure(fig, 'FullStaticBias', parameters, saveFigure=saveFigure, showFigure=showFigure, subplotHeightPad=plot_parameters['StaticBias']['subplot_spacing'])
	else:
		axisLabels(ax, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])
		adjustFigure(fig, 'FullStaticBias', parameters, saveFigure=saveFigure, showFigure=showFigure)

	return (fig, (ax, ax2, ax3))

def plotOnAndOffCurrentHistory(deviceHistory, parameters, timescale='', plotInRealTime=True, saveFigure=False, showFigure=True, includeDualAxis=True):
	if len(deviceHistory) < 1:
		return
	return
	print(deviceHistory[0])
	
	vds_setpoint_values = [record['StaticBias']['drainVoltageSetPoint'] for record in deviceHistory]
	vgs_setpoint_values = [record['StaticBias']['gateVoltageSetPoint'] for record in deviceHistory]
	
	vds_setpoint_changes = min(vds_setpoint_values) != max(vds_setpoint_values)
	vgs_setpoint_changes = min(vgs_setpoint_values) != max(vgs_setpoint_values)
	
	if not (vds_setpoint_changes or vgs_setpoint_changes):
		includeDualAxis = False
	
	# Init Figure
	testLabel = getTestLabel(deviceHistory, parameters['waferID'], parameters['chipID'], parameters['deviceID'])
	
	if(includeDualAxis):
		fig, (ax1, ax3) = initFigure(parameters, 2, 1, 'OnCurrent', testLabel, shareX=True)
		ax4 = None

		if vds_setpoint_changes and vgs_setpoint_changes:
			ax4 = ax3.twinx()
			vds_ax = ax3
			vgs_ax = ax4
		elif vds_setpoint_changes:
			vds_ax = ax3
		else:
			vgs_ax = ax3
	else:
		fig, ax1 = initFigure(parameters, 1, 1, 'OnCurrent', testLabel)
		ax3 = None
		ax4 = None
	
	ax1.set_title(plot_parameters['OnCurrent']['titles'][0])
	if(len(deviceHistory) <= 0):
		return
	
	# If timescale is unspecified, choose an appropriate one based on the data range
	if(timescale == '' and (len(deviceHistory) > 0)):
		timerange = flatten(deviceHistory[-1]['Results']['timestamps'])[-1] - flatten(deviceHistory[0]['Results']['timestamps'])[0]
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
	deviceHistory = scaledData(deviceHistory, 'Results', 'timestamps', 1/secondsPer(timescale))
	
	# Build On/Off Current lists
	onCurrents = []
	offCurrents = []
	timestamps = []
	for deviceRun in deviceHistory:
		onCurrents.append(deviceRun['Results']['onCurrent'])
		offCurrents.append(deviceRun['Results']['offCurrent'])
		timestamps.append(flatten(deviceRun['Results']['timestamps'])[0])
	
	# Plot On Current
	if(plotInRealTime):
		line = plotOverTime(ax1, timestamps, onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=0, markerSize=3, lineWidth=0)
		axisLabels(ax1, x_label=plot_parameters['OnCurrent']['time_label'].format(timescale), y_label=plot_parameters['OnCurrent']['ylabel'])
	else:
		line = scatter(ax1, range(len(onCurrents)), onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], markerSize=3, lineWidth=0, lineStyle=None)
		axisLabels(ax1, x_label=plot_parameters['OnCurrent']['index_label'].format(timescale), y_label=plot_parameters['OnCurrent']['ylabel'])
	setLabel(line, 'On-Currents')
	ax1.set_ylim(bottom=0)
	
	# Plot Off Current
	if plotOffCurrent:
		ax2 = ax1.twinx()
		if(plotInRealTime):
			line = plotOverTime(ax2, timestamps, offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], offset=0, markerSize=2, lineWidth=0)
		else:
			line = scatter(ax2, range(len(offCurrents)), offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], markerSize=2, lineWidth=0, lineStyle=None)
		setLabel(line, 'Off-Currents')
		ax2.set_ylabel(plot_parameters['OnCurrent']['ylabel_dual_axis'])
	
	if includeDualAxis:
		if vds_setpoint_changes:
			vds_line = plotOverTime(vds_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['StaticBias']['drainVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][0], offset=time_offset)
		if vgs_setpoint_changes:
			vgs_line = plotOverTime(vgs_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['StaticBias']['gateVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=time_offset)
		
	
	# Add Legend and save figure
	lines1, labels1 = ax1.get_legend_handles_labels()
	lines2, labels2 = [],[]
	legendax = ax1
	if plotOffCurrent:
		lines2, labels2 = ax2.get_legend_handles_labels()
		legendax = ax2
	
	legendax.legend(lines1 + lines2, labels1 + labels2, loc='lower left')
	adjustFigure(fig, 'OnAndOffCurrents', parameters, saveFigure=saveFigure, showFigure=showFigure)

	return (fig, (ax1, ax2, ax3, ax4))

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory, parameters):
	# Init Figure
	fig, ax = initFigure(parameters, 1, 1, 'ChipHistory', '')
	ax.set_title(plot_parameters['ChipHistory']['titles'][0])

	# Build On/Off Ratio lists
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['Results']['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['Results']['onOffRatio'])

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	# Plot First Run
	line = scatter(ax, range(len(devices)), firstOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], markerSize=6, lineWidth=0, lineStyle=None)
	setLabel(line, 'First Run')
	
	# Plot Most Recent Run
	line = scatter(ax, range(len(devices)), lastOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][0], markerSize=4, lineWidth=0, lineStyle=None)
	setLabel(line, 'Most Recent Run')

	# Label axes
	axisLabels(ax, x_label=plot_parameters['ChipHistory']['xlabel'], y_label=plot_parameters['ChipHistory']['ylabel'])
	tickLabels(ax, devices, rotation=90)
	
	# Add Legend and save figure
	ax.legend(loc='best')
	adjustFigure(fig, 'ChipHistory', parameters, saveFigure=False, showFigure=True)

	return (fig, ax)

def show():
	plt.show()



# ***** Device Plots *****
def plotGateSweepCurrent(axis, jsonData, lineColor, direction='both', currentSource='drain', logScale=True, scaleCurrentBy=1, lineStyle=None):
	if(currentSource == 'gate'):
		currentData = 'ig_data'
	elif(currentSource == 'drain'):
		currentData = 'id_data'
	
	x = jsonData['Results']['gateVoltages']
	y = jsonData['Results'][currentData]

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
		x = x[0]
		y = y[0]
	elif(direction == 'reverse'):
		x = x[1]
		y = y[1]
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
		line = scatter(axis, x, y, lineColor, markerSize=2, lineWidth=1, lineStyle=lineStyle)

	return line

def plotSubthresholdCurve(axis, jsonData, lineColor, direction='both', fitSubthresholdSwing=False, includeLabel=False, lineStyle=None):
	line = plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=True, scaleCurrentBy=1, lineStyle=lineStyle)
	axisLabels(axis, x_label=plot_parameters['SubthresholdCurve']['xlabel'], y_label=plot_parameters['SubthresholdCurve']['ylabel'])
	if(includeLabel): 
		#setLabel(line, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['Results']['onOffRatio'])))
		setLabel(line, 'max $|I_{g}|$'+': {:.2e}'.format(max(abs(np.array(flatten(jsonData['Results']['ig_data']))))))
	if(fitSubthresholdSwing):
		startIndex, endIndex = steepestRegion(np.log10(np.abs(jsonData['Results']['id_data'][0])), 10)
		vgs_region = jsonData['Results']['vgs_data'][0][startIndex:endIndex]
		id_region = jsonData['Results']['id_data'][0][startIndex:endIndex]
		fitted_region = semilogFit(vgs_region, id_region)['fitted_data']
		print(avgSubthresholdSwing(vgs_region, fitted_region))
		plot(axis, vgs_region, fitted_region, lineColor='b', lineStyle='--')

def plotTransferCurve(axis, jsonData, lineColor, direction='both', scaleCurrentBy=1, lineStyle=None):
	plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=False, scaleCurrentBy=scaleCurrentBy, lineStyle=lineStyle)
	axisLabels(axis, x_label=plot_parameters['TransferCurve']['xlabel'], y_label=plot_parameters['TransferCurve']['ylabel'])

def plotGateCurrent(axis, jsonData, lineColor, direction='both', scaleCurrentBy=1, lineStyle=None):
	plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='gate', logScale=False, scaleCurrentBy=scaleCurrentBy, lineStyle=lineStyle)
	axisLabels(axis, x_label=plot_parameters['GateCurrent']['xlabel'], y_label=plot_parameters['GateCurrent']['ylabel'])

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor, lineStyle=None):
	plot(axis1, jsonData['Results']['vds_data'], (np.array(jsonData['Results']['id_data'])*10**6), lineColor=lineColor, lineStyle=lineStyle)
	axisLabels(axis1, x_label=plot_parameters['BurnOut']['vds_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	# Add burn threshold annotation
	currentThreshold = np.percentile(np.array(jsonData['Results']['id_data']), 90) * jsonData['BurnOut']['thresholdProportion'] * 10**6
	axis1.plot([0, jsonData['Results']['vds_data'][-1]], [currentThreshold, currentThreshold], color=lineColor, linestyle='--', linewidth=1)
	axis1.annotate(plot_parameters['BurnOut']['id_annotation'], xy=(0, currentThreshold), xycoords='data', horizontalalignment='left', verticalalignment='bottom', color=lineColor)
	
	plotOverTime(axis2, jsonData['Results']['timestamps'], (np.array(jsonData['Results']['id_data'])*10**6), lineColor)	
	axisLabels(axis2, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	plotOverTime(axis3, jsonData['Results']['timestamps'], jsonData['Results']['vds_data'], lineColor)
	axisLabels(axis3, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['vds_label'])

def plotStaticBias(axis, jsonData, lineColor, timeOffset, timescale='seconds', includeLabel=True, lineStyle=None):
	plotOverTime(axis, jsonData['Results']['timestamps'], (np.array(jsonData['Results']['id_data'])*(10**6)), lineColor, offset=timeOffset, plotInnerGradient=plotGradient)	
	if(includeLabel):
		axisLabels(axis, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])




# ***** Figures *****

def initFigure(parameters, rows, columns, type, testLabel, shareX=False):
	if parameters['DeviceHistory']['figureSizeOverride'] != None:
		plot_parameters[type]['figsize'] = parameters['DeviceHistory']['figureSizeOverride']
	
	if(rows > 1 or columns > 1):
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[type]['figsize'], sharex=shareX, gridspec_kw={'width_ratios':plot_parameters[type]['subplot_width_ratio'], 'height_ratios':plot_parameters[type]['subplot_height_ratio']})
	else:
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[type]['figsize'])
	if(not publication_mode):
		fig.suptitle(testLabel)
	return fig, axes

def adjustFigure(figure, saveName, parameters, saveFigure, showFigure, subplotWidthPad=0, subplotHeightPad=0):
	# figure.set_size_inches(2.2,1.6) # Static Bias
	# figure.set_size_inches(1.4,1.6) # Subthreshold Curve
	# figure.set_size_inches(2.2,1.7) # On/Off-Current
	figure.tight_layout()
	plt.subplots_adjust(wspace=subplotWidthPad, hspace=subplotHeightPad)
	pngDPI = (300) if(publication_mode) else (default_png_dpi)
	if(saveFigure):
		plt.savefig(parameters['plotsFolder'] + saveName + '.png', transparent=True, dpi=pngDPI)
		# plt.savefig(parameters['plotsFolder'] + saveName + '.pdf', transparent=True)
		# plt.savefig(parameters['plotsFolder'] + saveName + '.eps', transparent=True)
	if(not showFigure):
		plt.close(figure)

def colorsFromMap(mapName, colorStartPoint, colorEndPoint, numberOfColors):
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=mapName)
	return {'colors':[scalarColorMap.to_rgba(i) for i in np.linspace(colorStartPoint, colorEndPoint, numberOfColors)], 'smap':scalarColorMap}

def getTestLabel(deviceHistory, waferID, chipID, deviceID):
	label = str(waferID) + str(chipID) + ':' + deviceID
	if len(deviceHistory) > 0:
		test1Num = deviceHistory[0]['experimentNumber']
		test2Num = deviceHistory[-1]['experimentNumber']
		if test1Num == test2Num:
			label += ', Test {:}'.format(test1Num)
		else:
			label += ', Tests {:}-{:}'.format(test1Num, test2Num)
	return label



# ***** Plots ***** 

def plot(axis, x, y, lineColor, lineStyle=None):
	return axis.plot(x, y, color=lineColor, linestyle=lineStyle)[0]

def scatter(axis, x, y, lineColor, markerSize=3, lineWidth=0, lineStyle=None):
	return axis.plot(x, y, color=lineColor, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=lineWidth, linestyle=lineStyle)[0]

def plotWithErrorBars(axis, x, y, lineColor):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	if not errorBarsOn:
		std = None
	return axis.errorbar(x_unique, avg, yerr=std, color=lineColor, capsize=2, capthick=0.5, elinewidth=0.5)[0]

def plotOverTime(axis, timestamps, y, lineColor, offset=0, markerSize=1, lineWidth=1, lineStyle=None, plotInnerGradient=False):
	zeroed_timestamps = list( np.array(timestamps) - timestamps[0] + offset )
	if not plotInnerGradient:
		return axis.plot(zeroed_timestamps, y, color=lineColor, marker='o', markersize=markerSize, linewidth=lineWidth, linestyle=lineStyle)[0]
	else:
		colors = colorsFromMap(plot_parameters['StaticBias']['colorMap'], 0, 0.95, len(y))['colors']
		N = len(y)//20
		if N < 1:
			N = 1
		for i in range(0, len(y)-1, N):
			p = axis.plot(zeroed_timestamps[i:i+1+N], y[i:i+1+N], color=colors[i])
		return p[0]

def colorBar(fig, scalarMappableColorMap, ticks=[0,1], tick_labels=['End','Start'], axisLabel='Time'):
	scalarMappableColorMap._A = []
	cbar = fig.colorbar(scalarMappableColorMap, pad=0.02, aspect=50)
	cbar.set_ticks(ticks)
	cbar.ax.set_yticklabels(tick_labels, rotation=270)
	cbar.ax.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
	cbar.ax.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
	if len(ticks) > 2:
		for i in range(len(ticks) - 2):
			cbar.ax.yaxis.get_majorticklabels()[i+1].set_verticalalignment('center')
	cbar.set_label(axisLabel, rotation=270, labelpad=0.9)



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



# ***** Legend *****

def getLegendTitle(deviceHistory, plotType, parameterType, includeVdsRange, includeSubthresholdSwing=False):
	legend_title = ''
	legend_entries = []
	if(includeVdsRange):
		vds_list = getParameterArray(deviceHistory, parameterType, 'drainVoltageSetPoint')
		vds_min = min(vds_list)
		vds_max = max(vds_list)
		legend_entries.append(plot_parameters[plotType]['leg_vds_label'].format(vds_min) if(vds_min == vds_max) else (plot_parameters[plotType]['leg_vds_range_label'].format(vds_min, vds_max)))
	if(includeSubthresholdSwing):
		SS_list = []
		for deviceRun in deviceHistory:
			startIndex, endIndex = steepestRegion(np.log10(np.abs(deviceRun['Results']['id_data'][0])), 10)
			vgs_region = deviceRun['Results']['vgs_data'][0][startIndex:endIndex]
			id_region = deviceRun['Results']['id_data'][0][startIndex:endIndex]
			fitted_region = semilogFit(vgs_region, id_region)['fitted_data']
			SS_list.append(avgSubthresholdSwing(vgs_region, fitted_region))
			#plot(axis, vgs_region, fitted_region, lineColor='b', lineStyle='--')
		SS_avg = np.mean(SS_list)
		legend_entries.append('$SS_{{avg}} = $ {:.0f}mV/dec'.format(SS_avg))
	
	# if len(deviceHistory) > 1:
	# 	if 'StaticBias' in deviceHistory[0].keys():
	# 		totalBiasTimeKey = 'totalBiasTime'
	# 		if 'biasTime' in deviceHistory[0]['StaticBias'].keys():
	# 			totalBiasTimeKey = 'biasTime'
			
	# 		biasTimes = [history['StaticBias'][totalBiasTimeKey] for history in deviceHistory]
	# 		biasTimeSeconds = np.mean(biasTimes)
	# 	else:
	# 		biasTimeSeconds = deviceHistory[1]['Results']['timestamps'][-1][-1] - deviceHistory[0]['Results']['timestamps'][0][0]
		
	# 	legend_entries.append('$t_{{Hold}}$ = {}'.format(timeToString(biasTimeSeconds)))
	
	for i in range(len(legend_entries)):
		if(i != 0):
			legend_title += '\n'
		legend_title += legend_entries[i]

	return legend_title



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
	return (abs( vgs_data[0] - vgs_data[-1] / (np.log10(np.abs(id_data[0])) - np.log10(np.abs(id_data[-1]))) ) * 1000)



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



# ***** Data Manipulation *****

def flatten(dataList):
	data = list([dataList])
	while(isinstance(data[0], list)):
		data = [(item) for sublist in data for item in sublist]
	return data

def scaledData(deviceHistory, dataSubdirectory, dataToScale, scalefactor):
	data = list(deviceHistory)
	for i in range(len(data)):
		data_entry = data[i][dataSubdirectory][dataToScale]
		if(isinstance(data_entry[0], list)):
			for j in range(len(data_entry)):
				data_entry[j] = list(np.array(data_entry[j])*scalefactor)
		else:
			data_entry = list(np.array(data_entry)*scalefactor)
		data[i][dataSubdirectory][dataToScale] = data_entry
	return data

def getParameterArray(deviceHistory, parameterType, parameterName):
	result = []
	for i in range(len(deviceHistory)):
		if(parameterType != ''):
			result.append(deviceHistory[i][parameterType][parameterName])
		else:
			result.append(deviceHistory[i][parameterName])
	return result



