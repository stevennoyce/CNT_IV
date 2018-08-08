import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

import io
import os

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



# === Plot Parameters ===
default_mode_parameters = {
	'showFigures': True,
	'saveFigures': True,
	'plotSaveFolder': 'CurrentPlots/',
	'plotSaveName': '',
	'publication_mode': False,
	'default_png_dpi': 300,
	'figureSizeOverride': None,
	'legendLoc': 'best',
	'legendLabels': [],
	'enableErrorBars': True,
	'enableColorBar': True,
	'enableGradient': False,
	'staticBiasSegmentDividers': False,
	'staticBiasChangeDividers': True,
	'plotOffCurrent': True
}

plot_parameters = {
	'SubthresholdCurve': {
		'figsize':(2.8,3.2),#(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{{GS}}^{{Sweep}}$ [V]',
		'ylabel':'$I_{{D}}$ [A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}}$\n  = {:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'TransferCurve':{
		'figsize':(2.8,3.2),#(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{{GS}}^{{Sweep}}$ [V]',
		'ylabel':'$I_{{D}}$ [$\\mu$A]',
		'neg_label':'$-I_{{D}}$ [$\\mu$A]',
		'ii_label':'$I_{{D}}$, $I_{{G}}$ [$\\mu$A]',
		'neg_ii_label':'$-I_{{D}}$, $I_{{G}}$ [$\\mu$A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}}$\n  = {:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'GateCurrent':{
		'figsize':(2.8,3.2),#(2*1.4,2*1.6),#(4.2,4.9),
		'colorMap':'hot',
		'xlabel':'$V_{{GS}}^{{Sweep}}$ [V]',
		'ylabel':'$I_{{G}}$ [A]',
		'leg_vds_label':'$V_{{DS}}^{{Sweep}} = ${:}V',
		'leg_vds_range_label':'$V_{{DS}}^{{min}} = $ {:}V\n'+'$V_{{DS}}^{{max}} = $ {:}V'
	},
	'BurnOut':{
		'figsize':(8,4.5),
		'subplot_height_ratio':[1],
		'subplot_width_ratio':[1,1],
		'colorMap':'hot',
		'vds_label':'$V_{{DS}}$ [V]',
		'id_micro_label':'$I_{{D}}$ [$\\mu$A]',
		'time_label':'Time [sec]',
		'id_annotation':'burn current',
		'legend_title':'$V_{{GS}}$ = {:}V'
	},
	'StaticBias':{
		'figsize':(4.4,3.2),#(2*2.2,2*1.6),#(5,4),
		'colorMap':'plasma',
		'xlabel':'Time [{:}]',
		'ylabel':'$I_{{D}}$ [$\\mu$A]',
		'vds_label': '$V_{{DS}}^{{Hold}}$ [V]',
		'vgs_label': '$V_{{GS}}^{{Hold}}$ [V]',
		'subplot_height_ratio':[3,1],
		'subplot_width_ratio': [1],
		'subplot_spacing': 0.03
	},
	'OnCurrent':{
		'figsize':(4.4,3.4),#(2*2.2,2*1.7),#(5,4),
		'time_label':'Time [{:}]',
		'index_label':'Time Index of Gate Sweep [#]',
		'ylabel':'On-Current [A]',
		'ylabel_dual_axis':'Off-Current [A]',
		'vds_label': '$V_{{DS}}^{{Hold}}$ [V]',
		'vgs_label': '$V_{{GS}}^{{Hold}}$ [V]',
		'subplot_height_ratio':[3,1],
		'subplot_width_ratio': [1],
		'subplot_spacing': 0.03
	},
	'ChipHistogram':{
		'figsize':(5,4),
		'xlabel':'Device',
		'ylabel':'Experiments'
	},
	'ChipOnOffRatios':{
		'figsize':(5,4),
		'xlabel':'Device',
		'ylabel':'On/Off Ratio, (Order of Mag)'
	},
	'ChipOnOffCurrents':{
		'figsize':(5,4),
		'xlabel':'Device',
		'ylabel':'$I_{{ON}}$ [$\\mu$A]',
		'ylabel_dual_axis':'$I_{{OFF}}$ [$\\mu$A]'
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



# === API ===
def plotFullSubthresholdCurveHistory(deviceHistory, identifiers, sweepDirection='both', mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No subthreshold curve history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'SubthresholdCurve', figsizeOverride=mode_parameters['figureSizeOverride'])
	if(not mode_parameters['publication_mode']):
		ax.set_title(getTestLabel(deviceHistory, identifiers))
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['SubthresholdCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	elif(len(deviceHistory) == 2):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1], plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	elif(mode_parameters['enableColorBar']):
		elapsedTime = timeToString(deviceHistory[-1]['Results']['timestamps'][0][0] - deviceHistory[0]['Results']['timestamps'][-1][-1])
		
		axisLabel = 'Time'
		if len(deviceHistory) > 1:
			biasTimeSeconds = deviceHistory[1]['Results']['timestamps'][-1][-1] - deviceHistory[0]['Results']['timestamps'][0][0]
			axisLabel = '[$t_{{Hold}}$ = {}]'.format(timeToString(biasTimeSeconds))
		
		colorBar(fig, colorMap['smap'], ticks=[0,0.6,1], tick_labels=[elapsedTime, axisLabel, '$t_0$'], axisLabel='')
	
	# Plot
	for i in range(len(deviceHistory)):
		line = plotSubthresholdCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection, fitSubthresholdSwing=False, includeLabel=False, lineStyle=None, errorBars=mode_parameters['enableErrorBars'])			
		if(len(deviceHistory) == len(mode_parameters['legendLabels'])):
			setLabel(line, mode_parameters['legendLabels'][i])

	ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=10))
	
	# Add Legend and save figure
	lines, labels = ax.get_legend_handles_labels()
	ax.legend(lines, labels, loc=mode_parameters['legendLoc'], title=getLegendTitle(deviceHistory, 'SubthresholdCurve', 'runConfigs', 'GateSweep', includeVdsRange=True, includeSubthresholdSwing=False), labelspacing=(0) if(len(labels) == 0) else (0.3))
	adjustFigure(fig, 'FullSubthresholdCurves', mode_parameters)

	return (fig, ax)

def plotFullTransferCurveHistory(deviceHistory, identifiers, sweepDirection='both', includeGateCurrent=False, mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No transfer curve history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'TransferCurve', figsizeOverride=mode_parameters['figureSizeOverride'])
	if(not mode_parameters['publication_mode']):
		ax.set_title(getTestLabel(deviceHistory, identifiers))
	
	
	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['TransferCurve']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1]]
	elif(len(deviceHistory) == 2):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1], plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	elif(mode_parameters['enableColorBar']):
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
		line = plotTransferCurve(ax, deviceHistory[i], colors[i], direction=sweepDirection, scaleCurrentBy=1e6, lineStyle=None, errorBars=mode_parameters['enableErrorBars'])
		if(len(deviceHistory) == len(mode_parameters['legendLabels'])):
			setLabel(line, mode_parameters['legendLabels'][i])

	# Add gate current to axis
	if(includeGateCurrent):
		if(len(deviceHistory) == 1):
			gate_colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][2]]
			gate_linestyle = None
		else:	
			gate_colors = colors
			gate_linestyle = '--'
		for i in range(len(deviceHistory)):
			plotGateCurrent(ax, deviceHistory[i], gate_colors[i], direction=sweepDirection, scaleCurrentBy=1e6, lineStyle=gate_linestyle, errorBars=mode_parameters['enableErrorBars'])
		if(plot_parameters['TransferCurve']['ylabel'] == plot_parameters['TransferCurve']['neg_label']):
			plot_parameters['TransferCurve']['ylabel'] = plot_parameters['TransferCurve']['neg_ii_label']
		else:
			plot_parameters['TransferCurve']['ylabel'] = plot_parameters['TransferCurve']['ii_label']
		axisLabels(ax, x_label=plot_parameters['TransferCurve']['xlabel'], y_label=plot_parameters['TransferCurve']['ylabel'])

	# Add Legend and save figure	
	lines, labels = ax.get_legend_handles_labels()
	ax.legend(lines, labels, loc=mode_parameters['legendLoc'], title=getLegendTitle(deviceHistory, 'TransferCurve', 'runConfigs', 'GateSweep', includeVdsRange=True), labelspacing=(0) if(len(labels) == 0) else (0.3))
	adjustFigure(fig, 'FullTransferCurves', mode_parameters)

	return (fig, ax)

def plotFullGateCurrentHistory(deviceHistory, identifiers, sweepDirection='both', mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No gate current curve history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'GateCurrent', figsizeOverride=mode_parameters['figureSizeOverride'])
	if(not mode_parameters['publication_mode']):
		ax.set_title(getTestLabel(deviceHistory, identifiers))

	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['GateCurrent']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][2]]
	elif(len(deviceHistory) == 2):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][1], plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	elif(mode_parameters['enableColorBar']):
		elapsedTime = timeToString(deviceHistory[-1]['Results']['timestamps'][0][0] - deviceHistory[0]['Results']['timestamps'][-1][-1])
		colorBar(fig, colorMap['smap'], tick_labels=[elapsedTime, 'Start'])

	# Plot
	for i in range(len(deviceHistory)):
		line = plotGateCurrent(ax, deviceHistory[i], colors[i], direction=sweepDirection, scaleCurrentBy=1, lineStyle=None, errorBars=mode_parameters['enableErrorBars'])
		if(len(deviceHistory) == len(mode_parameters['legendLabels'])):
			setLabel(line, mode_parameters['legendLabels'][i])

	# Add Legend and save figure
	lines, labels = ax.get_legend_handles_labels()
	ax.legend(lines, labels, loc=mode_parameters['legendLoc'], title=getLegendTitle(deviceHistory, 'GateCurrent', 'runConfigs', 'GateSweep', includeVdsRange=True), labelspacing=(0) if(len(labels) == 0) else (0.3))
	adjustFigure(fig, 'FullGateCurrents', mode_parameters)

	return (fig, ax)

def plotFullBurnOutHistory(deviceHistory, identifiers, mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No burn out history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure	
	fig, (ax1, ax2) = initFigure(1, 2, 'BurnOut', figsizeOverride=mode_parameters['figureSizeOverride'])
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(224)
	if(not mode_parameters['publication_mode']):
		ax1.set_title(getTestLabel(deviceHistory, identifiers))

	# Build Color Map and Color Bar
	colorMap = colorsFromMap(plot_parameters['BurnOut']['colorMap'], 0.7, 0, len(deviceHistory))
	colors = colorMap['colors']
	if(len(deviceHistory) == 1):
		colors = [plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]
	elif(mode_parameters['enableColorBar']):
		plt.sca(ax1)
		colorBar(fig, colorMap['smap'])

	# Plot
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i], lineStyle=None)

	# Add Legend and save figure
	ax1.legend([],[], loc=mode_parameters['legendLoc'], title=plot_parameters['BurnOut']['legend_title'].format(np.mean([deviceRun['runConfigs']['BurnOut']['gateVoltageSetPoint'] for deviceRun in deviceHistory])), labelspacing=0)
	ax2.legend([],[], loc=mode_parameters['legendLoc'], title=plot_parameters['BurnOut']['legend_title'].format(np.mean([deviceRun['runConfigs']['BurnOut']['gateVoltageSetPoint'] for deviceRun in deviceHistory])), labelspacing=0)
	ax3.legend([],[], loc=mode_parameters['legendLoc'], title=plot_parameters['BurnOut']['legend_title'].format(np.mean([deviceRun['runConfigs']['BurnOut']['gateVoltageSetPoint'] for deviceRun in deviceHistory])), labelspacing=0)
	adjustFigure(fig, 'FullBurnOut', mode_parameters, subplotWidthPad=0.25, subplotHeightPad=0.8)

	return (fig, (ax1, ax2, ax3))

def plotFullStaticBiasHistory(deviceHistory, identifiers, timescale='', plotInRealTime=True, includeDualAxis=True, mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No static bias history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)
	
	vds_setpoint_values = [jsonData['runConfigs']['StaticBias']['drainVoltageSetPoint'] for jsonData in deviceHistory]
	vgs_setpoint_values = [jsonData['runConfigs']['StaticBias']['gateVoltageSetPoint'] for jsonData in deviceHistory]
	vds_setpoint_changes = min(vds_setpoint_values) != max(vds_setpoint_values)
	vgs_setpoint_changes = min(vgs_setpoint_values) != max(vgs_setpoint_values)
	
	if(not (vds_setpoint_changes or vgs_setpoint_changes)):
		includeDualAxis = False
	
	# Init Figure
	if(includeDualAxis):
		fig, (ax1, ax2) = initFigure(2, 1, 'StaticBias', shareX=True, figsizeOverride=mode_parameters['figureSizeOverride'])
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
		fig, ax = initFigure(1, 1, 'StaticBias', figsizeOverride=mode_parameters['figureSizeOverride'])
		ax2 = None
		ax3 = None
	if(not mode_parameters['publication_mode']):
		ax.set_title(getTestLabel(deviceHistory, identifiers))
	
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
	if((np.mean(deviceHistory[0]['Results']['id_data']) < 0)):
		deviceHistory = scaledData(deviceHistory, 'Results', 'id_data', -1)
		plot_parameters['StaticBias']['ylabel'] = '$-I_{D}$ [$\\mu$A]'
	
	time_offset = 0
	dotted_lines = []
	parameter_labels = {'drainVoltageSetPoint':[],'gateVoltageSetPoint':[]}
	for i in range(len(deviceHistory)):
		# Plot
		if(plotInRealTime):
			t_0 = deviceHistory[0]['Results']['timestamps'][0]
			t_i_start = deviceHistory[i]['Results']['timestamps'][0]
			time_offset = (t_i_start - t_0)
		else:
			t_prev_end = deviceHistory[i-1]['Results']['timestamps'][-1]
			t_prev_start = deviceHistory[i-1]['Results']['timestamps'][0]
			time_offset = (0) if(i == 0) else (time_offset + (t_prev_end - t_prev_start))
		
		line = plotStaticBias(ax, deviceHistory[i], colors[i], time_offset, timescale=timescale, includeLabel=False, lineStyle=None, gradient=mode_parameters['enableGradient'])
		if(len(deviceHistory) == len(mode_parameters['legendLabels'])):
			setLabel(line, mode_parameters['legendLabels'][i])
		#line = plotStaticBias(ax, deviceHistory[i], 'b', time_offset, currentData='ig_data', timescale=timescale, includeLabel=False, lineStyle=None, gradient=mode_parameters['enableGradient'])
			
		if(includeDualAxis):
			if vds_setpoint_changes:
				vds_line = plotOverTime(vds_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['runConfigs']['StaticBias']['drainVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][0], offset=time_offset)
			if vgs_setpoint_changes:
				vgs_line = plotOverTime(vgs_ax, deviceHistory[i]['Results']['timestamps'], [deviceHistory[i]['runConfigs']['StaticBias']['gateVoltageSetPoint']]*len(deviceHistory[i]['Results']['timestamps']), plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=time_offset)
				
		# Compare current plot's parameters to the next ones, and save any differences
		if((i == 0) or (deviceHistory[i]['runConfigs']['StaticBias'] != deviceHistory[i-1]['runConfigs']['StaticBias']) or mode_parameters['staticBiasSegmentDividers']):
			dotted_lines.append({'x':time_offset})
			for key in set(deviceHistory[i]['runConfigs']['StaticBias'].keys()).intersection(deviceHistory[i-1]['runConfigs']['StaticBias'].keys()):
				if((i == 0) or deviceHistory[i]['runConfigs']['StaticBias'][key] != deviceHistory[i-1]['runConfigs']['StaticBias'][key]):
					if(key not in parameter_labels):
						parameter_labels[key] = []
					parameter_labels[key].append({'x':time_offset, key:deviceHistory[i]['runConfigs']['StaticBias'][key]})
	
	
	# Increase height of the plot to give more room for labels
	if(len(dotted_lines) > 1):
		# Draw dotted lines between ANY plots that have different parameters
		if(mode_parameters['staticBiasChangeDividers'] or mode_parameters['staticBiasSegmentDividers']):
			for i in range(len(dotted_lines)):
				ax.annotate('', xy=(dotted_lines[i]['x'], ax.get_ylim()[0]), xytext=(dotted_lines[i]['x'], ax.get_ylim()[1]), xycoords='data', arrowprops=dict(arrowstyle='-', color=(0,0,0,0.3), ls=':', lw=0.5))
			
		if(not includeDualAxis):
			if(len(parameter_labels['drainVoltageSetPoint']) > 1) or (len(parameter_labels['gateVoltageSetPoint']) > 1):
				# Make the data take up less of the vertical space to make room for the labels
				x0, x1, y0, y1 = ax.axis()
				ax.axis((x0,x1,y0,1.2*y1))
				
				# Add V_DS annotation
				for i in range(len(parameter_labels['drainVoltageSetPoint'])):
					ax.annotate(' $V_{DS} = $'+'{:.1f}V'.format(parameter_labels['drainVoltageSetPoint'][i]['drainVoltageSetPoint']), xy=(parameter_labels['drainVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.99 - 0*0.03*i)), xycoords='data', ha='left', va='top', rotation=-90)

				# Add V_GS annotation
				for i in range(len(parameter_labels['gateVoltageSetPoint'])):
					ax.annotate(' $V_{GS} = $'+'{:.0f}V'.format(parameter_labels['gateVoltageSetPoint'][i]['gateVoltageSetPoint']), xy=(parameter_labels['gateVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.09 - 0*0.03*i)), xycoords='data', ha='left', va='bottom', rotation=-90)
	
	biasTimes = [jsonData['runConfigs']['StaticBias']['totalBiasTime'] for jsonData in deviceHistory]
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
		ax.legend([],[], loc=mode_parameters['legendLoc'], title=legend_title, labelspacing=0)
	
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
			vds_ax.set_ylim(bottom=vds_ax.get_ylim()[0] - (vds_ax.get_ylim()[1] - vds_ax.get_ylim()[0])*0.08)
			vds_ax.set_ylim(top=   vds_ax.get_ylim()[1] + (vds_ax.get_ylim()[1] - vds_ax.get_ylim()[0])*0.08)
			vds_ax.set_ylabel(plot_parameters['StaticBias']['vds_label'])
			setLabel(vds_line, '$V_{DS}^{{Hold}}$')
			if vds_setpoint_changes and vgs_setpoint_changes:
				vds_ax.legend(loc=mode_parameters['legendLoc'], borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
		if vgs_setpoint_changes:
			includeOriginOnYaxis(vgs_ax)
			vgs_ax.set_ylabel(plot_parameters['StaticBias']['vgs_label'])
			setLabel(vgs_line, '$V_{GS}^{{Hold}}$')
			if vds_setpoint_changes and vgs_setpoint_changes:
				vgs_ax.legend(loc=mode_parameters['legendLoc'], borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
		
		# Legend
		# lines1, labels1 = ax2.get_legend_handles_labels()
		# lines2, labels2 = ax3.get_legend_handles_labels()
		# ax2.legend(lines1 + lines2, labels1 + labels2, loc=mode_parameters['legendLoc'], ncol=2, borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1, columnspacing=0.1)
		
		fig.align_labels()
		
		# Adjust tick alignment
		[tick.set_verticalalignment('top') for tick in ax2.yaxis.get_majorticklabels()]
		adjustFigure(fig, 'FullStaticBias', mode_parameters, subplotHeightPad=plot_parameters['StaticBias']['subplot_spacing'])
	else:
		axisLabels(ax, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])
		adjustFigure(fig, 'FullStaticBias', mode_parameters)

	return (fig, (ax, ax2, ax3))

def plotOnAndOffCurrentHistory(deviceHistory, identifiers, timescale='', plotInRealTime=True, includeDualAxis=True, mode_params=None):
	if(len(deviceHistory) <= 0):
		print('No on/off current history to plot.')
		return
	
	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)
	
	vds_setpoint_values = [jsonData['runConfigs']['StaticBias']['drainVoltageSetPoint'] for jsonData in deviceHistory]
	vgs_setpoint_values = [jsonData['runConfigs']['StaticBias']['gateVoltageSetPoint'] for jsonData in deviceHistory]
	vds_setpoint_changes = min(vds_setpoint_values) != max(vds_setpoint_values)
	vgs_setpoint_changes = min(vgs_setpoint_values) != max(vgs_setpoint_values)
	
	if(not (vds_setpoint_changes or vgs_setpoint_changes)):
		includeDualAxis = False
	
	# Init Figure
	if(includeDualAxis):
		fig, (ax1, ax3) = initFigure(2, 1, 'OnCurrent', shareX=True, figsizeOverride=mode_parameters['figureSizeOverride'])
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
		fig, ax1 = initFigure(1, 1, 'OnCurrent', figsizeOverride=mode_parameters['figureSizeOverride'])
		ax3 = None
		ax4 = None
	if(not mode_parameters['publication_mode']):
		ax1.set_title(getTestLabel(deviceHistory, identifiers))
	
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
		onCurrents.append(deviceRun['Computed']['onCurrent'])
		offCurrents.append(deviceRun['Computed']['offCurrent'])
		timestamps.append(flatten(deviceRun['Results']['timestamps'])[0])
	
	# Plot On Current
	if(plotInRealTime):
		line = plotOverTime(ax1, timestamps, onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=0, markerSize=3, lineWidth=0)
	else:
		line = scatter(ax1, range(len(onCurrents)), onCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], markerSize=3, lineWidth=0, lineStyle=None)
	setLabel(line, 'On-Currents')
	ax1.set_ylim(bottom=0)
	ax1.set_ylabel(plot_parameters['OnCurrent']['ylabel'])
	
	# Plot Off Current
	if(mode_parameters['plotOffCurrent']):
		ax2 = ax1.twinx()
		if(plotInRealTime):
			line = plotOverTime(ax2, timestamps, offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], offset=0, markerSize=2, lineWidth=0)
		else:
			line = scatter(ax2, range(len(offCurrents)), offCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], markerSize=2, lineWidth=0, lineStyle=None)
		setLabel(line, 'Off-Currents')
		ax2.set_ylabel(plot_parameters['OnCurrent']['ylabel_dual_axis'])
	
	# Plot in Dual Axis
	if(includeDualAxis):
		time_offset = 0
		for i in range(len(deviceHistory)):
			t_0 = timestamps[0]
			t_i = timestamps[i]
			time_offset = (t_i - t_0)
			t_i_next = timestamps[i] + deviceHistory[i]['runConfigs']['StaticBias']['totalBiasTime']/secondsPer(timescale)

			if vds_setpoint_changes:
				vds_line = plotOverTime(vds_ax, [timestamps[i], t_i_next], [deviceHistory[i]['runConfigs']['StaticBias']['drainVoltageSetPoint']]*2, plt.rcParams['axes.prop_cycle'].by_key()['color'][0], offset=time_offset)
			if vgs_setpoint_changes:
				vgs_line = plotOverTime(vgs_ax, [timestamps[i], t_i_next], [deviceHistory[i]['runConfigs']['StaticBias']['gateVoltageSetPoint']]*2, plt.rcParams['axes.prop_cycle'].by_key()['color'][3], offset=time_offset)
	
	# Add Legend
	lines1, labels1 = ax1.get_legend_handles_labels()
	lines2, labels2 = [],[]
	legendax = ax1
	if(mode_parameters['plotOffCurrent']):
		lines2, labels2 = ax2.get_legend_handles_labels()
		legendax = ax2
	legendax.legend(lines1 + lines2, labels1 + labels2, loc=mode_parameters['legendLoc'])

	if(includeDualAxis):
		if(plotInRealTime):
			ax3.set_xlabel(plot_parameters['OnCurrent']['time_label'].format(timescale))
		else:
			ax3.set_xlabel(plot_parameters['OnCurrent']['index_label'])
		if(vds_setpoint_changes):
			vds_ax.set_ylabel(plot_parameters['StaticBias']['vds_label'])
		if(vgs_setpoint_changes):
			vgs_ax.set_ylabel(plot_parameters['StaticBias']['vgs_label'])
		adjustFigure(fig, 'OnAndOffCurrents', mode_parameters, subplotHeightPad=plot_parameters['StaticBias']['subplot_spacing'])
	else:
		if(plotInRealTime):
			ax1.set_xlabel(plot_parameters['OnCurrent']['time_label'].format(timescale))
		else:
			ax1.set_xlabel(plot_parameters['OnCurrent']['index_label'])
		adjustFigure(fig, 'OnAndOffCurrents', mode_parameters)
	
	return (fig, (ax1, ax2, ax3, ax4))

def plotChipHistogram(chipIndexes, mode_params=None):
	if(len(chipIndexes) <= 0):
		print('No chip histogram to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'ChipHistogram', figsizeOverride=mode_parameters['figureSizeOverride'])

	# Build index, experiment lists
	devices = list(chipIndexes.keys())
	deviceExperiments = len(devices)*[0]
	for device, indexData in chipIndexes.items():
		deviceExperiments[devices.index(device)] = indexData['experimentNumber']
	
	deviceExperiments, devices = zip(*(reversed(sorted(zip(deviceExperiments, devices)))))

	# Plot
	ax.bar(devices, deviceExperiments)

	# Label axes
	axisLabels(ax, x_label=plot_parameters['ChipHistogram']['xlabel'], y_label=plot_parameters['ChipHistogram']['ylabel'])
	tickLabels(ax, devices, rotation=90)

	# Save figure
	adjustFigure(fig, 'ChipHistogram', mode_parameters)
	return (fig, ax)


def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory, mode_params=None):
	if(len(firstRunChipHistory) <= 0):
		print('No chip on-off ratio history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'ChipOnOffRatios', figsizeOverride=mode_parameters['figureSizeOverride'])

	# Build On/Off Ratio lists
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['Identifiers']['device']) 
		firstOnOffRatios.append(np.log10(deviceRun['Computed']['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['Identifiers']['device'])] = np.log10(deviceRun['Computed']['onOffRatio'])

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	# Plot
	line = scatter(ax, range(len(devices)), firstOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], markerSize=6, lineWidth=0, lineStyle=None)
	setLabel(line, 'First Run')
	line = scatter(ax, range(len(devices)), lastOnOffRatios, plt.rcParams['axes.prop_cycle'].by_key()['color'][0], markerSize=4, lineWidth=0, lineStyle=None)
	setLabel(line, 'Most Recent Run')

	# Label axes
	axisLabels(ax, x_label=plot_parameters['ChipOnOffRatios']['xlabel'], y_label=plot_parameters['ChipOnOffRatios']['ylabel'])
	tickLabels(ax, devices, rotation=90)
	
	# Add Legend and save figure
	ax.legend(loc=mode_parameters['legendLoc'])
	adjustFigure(fig, 'ChipOnOffRatios', mode_parameters)
	return (fig, ax)
	
def plotChipOnOffCurrents(recentRunChipHistory, mode_params=None):
	if(len(recentRunChipHistory) <= 0):
		print('No chip on-current history to plot.')
		return

	mode_parameters = default_mode_parameters.copy()
	if(mode_params is not None):
		mode_parameters.update(mode_params)

	# Init Figure
	fig, ax = initFigure(1, 1, 'ChipOnOffCurrents', figsizeOverride=mode_parameters['figureSizeOverride'])

	# Build On Current lists
	devices = []
	recentOnCurrents = []
	recentOffCurrents = []
	for deviceRun in recentRunChipHistory:
		devices.append(deviceRun['Identifiers']['device']) 
		recentOnCurrents.append(deviceRun['Computed']['onCurrent'] * 10**6)
		recentOffCurrents.append(deviceRun['Computed']['offCurrent'] * 10**6)

	recentOnCurrents, devices, recentOffCurrents = zip(*(reversed(sorted(zip(recentOnCurrents, devices, recentOffCurrents)))))

	# Plot
	if(mode_parameters['plotOffCurrent']):
		line = scatter(ax, range(len(devices)), recentOffCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][1], markerSize=8, lineWidth=0, lineStyle=None)
		setLabel(line, 'Off Currents')
	line = scatter(ax, range(len(devices)), recentOnCurrents, plt.rcParams['axes.prop_cycle'].by_key()['color'][0], markerSize=4, lineWidth=0, lineStyle=None)
	setLabel(line, 'On Currents')

	# Label axes
	axisLabels(ax, x_label=plot_parameters['ChipOnOffCurrents']['xlabel'], y_label=plot_parameters['ChipOnOffCurrents']['ylabel'])
	tickLabels(ax, devices, rotation=90)
	
	# Add Legend
	ax.legend(loc=mode_parameters['legendLoc'])
	
	# Save Figure
	adjustFigure(fig, 'ChipOnOffCurrents', mode_parameters)
	return (fig, ax)

def show():
	plt.show()



# === Device Plots ===
def plotGateSweepCurrent(axis, jsonData, lineColor, direction='both', currentSource='drain', logScale=True, scaleCurrentBy=1, lineStyle=None, errorBars=True, alphaForwardSweep=1):
	if(currentSource == 'gate'):
		currentData = 'ig_data'
	elif(currentSource == 'drain'):
		currentData = 'id_data'
	
	x = jsonData['Results']['vgs_data']
	y = jsonData['Results'][currentData]

	# Sort data if it was collected in an unordered fashion
	try:
		if(jsonData['runConfigs']['GateSweep']['isAlternatingSweep']):
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
		if(alphaForwardSweep < 1):
			x = x
			y = y
		else:
			x = flatten(x)
			y = flatten(y)

	# Make y-axis a logarithmic scale
	if(logScale):
		y = abs(np.array(y))
		semiLogScale(axis)

	# Scale the data by a given factor
	y = np.array(y)*scaleCurrentBy

	
	if(alphaForwardSweep < 1):
		forward_x = x[0]
		forward_y = y[0]
		reverse_x = x[1]
		reverse_y = y[1]
		if(forward_x[0] == forward_x[1]):
			plotWithErrorBars(axis, forward_x, forward_y, lineColor, errorBars=errorBars, alpha=alphaForwardSweep)
			line = plotWithErrorBars(axis, reverse_x, reverse_y, lineColor, errorBars=errorBars)
		else:
			scatter(axis, forward_x, forward_y, lineColor, markerSize=2, lineWidth=1, lineStyle=lineStyle, alpha=alphaForwardSweep)
			line = scatter(axis, reverse_x, reverse_y, lineColor, markerSize=2, lineWidth=1, lineStyle=lineStyle)
	else:
		# data contains multiple y-values per x-value
		if(x[0] == x[1]):
			line = plotWithErrorBars(axis, x, y, lineColor, errorBars=errorBars)
		else:
			line = scatter(axis, x, y, lineColor, markerSize=2, lineWidth=1, lineStyle=lineStyle)

	return line

def plotSubthresholdCurve(axis, jsonData, lineColor, direction='both', fitSubthresholdSwing=False, includeLabel=False, lineStyle=None, errorBars=True):
	line = plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=True, scaleCurrentBy=1, lineStyle=lineStyle, errorBars=errorBars)
	axisLabels(axis, x_label=plot_parameters['SubthresholdCurve']['xlabel'], y_label=plot_parameters['SubthresholdCurve']['ylabel'])
	if(includeLabel): 
		#setLabel(line, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['Computed']['onOffRatio'])))
		setLabel(line, 'max $|I_{g}|$'+': {:.2e}'.format(jsonData['Computed']['ig_max']))
	if(fitSubthresholdSwing):
		startIndex, endIndex = steepestRegion(np.log10(np.abs(jsonData['Results']['id_data'][0])), 10)
		vgs_region = jsonData['Results']['vgs_data'][0][startIndex:endIndex]
		id_region = jsonData['Results']['id_data'][0][startIndex:endIndex]
		fitted_region = semilogFit(vgs_region, id_region)['fitted_data']
		print(avgSubthresholdSwing(vgs_region, fitted_region))
		plot(axis, vgs_region, fitted_region, lineColor='b', lineStyle='--')
	return line

def plotTransferCurve(axis, jsonData, lineColor, direction='both', scaleCurrentBy=1, lineStyle=None, errorBars=True):
	line = plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='drain', logScale=False, scaleCurrentBy=scaleCurrentBy, lineStyle=lineStyle, errorBars=errorBars)
	axisLabels(axis, x_label=plot_parameters['TransferCurve']['xlabel'], y_label=plot_parameters['TransferCurve']['ylabel'])
	return line

def plotGateCurrent(axis, jsonData, lineColor, direction='both', scaleCurrentBy=1, lineStyle=None, errorBars=True):
	line = plotGateSweepCurrent(axis, jsonData, lineColor, direction, currentSource='gate', logScale=False, scaleCurrentBy=scaleCurrentBy, lineStyle=lineStyle, errorBars=errorBars)
	axisLabels(axis, x_label=plot_parameters['GateCurrent']['xlabel'], y_label=plot_parameters['GateCurrent']['ylabel'])
	return line

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor, lineStyle=None, annotate=False):
	line1 = plot(axis1, jsonData['Results']['vds_data'], (np.array(jsonData['Results']['id_data'])*10**6), lineColor=lineColor, lineStyle=lineStyle)
	axisLabels(axis1, x_label=plot_parameters['BurnOut']['vds_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	# Add burn threshold annotation
	if(annotate):
		currentThreshold = np.percentile(np.array(jsonData['Results']['id_data']), 90) * jsonData['runConfigs']['BurnOut']['thresholdProportion'] * 10**6
		axis1.plot([0, jsonData['Results']['vds_data'][-1]], [currentThreshold, currentThreshold], color=lineColor, linestyle='--', linewidth=1)
		axis1.annotate(plot_parameters['BurnOut']['id_annotation'], xy=(0, currentThreshold), xycoords='data', horizontalalignment='left', verticalalignment='bottom', color=lineColor)
		
	line2 = plotOverTime(axis2, jsonData['Results']['timestamps'], (np.array(jsonData['Results']['id_data'])*10**6), lineColor)	
	axisLabels(axis2, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['id_micro_label'])

	line3 = plotOverTime(axis3, jsonData['Results']['timestamps'], jsonData['Results']['vds_data'], lineColor)
	axisLabels(axis3, x_label=plot_parameters['BurnOut']['time_label'], y_label=plot_parameters['BurnOut']['vds_label'])
	return (line1, line2, line3)

def plotStaticBias(axis, jsonData, lineColor, timeOffset, currentData='id_data', timescale='seconds', includeLabel=True, lineStyle=None, gradient=False):
	line = plotOverTime(axis, jsonData['Results']['timestamps'], (np.array(jsonData['Results'][currentData])*(10**6)), lineColor, offset=timeOffset, plotInnerGradient=gradient)	
	if(includeLabel):
		axisLabels(axis, x_label=plot_parameters['StaticBias']['xlabel'].format(timescale), y_label=plot_parameters['StaticBias']['ylabel'])
	return line



# === Figures ===
def initFigure(rows, columns, plotType, shareX=False, figsizeOverride=None):
	if(figsizeOverride != None):
		plot_parameters[plotType]['figsize'] = figsizeOverride
	if(rows > 1 or columns > 1):
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[plotType]['figsize'], sharex=shareX, gridspec_kw={'width_ratios':plot_parameters[plotType]['subplot_width_ratio'], 'height_ratios':plot_parameters[plotType]['subplot_height_ratio']})
	else:
		fig, axes = plt.subplots(rows, columns, figsize=plot_parameters[plotType]['figsize'])
	return fig, axes

def adjustFigure(figure, plotType, mode_parameters, subplotWidthPad=0, subplotHeightPad=0):
	# figure.set_size_inches(2.2,1.6) # Static Bias
	# figure.set_size_inches(1.4,1.6) # Subthreshold Curve
	# figure.set_size_inches(2.2,1.7) # On/Off-Current	
	figure.tight_layout()
	plt.subplots_adjust(wspace=subplotWidthPad, hspace=subplotHeightPad)
	pngDPI = (300) if(mode_parameters['publication_mode']) else (mode_parameters['default_png_dpi'])
	if(mode_parameters['saveFigures']):
		if isinstance(mode_parameters['plotSaveName'], io.BytesIO):
			plt.savefig(mode_parameters['plotSaveName'], transparent=True, dpi=pngDPI, format='png')
		else:
			plt.savefig(os.path.join(mode_parameters['plotSaveFolder'], mode_parameters['plotSaveName'] + plotType + '.png'), transparent=True, dpi=pngDPI)
			# plt.savefig(os.path.join(mode_parameters['plotSaveFolder'], mode_parameters['plotSaveName'] + plotType + '.pdf'), transparent=True, dpi=pngDPI)
			# plt.savefig(os.path.join(mode_parameters['plotSaveFolder'], mode_parameters['plotSaveName'] + plotType + '.eps'), transparent=True, dpi=pngDPI)
	if(not mode_parameters['showFigures']):
		plt.close(figure)

def colorsFromMap(mapName, colorStartPoint, colorEndPoint, numberOfColors):
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=mapName)
	return {'colors':[scalarColorMap.to_rgba(i) for i in np.linspace(colorStartPoint, colorEndPoint, numberOfColors)], 'smap':scalarColorMap}

def getTestLabel(deviceHistory, identifiers):
	label = str(identifiers['wafer']) + str(identifiers['chip']) + ':' + identifiers['device']
	if len(deviceHistory) > 0:
		test1Num = deviceHistory[0]['experimentNumber']
		test2Num = deviceHistory[-1]['experimentNumber']
		if test1Num == test2Num:
			label += ', Test {:}'.format(test1Num)
		else:
			label += ', Tests {:}-{:}'.format(test1Num, test2Num)
	return label



# === Plots === 
def plot(axis, x, y, lineColor, lineStyle=None, alpha=1):
	return axis.plot(x, y, color=lineColor, linestyle=lineStyle, alpha=alpha)[0]

def scatter(axis, x, y, lineColor, markerSize=3, lineWidth=0, lineStyle=None, alpha=1):
	return axis.plot(x, y, color=lineColor, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=lineWidth, linestyle=lineStyle, alpha=alpha)[0]

def plotWithErrorBars(axis, x, y, lineColor, errorBars=True, alpha=1):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	if(not errorBars):
		std = None
	return axis.errorbar(x_unique, avg, yerr=std, color=lineColor, capsize=2, capthick=0.5, elinewidth=0.5, alpha=alpha)[0]

def plotOverTime(axis, timestamps, y, lineColor, offset=0, markerSize=1, lineWidth=1, lineStyle=None, plotInnerGradient=False):
	zeroed_timestamps = list( np.array(timestamps) - timestamps[0] + offset )
	if(not plotInnerGradient):
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



# === Labels ===
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



# === Legend ===
def getLegendTitle(deviceHistory, plotType, parameterSuperType, parameterType, includeVdsRange, includeSubthresholdSwing=False):
	legend_title = ''
	legend_entries = []
	if(includeVdsRange):
		vds_list = getParameterArray(deviceHistory, parameterSuperType, parameterType, 'drainVoltageSetPoint')
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



# === Curve Fitting ===
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



# === Metrics ===
def avgSubthresholdSwing(vgs_data, id_data):
	return (abs( vgs_data[0] - vgs_data[-1] / (np.log10(np.abs(id_data[0])) - np.log10(np.abs(id_data[-1]))) ) * 1000)



# === Statistics ===
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



# === Data Manipulation ===
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

def getParameterArray(deviceHistory, parameterSuperType, parameterSubType, parameterName):
	result = []
	for i in range(len(deviceHistory)):
		element = deviceHistory[i]
		if(parameterSuperType != ''):
			element = element[parameterSuperType]
		if(parameterSubType != ''):
			element = element[parameterSubType]
		result.append(element[parameterName])
	return result



