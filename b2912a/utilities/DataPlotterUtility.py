from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Constants **********

titles = {
	'GateSweep':'Subthreshold Sweep',
	'BurnOut':'Metallic CNT Burn Out',
	'ChipHistory':'Chip History'
}

color_maps = {
	'GateSweep':'hot',
	'BurnOut':'Greys'
}



# ********** API **********

def plotJSON(jsonData, lineColor):
	if(jsonData['runType'] == 'GateSweep'):
		fig, ax = plt.subplots(1,1,'GateSweep')
		plotGateSweep(ax, jsonData, lineColor)
	elif(jsonData['runType'] == 'BurnOut'):
		fig, (ax1, ax2) = plt.subplots(1,2,'BurnOut')
		plotBurnOut(ax1, ax2, jsonData, lineColor)
	else:
		raise NotImplementedError("Unable to determine plot type")

def plotFullGateSweepHistory(deviceHistory):
	fig, ax = subplots(1, 1, 'GateSweep')
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=color_maps['GateSweep'])
	colors = [scalarColorMap.to_rgba(i) for i in np.linspace(0.7, 0, len(deviceHistory))]
	for i in range(len(deviceHistory)):
		plotGateSweep(ax, deviceHistory[i], colors[i])	
	ax.annotate('Burning Away Metallic CNTs', xy=(0.3, 0.05), xycoords='axes fraction', fontsize=8, horizontalalignment='left', verticalalignment='bottom', rotation=270)
	ax.annotate('', xy=(0.29, 0.05), xytext=(0.29,0.38), xycoords='axes fraction', arrowprops=dict(arrowstyle='->'))
	ax.annotate('$V_{DS} = 0.5V$', xy=(0.05, 0.45), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='bottom')

def plotFullBurnOutHistory(deviceHistory):
	fig, (ax1, ax2) = subplots(1, 2, 'BurnOut')
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=color_maps['BurnOut'])
	colors = [scalarColorMap.to_rgba(i) for i in np.linspace(0.3, 1.0, len(deviceHistory))]
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, deviceHistory[i], colors[i])

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory):
	fig, ax = subplots(1,1,'ChipHistory')
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['onOffRatio'])
	scatterLinearXLinearY(ax, range(len(devices)), firstOnOffRatios, 'b', 'First Run', 6)
	scatterLinearXLinearY(ax, range(len(devices)), lastOnOffRatios, 'r', 'Most Recent Run', 4)
	ax.set_ylabel('On/Off Ratio, $log_{10}(I_{on}/I_{off})$ (Orders of Magnitude)')
	ax.set_xticklabels(devices)
	ax.set_xticks(range(len(devices)))
	ax.xaxis.set_tick_params(rotation=90)
	fig.tight_layout(rect=[0,0,1.0,0.95])
	

# ***** Figures *****

def subplots(rows, columns, type):
	fig, axes = plt.subplots(rows, columns, figsize = (8,6))
	fig.suptitle(titles[type])
	return fig, axes

def show():
	plt.show()


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


# ***** Plots *****

def plotGateSweep(axis, jsonData, lineColor):
	#scatterLinearXLogY(axis jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$I_{on}/I_{off}$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])), 3)
	errorBarsLinearXLogY(axis, jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$log_{10}(I_{on}/I_{off})$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])))
	axis.set_xlabel('Gate Voltage, $V_{gs}$ [V]')
	axis.set_ylabel('Drain Current, $I_D$ [A]')
	axis.legend(loc='lower left') #bbox_to_anchor=(1.25,0.5)
	#axis.tight_layout(rect=[0,0,0.8,0.95])

def plotBurnOut(axis1, axis2, jsonData, lineColor):
	plotLinearXLinearY(axis1, jsonData['voltage1s'], jsonData['current1s'], lineColor, '')
	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['thresholdProportion']
	axis1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, label='', linestyle='--', linewidth=1)
	axis1.set_xlabel('Drain Voltage, $V_{ds}$ [V]')
	axis1.set_ylabel('Drain Current, $I_d$ [A]')
	plt.tight_layout(rect=[0,0,0.95,0.95])

	plotTimeLinearY(axis2, jsonData['timestamps'], jsonData['current1s'], lineColor, '')	
	axis2.set_xlabel('Time, $t$ [sec]')
	axis2.set_ylabel('Drain Current, $I_d$ [A]')
	plt.tight_layout(rect=[0,0,0.95,0.95])

def plotLinearXLogY(axis, x, y, lineColor, lineLabel):
	axis.plot(x, y, color=lineColor, label=lineLabel)
	axis.set_yscale('log')

def errorBarsLinearXLogY(axis, x, y, lineColor, lineLabel):
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	axis.errorbar(x_unique, avg, yerr=std, color=lineColor, label=lineLabel, capsize=4, capthick=0.5, elinewidth=0.5,)
	axis.set_yscale('log')

def scatterLinearXLogY(axis, x, y, lineColor, lineLabel, markerSize):
	axis.plot(x, y, color=lineColor, label=lineLabel, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)
	axis.set_yscale('log')

def plotLinearXLinearY(axis, x, y, lineColor, lineLabel):
	axis.plot(x, y, color=lineColor, label=lineLabel)

def scatterLinearXLinearY(axis, x, y, lineColor, lineLabel, markerSize):
	axis.plot(x, y, color=lineColor, label=lineLabel, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)

def plotTimeLogY(axis, timestamps, y, lineColor, lineLabel):
	zeroed_timestamps = list(np.array(timestamps) - np.array(timestamps)[0])
	axis.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel)
	axis.set_yscale('log')

def plotTimeLinearY(axis, timestamps, y, lineColor, lineLabel):
	zeroed_timestamps = list(np.array(timestamps) - np.array(timestamps)[0])
	axis.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel)







