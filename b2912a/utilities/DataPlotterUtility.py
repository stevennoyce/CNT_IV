from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Matplotlib Parameters **********

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial'
plt.rcParams['mathtext.bf'] = 'Arial:bold'
# plt.rcParams['figure.figsize'] = [4.2,4.9] # Thin size for subthreshold curves
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 9.5
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['axes.axisbelow'] = False
# plt.rcParams['figure.autolayout'] = True
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1

# ********** Constants **********

titles = {
	'GateSweep':'',
	'BurnOut':'Metallic CNT Burnout for ',
	'StaticBias':'Static Bias for ',
	'OnCurrent':'On/Off Current History for ',
	'ChipHistory':'Chip History for '
}

color_maps = {
	'GateSweep':'hot',
	'BurnOut':'Blues',
	'StaticBias':'plasma'
}



# ********** API **********

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

def plotJSON(jsonData, parameters, lineColor):
	titleNumbers = ', Test {:}'.format(jsonData['experimentNumber'])
	if(jsonData['runType'] == 'GateSweep'):
		fig, ax = initFigure(1, 1, 'GateSweep', jsonData['chipID'], jsonData['deviceID'], titleNumbers)
		plotGateSweep(ax, jsonData, lineColor)
	elif(jsonData['runType'] == 'BurnOut'):
		fig, (ax1, ax2) = initFigure(1, 2, 'BurnOut', jsonData['chipID'], jsonData['deviceID'], titleNumbers)
		ax2 = plt.subplot(2,2,2)
		ax3 = plt.subplot(2,2,4)
		plotBurnOut(ax1, ax2, ax3, jsonData, lineColor)
	elif(jsonData['runType'] == 'StaticBias'):
		fig, ax = initFigure(1, 1, 'StaticBias', jsonData['chipID'], jsonData['deviceID'], titleNumbers)
		plotStaticBias(ax, jsonData, lineColor, 0)
	else:
		raise NotImplementedError("Error: Unable to determine plot type")
	adjustFigure(fig, jsonData['runType'], parameters, saveFigure=False, showFigure=True)

def plotFullGateSweepHistory(deviceHistory, parameters, saveFigure=False, showFigure=True):
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax = initFigure(1, 1, 'GateSweep', parameters['chipID'], parameters['deviceID'], titleNumbers)
	fig.set_size_inches(4.2,4.9)
	colors = colorsFromMap(color_maps['GateSweep'], 0.7, 0, len(deviceHistory))
	indicesToLabel = np.linspace(0, len(deviceHistory)-1, 8).astype(int)
	for i in range(len(deviceHistory)):
		includeLegend = True if(len(deviceHistory) <= 8 or (i in indicesToLabel)) else False
		plotGateSweep(ax, deviceHistory[i], colors[i], includeLegend)	
	ax.annotate('Oldest to newest', xy=(0.3, 0.04), xycoords='axes fraction', fontsize=8, horizontalalignment='left', verticalalignment='bottom', rotation=270)
	ax.annotate('', xy=(0.29, 0.02), xytext=(0.29,0.3), xycoords='axes fraction', arrowprops=dict(arrowstyle='->'))
	ax.annotate('$V_{ds} = 0.5V$', xy=(0.05, 0.45), xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom')
	adjustFigure(fig, 'FullGateSweep', parameters, saveFigure, showFigure)

def plotFullBurnOutHistory(deviceHistory, parameters, saveFigure=False, showFigure=True):
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, (ax1, ax2) = initFigure(1, 2, 'BurnOut', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax2 = plt.subplot(2,2,2)
	ax3 = plt.subplot(2,2,4)
	colors = colorsFromMap(color_maps['BurnOut'], 0.6, 1.0, len(deviceHistory))
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i])
	ax1.annotate('$V_{gs} = $', xy=(0.96, 0.05), xycoords='axes fraction', horizontalalignment='right', verticalalignment='bottom')
	adjustFigure(fig, 'FullBurnOut', parameters, saveFigure, showFigure)

def plotFullStaticBiasHistory(deviceHistory, parameters, timescale, saveFigure=False, showFigure=True):
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax = initFigure(1, 1, 'StaticBias', parameters['chipID'], parameters['deviceID'], titleNumbers)
	colors = colorsFromMap(color_maps['StaticBias'], 0, 0.9, len(deviceHistory))
	deviceHistory = scaledData(deviceHistory, 'timestamps', 1/secondsPer(timescale))
	dotted_lines = []
	parameter_labels = {}
	for i in range(len(deviceHistory)):
		time_offset = (deviceHistory[i]['timestamps'][0] - deviceHistory[0]['timestamps'][0])
		plotStaticBias(ax, deviceHistory[i], colors[i], time_offset, timescale)

		# Compare current plot's parameters to the next ones, and save any differences
		if((i == 0) or (deviceHistory[i]['StaticBias'] != deviceHistory[i-1]['StaticBias'])):
			dotted_lines.append({'x':time_offset})
			for key in set(deviceHistory[i]['StaticBias'].keys()).intersection(deviceHistory[i-1]['StaticBias'].keys()):
				if((i == 0) or deviceHistory[i]['StaticBias'][key] != deviceHistory[i-1]['StaticBias'][key]):
					if(key not in parameter_labels):
						parameter_labels[key] = []
					parameter_labels[key].append({'x':time_offset, key:deviceHistory[i]['StaticBias'][key]})
		
	# Draw dotted lines between ANY plots that have different parameters
	for i in range(len(dotted_lines)):
		ax.annotate('', xy=(dotted_lines[i]['x'], ax.get_ylim()[0]), xytext=(dotted_lines[i]['x'], ax.get_ylim()[1]), xycoords='data', arrowprops=dict(arrowstyle='-', color=(0,0,0,0.3), ls=':', lw=1))
	
	# Add V_ds annotation
	for i in range(len(parameter_labels['drainVoltageSetPoint'])):
		ax.annotate(' $V_{ds} = $'+'{:.2f}V'.format(parameter_labels['drainVoltageSetPoint'][i]['drainVoltageSetPoint']), xy=(parameter_labels['drainVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.96 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')
	# Add V_gs annotation
	for i in range(len(parameter_labels['gateVoltageSetPoint'])):
		ax.annotate(' $V_{gs} = $'+'{:.1f}V'.format(parameter_labels['gateVoltageSetPoint'][i]['gateVoltageSetPoint']), xy=(parameter_labels['gateVoltageSetPoint'][i]['x'], ax.get_ylim()[1]*(0.94 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')

	# Add Grounding annotation
	# for i in range(len(parameter_labels['groundDrainWhenDone'])):
	# 	ax.annotate(' Grounded Drain: {:}'.format(parameter_labels['groundDrainWhenDone'][i]['groundDrainWhenDone']), xy=(parameter_labels['groundDrainWhenDone'][i]['x'], ax.get_ylim()[1]*(0.94 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')
	# for i in range(len(parameter_labels['groundGateWhenDone'])):
	# 	ax.annotate(' Grounded Gate: {:}'.format(parameter_labels['groundGateWhenDone'][i]['groundGateWhenDone']), xy=(parameter_labels['groundGateWhenDone'][i]['x'], ax.get_ylim()[1]*(0.92 - 0.03*i)), xycoords='data', fontsize=9, ha='left', va='bottom')

	adjustFigure(fig, 'FullStaticBias', parameters, saveFigure, showFigure)

def plotOnAndOffCurrentHistory(deviceHistory, parameters, saveFigure=False, showFigure=True):
	titleNumbers = getTitleTestNumbersLabel(deviceHistory)
	fig, ax1 = initFigure(1, 1, 'OnCurrent', parameters['chipID'], parameters['deviceID'], titleNumbers)
	ax2 = ax1.twinx()
	onCurrents = []
	offCurrents = []
	for deviceRun in deviceHistory:
		onCurrents.append(deviceRun['onCurrent'])
		offCurrents.append(deviceRun['offCurrent'])

	line = scatter(ax1, range(len(onCurrents)), onCurrents, 'r', 6)
	setLabel(line, 'On Currents')
	axisLabels(ax1, 'Time Index of Gate Sweep [#]', 'On Current, $(I_{on})$ [A]')
	ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

	line = scatter(ax2, range(len(offCurrents)), offCurrents, 'b', 2)
	setLabel(line, 'Off Currents')
	ax2.set_ylabel('Off Current, $(I_{off})$ [A]')
	ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	
	lines1, labels1 = ax1.get_legend_handles_labels()
	lines2, labels2 = ax2.get_legend_handles_labels()
	ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=8)

	adjustFigure(fig, 'OnAndOffCurrents', parameters, saveFigure, showFigure)

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory, parameters):
	fig, ax = initFigure(1, 1, 'ChipHistory', parameters['chipID'], parameters['deviceID'], '')
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['onOffRatio'])

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	line = scatter(ax, range(len(devices)), firstOnOffRatios, 'b', 6)
	setLabel(line, 'First Run')
	line = scatter(ax, range(len(devices)), lastOnOffRatios, 'r', 4)
	setLabel(line, 'Most Recent Run')
	axisLabels(ax, x_label='Device', y_label='On/Off Ratio, $log_{10}(I_{on}/I_{off})$ (Orders of Magnitude)')
	tickLabels(ax, devices, rotation=90)
	
	ax.legend(loc='best', fontsize=8) #bbox_to_anchor=(1.25,0.5)
	adjustFigure(fig, 'ChipHistory', parameters, saveFigure=False, showFigure=True)

def show():
	plt.show()



# ***** Device Plots *****

def plotGateSweep(axis, jsonData, lineColor, includeLabel=True):
	#scatter(axis, jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$I_{on}/I_{off}$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])), 3)
	line = plotWithErrorBars(axis, [(data) for sublist in jsonData['gateVoltages'] for data in sublist], abs(np.array([(data) for sublist in jsonData['current1s'] for data in sublist])), lineColor)
	semiLogScale(axis)
	axisLabels(axis, x_label='Gate Voltage, $V_{gs}$ [V]', y_label='Drain Current, $I_D$ [A]')
	if(includeLabel): 
		setLabel(line, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])))
		#setLabel(line, 'max $|I_{g}|$'+': {:.2e}'.format(max(abs(np.array(jsonData['current2s'])))))
		axis.legend(loc='lower left', fontsize=8) #bbox_to_anchor=(1.25,0.5)

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor):
	plot(axis1, jsonData['voltage1s'], (np.array(jsonData['current1s'])*10**6), lineColor)
	axisLabels(axis1, x_label='Drain-to-Source Voltage, $V_{ds}$ [V]', y_label='Drain Current, $I_D$ [$\mu$A]')

	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['BurnOut']['thresholdProportion'] * 10**6
	axis1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, linestyle='--', linewidth=1)
	axis1.annotate('burn current', xy=(0, currentThreshold), xycoords='data', fontsize=8, horizontalalignment='left', verticalalignment='bottom', color=lineColor)
	
	plotOverTime(axis2, jsonData['timestamps'], (np.array(jsonData['current1s'])*10**6), lineColor)	
	axisLabels(axis2, x_label='Time, $t$ [sec]', y_label='Drain Current, $I_D$ [$\mu$A]')

	plotOverTime(axis3, jsonData['timestamps'], jsonData['voltage1s'], lineColor)
	axisLabels(axis3, x_label='Time, $t$ [sec]', y_label='Drain-to-Source Voltage, $V_{ds}$ [V]')

def plotStaticBias(axis, jsonData, lineColor, timeOffset, timescale='seconds'):
	currents = (np.array(jsonData['current1s'])*(10**6))
	plotOverTime(axis, jsonData['timestamps'], currents, lineColor, timeOffset)	
	axisLabels(axis, x_label='Time, $t$ [{:}]'.format(timescale), y_label='Drain Current, $I_D$ [$\mu$A]')

	## Measuring how quickly the current decays from its start to final value
	#decay_threshold = np.exp(-1)*(currents[0] - currents[-1]) + currents[-1]
	#axis.plot([0, timestamps[-1] - timestamps[0]], [decay_threshold, decay_threshold], color=lineColor, linestyle='--', linewidth=1)
	#axis.plot([15, 15], [8, decay_threshold], color='r', linestyle='--', linewidth=1)


# ***** Figures *****

def initFigure(rows, columns, type, chipID, deviceID, testLabel):
	fig, axes = plt.subplots(rows, columns)
	title = titles[type] + chipID + ':' + deviceID + testLabel
	fig.suptitle(title)
	return fig, axes

def adjustFigure(figure, saveName, parameters, saveFigure, showFigure):
	figure.tight_layout(rect=[0,0,0.95,0.95])
	if(saveFigure):
		plt.savefig(parameters['plotsFolder'] + saveName + '.png')
	if(not showFigure):
		plt.close(figure)

def colorsFromMap(mapName, colorStartPoint, colorEndPoint, numberOfColors):
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=mapName)
	return [scalarColorMap.to_rgba(i) for i in np.linspace(colorStartPoint, colorEndPoint, numberOfColors)]

def scaledData(deviceHistory, dataToScale, scalefactor):
	data = list(deviceHistory)
	for i in range(len(data)):
		data[i][dataToScale] = list(np.array(data[i][dataToScale])*scalefactor)
	return data



# ***** Plots ***** 

def plot(axis, x, y, lineColor):
	return axis.plot(x, y, color=lineColor)[0]

def scatter(axis, x, y, lineColor, markerSize):
	return axis.plot(x, y, color=lineColor, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)[0]

def plotWithErrorBars(axis, x, y, lineColor):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	return axis.errorbar(x_unique, avg, yerr=std, color=lineColor, capsize=4, capthick=0.5, elinewidth=0.5)[0]

def plotOverTime(axis, timestamps, y, lineColor, offset=0):
	zeroed_timestamps = list( np.array(timestamps) - timestamps[0] + offset )
	return axis.plot(zeroed_timestamps, y, color=lineColor, marker='o', markersize = 1, linewidth=1)[0]



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



# ***** Math *****

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







