from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Constants **********

titles = {
	'GateSweep':'Subthreshold Sweep',
	'BurnOut':'Metallic CNT Burnout',
	'OnCurrent':'Device On/Off Current History',
	'ChipHistory':'Chip History'
}

color_maps = {
	'GateSweep':'hot',
	'BurnOut':'Blues'
}



# ********** API **********

def plotJSON(jsonData, lineColor):
	if(jsonData['runType'] == 'GateSweep'):
		fig, ax = initFigure(1,1,'GateSweep')
		plotGateSweep(ax, jsonData, lineColor)
	elif(jsonData['runType'] == 'BurnOut'):
		fig, (ax1, ax2) = initFigure(1,2,'BurnOut')
		ax2 = plt.subplot(2,2,2)
		ax3 = plt.subplot(2,2,4)
		plotBurnOut(ax1, ax2, ax3, jsonData, lineColor)
	else:
		raise NotImplementedError("Error: Unable to determine plot type")
	adjustFigure(fig, saveFigure=False, showFigure=True)

def plotFullGateSweepHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, ax = initFigure(1, 1, 'GateSweep')
	colors = colorsFromMap(color_maps['GateSweep'], 0.7, 0, len(deviceHistory))
	for i in range(len(deviceHistory)):
		plotGateSweep(ax, deviceHistory[i], colors[i])	
	ax.annotate('Oldest to newest', xy=(0.3, 0.01*len(deviceHistory)), xycoords='axes fraction', fontsize=8, horizontalalignment='left', verticalalignment='bottom', rotation=270)
	ax.annotate('', xy=(0.29, 0.04), xytext=(0.29,0.0475*len(deviceHistory)), xycoords='axes fraction', arrowprops=dict(arrowstyle='->'))
	ax.annotate('$V_{DS} = $', xy=(0.05, 0.45), xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom')
	adjustFigure(fig, saveFigure, showFigure)

def plotFullBurnOutHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, (ax1, ax2) = initFigure(1, 2, 'BurnOut')
	ax2 = plt.subplot(2,2,2)
	ax3 = plt.subplot(2,2,4)
	colors = colorsFromMap(color_maps['BurnOut'], 0.6, 1.0, len(deviceHistory))
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i])
	ax1.annotate('$V_{GS} = 15V$', xy=(0.96, 0.05), xycoords='axes fraction', horizontalalignment='right', verticalalignment='bottom')
	adjustFigure(fig, saveFigure, showFigure)

def plotOnCurrentHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, ax1 = initFigure(1, 1, 'OnCurrent')
	ax2 = ax1.twinx()
	onCurrents = []
	offCurrents = []
	for deviceRun in deviceHistory:
		onCurrents.append(deviceRun['onCurrent'])
		offCurrents.append(deviceRun['offCurrent'])

	scatter(ax1, range(len(onCurrents)), onCurrents, 'r', 'On Currents', 6)
	axisLabels(ax1, 'Data From Subthreshold Sweeps Over Time', 'On Current, $(I_{on})$ [A]')
	ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

	scatter(ax2, range(len(offCurrents)), offCurrents, 'b', 'Off Currents', 2)
	ax2.set_ylabel('Off Current, $(I_{off})$ [A]')
	ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	
	lines1, labels1 = ax1.get_legend_handles_labels()
	lines2, labels2 = ax2.get_legend_handles_labels()
	ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=8)

	adjustFigure(fig, saveFigure, showFigure)

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory):
	fig, ax = initFigure(1,1,'ChipHistory')
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['onOffRatio'])

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	scatter(ax, range(len(devices)), firstOnOffRatios, 'b', 'First Run', 6)
	scatter(ax, range(len(devices)), lastOnOffRatios, 'r', 'Most Recent Run', 4)
	axisLabels(ax, x_label='Device', y_label='On/Off Ratio, $log_{10}(I_{on}/I_{off})$ (Orders of Magnitude)')
	tickLabels(ax, devices, rotation=90)
	
	ax.legend(loc='best', fontsize=8) #bbox_to_anchor=(1.25,0.5)
	adjustFigure(fig, saveFigure=False, showFigure=True)

def show():
	plt.show()



# ***** Device Plots *****

def plotGateSweep(axis, jsonData, lineColor):
	#scatter(axis jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$I_{on}/I_{off}$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])), 3)
	plotWithErrorBars(axis, jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])))
	semiLogScale(axis)
	axisLabels(axis, x_label='Gate Voltage, $V_{GS}$ [V]', y_label='Drain Current, $I_D$ [A]')
	axis.legend(loc='lower left', fontsize=8) #bbox_to_anchor=(1.25,0.5)

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor):
	plot(axis1, jsonData['voltage1s'], (np.array(jsonData['current1s'])*10**6), lineColor, '')
	axisLabels(axis1, x_label='Drain-to-Source Voltage, $V_{DS}$ [V]', y_label='Drain Current, $I_D$ [$\mu$A]')

	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['thresholdProportion'] * 10**6
	axis1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, linestyle='--', linewidth=1)
	axis1.annotate('burn current', xy=(0, currentThreshold), xycoords='data', fontsize=8, horizontalalignment='left', verticalalignment='bottom', color=lineColor)
	
	plotOverTime(axis2, jsonData['timestamps'], (np.array(jsonData['current1s'])*10**6), lineColor, '')	
	axisLabels(axis2, x_label='Time, $t$ [sec]', y_label='Drain Current, $I_D$ [$\mu$A]')

	plotOverTime(axis3, jsonData['timestamps'], jsonData['voltage1s'], lineColor, '')
	axisLabels(axis3, x_label='Time, $t$ [sec]', y_label='Drain-to-Source Voltage, $V_{DS}$ [V]')



# ***** Figures *****

def initFigure(rows, columns, type):
	fig, axes = plt.subplots(rows, columns)
	fig.suptitle(titles[type])
	return fig, axes

def adjustFigure(figure, saveFigure, showFigure):
	figure.tight_layout(rect=[0,0,0.95,0.95])
	if(saveFigure):
		plt.savefig('fig'+str(figure.number)+'.png')
	if(not showFigure):
		plt.close(figure)

def colorsFromMap(mapName, colorStartPoint, colorEndPoint, numberOfColors):
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=mapName)
	return [scalarColorMap.to_rgba(i) for i in np.linspace(colorStartPoint, colorEndPoint, numberOfColors)]



# ***** Plots ***** 

def plot(axis, x, y, lineColor, lineLabel):
	axis.plot(x, y, color=lineColor, label=lineLabel)

def scatter(axis, x, y, lineColor, lineLabel, markerSize):
	axis.plot(x, y, color=lineColor, label=lineLabel, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)

def plotWithErrorBars(axis, x, y, lineColor, lineLabel):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	axis.errorbar(x_unique, avg, yerr=std, color=lineColor, label=lineLabel, capsize=4, capthick=0.5, elinewidth=0.5,)

def plotOverTime(axis, timestamps, y, lineColor, lineLabel):
	zeroed_timestamps = list(np.array(timestamps) - np.array(timestamps)[0])
	axis.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel, marker='o', markersize = 1, linewidth=1)



# ***** Labels *****

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





