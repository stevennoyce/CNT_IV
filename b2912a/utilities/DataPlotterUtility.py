from matplotlib import pyplot as plt
from matplotlib import colors as pltc
from matplotlib import cm
import numpy as np

# ********** Constants **********

titles = {
	'GateSweep':'Subthreshold Sweep',
	'BurnOut':'Metallic CNT Burnout',
	'OnCurrent':'Device On Current History',
	'ChipHistory':'Chip History'
}

color_maps = {
	'GateSweep':'hot',
	'BurnOut':'Blues'
}



# ********** API **********

def plotJSON(jsonData, lineColor):
	if(jsonData['runType'] == 'GateSweep'):
		fig, ax = subplots(1,1,'GateSweep')
		plotGateSweep(ax, jsonData, lineColor)
	elif(jsonData['runType'] == 'BurnOut'):
		fig, (ax1, ax2) = subplots(1,2,'BurnOut')
		ax2 = plt.subplot(2,2,2)
		ax3 = plt.subplot(2,2,4)
		plotBurnOut(ax1, ax2, ax3, jsonData, lineColor)
	else:
		raise NotImplementedError("Unable to determine plot type")

def plotFullGateSweepHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, ax = subplots(1, 1, 'GateSweep')
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=color_maps['GateSweep'])
	colors = [scalarColorMap.to_rgba(i) for i in np.linspace(0.7, 0, len(deviceHistory))]
	for i in range(len(deviceHistory)):
		plotGateSweep(ax, deviceHistory[i], colors[i])	
	ax.annotate('Oldest to newest', xy=(0.3, 0.01*len(deviceHistory)), xycoords='axes fraction', fontsize=8, horizontalalignment='left', verticalalignment='bottom', rotation=270)
	ax.annotate('', xy=(0.29, 0.04), xytext=(0.29,0.0475*len(deviceHistory)), xycoords='axes fraction', arrowprops=dict(arrowstyle='->'))
	ax.annotate('$V_{DS} = 0.5V$', xy=(0.05, 0.45), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='bottom')
	if(saveFigure):
		plt.savefig('fig1.png')
	if(not showFigure):
		plt.close(fig)

def plotFullBurnOutHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, (ax1, ax2) = subplots(1, 2, 'BurnOut')
	ax2 = plt.subplot(2,2,2)
	ax3 = plt.subplot(2,2,4)
	scalarColorMap = cm.ScalarMappable(norm=pltc.Normalize(vmin=0, vmax=1.0), cmap=color_maps['BurnOut'])
	colors = [scalarColorMap.to_rgba(i) for i in np.linspace(0.6, 1.0, len(deviceHistory))]
	for i in range(len(deviceHistory)):
		plotBurnOut(ax1, ax2, ax3, deviceHistory[i], colors[i])
	ax1.annotate('$V_{GS} = 15V$', xy=(0.96, 0.05), xycoords='axes fraction', fontsize=10, horizontalalignment='right', verticalalignment='bottom')
	if(saveFigure):
		plt.savefig('fig2.png')
	if(not showFigure):
		plt.close(fig)

def plotOnCurrentHistory(deviceHistory, saveFigure=False, showFigure=True):
	fig, ax = subplots(1, 1, 'OnCurrent')
	onCurrents = []
	for deviceRun in deviceHistory:
		onCurrents.append(deviceRun['onCurrent'])
	scatterLinearXLogY(ax, range(len(onCurrents)), onCurrents, 'b', 'On Currents', 6)
	ax.set_ylabel('On Current, $(I_{on})$ [A]')
	ax.set_xlabel('Data From Subthreshold Sweeps Over Time')
	fig.tight_layout(rect=[0,0,0.95,0.95])
	if(saveFigure):
		plt.savefig('fig3.png')
	if(not showFigure):
		plt.close(fig)

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

	lastOnOffRatios, devices, firstOnOffRatios = zip(*(reversed(sorted(zip(lastOnOffRatios, devices, firstOnOffRatios)))))

	scatterLinearXLinearY(ax, range(len(devices)), firstOnOffRatios, 'b', 'First Run', 6)
	scatterLinearXLinearY(ax, range(len(devices)), lastOnOffRatios, 'r', 'Most Recent Run', 4)
	ax.set_ylabel('On/Off Ratio, $log_{10}(I_{on}/I_{off})$ (Orders of Magnitude)')
	ax.set_xlabel('Device')
	ax.set_xticklabels(devices)
	ax.set_xticks(range(len(devices)))
	ax.xaxis.set_tick_params(rotation=90)
	ax.legend(loc='best', fontsize=8) #bbox_to_anchor=(1.25,0.5)
	fig.tight_layout(rect=[0,0,0.95,0.95])

# ***** Figures *****

def subplots(rows, columns, type):
	fig, axes = plt.subplots(rows, columns)
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
	axis.set_xlabel('Gate Voltage, $V_{GS}$ [V]')
	axis.set_ylabel('Drain Current, $I_D$ [A]')
	axis.legend(loc='lower left', fontsize=8) #bbox_to_anchor=(1.25,0.5)

	plt.tight_layout(rect=[0,0,0.95,0.95])

def plotBurnOut(axis1, axis2, axis3, jsonData, lineColor):
	plotLinearXLinearY(axis1, jsonData['voltage1s'], (np.array(jsonData['current1s'])*10**6), lineColor, '')
	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['thresholdProportion'] * 10**6
	axis1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, label='', linestyle='--', linewidth=1)
	axis1.annotate('burn current', xy=(0, currentThreshold), xycoords='data', fontsize=8, horizontalalignment='left', verticalalignment='bottom', color=lineColor)
	axis1.set_xlabel('Drain-to-Source Voltage, $V_{DS}$ [V]')
	axis1.set_ylabel('Drain Current, $I_D$ [$\mu$A]')

	plotTimeLinearY(axis2, jsonData['timestamps'], (np.array(jsonData['current1s'])*10**6), lineColor, '')	
	axis2.set_xlabel('Time, $t$ [sec]')
	axis2.set_ylabel('Drain Current, $I_D$ [$\mu$A]')

	plotTimeLinearY(axis3, jsonData['timestamps'], jsonData['voltage1s'], lineColor, '')
	axis3.set_xlabel('Time, $t$ [sec]')
	axis3.set_ylabel('Drain-to-Source Voltage, $V_{DS}$ [V]')

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
	axis.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel, marker='o', markersize = 1, linewidth=1)







