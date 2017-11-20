from matplotlib import pyplot as plt
import numpy as np

# ********** Constants **********

figures = {
	'GateSweep':1,
	'BurnOut':2,
	'ChipHistory':3
}

titles = {
	'GateSweep':'Gate Sweep',
	'BurnOut':'Burn Out',
	'ChipHistory':'Chip History'
}



# ********** API **********

def plotJSON(jsonData, lineColor):
	figure(jsonData['runType'])
	if(jsonData['runType'] == 'GateSweep'):
		plotGateSweep(jsonData, lineColor)
	elif(jsonData['runType'] == 'BurnOut'):
		plotBurnOut(jsonData, lineColor)
	else:
		raise NotImplementedError("Unable to determine plot type")

def plotFullDeviceHistory(deviceHistory):
	for i in range(len(deviceHistory)):
		plotJSON(deviceHistory[i], rgbFade(i, len(deviceHistory)))

def plotChipOnOffRatios(firstRunChipHistory, recentRunChipHistory):
	figure('ChipHistory')
	devices = []
	firstOnOffRatios = []
	for deviceRun in firstRunChipHistory:
		devices.append(deviceRun['deviceID']) 
		firstOnOffRatios.append(np.log10(deviceRun['onOffRatio']))
	lastOnOffRatios = len(devices)*[0]
	for deviceRun in recentRunChipHistory:
		lastOnOffRatios[devices.index(deviceRun['deviceID'])] = np.log10(deviceRun['onOffRatio'])
	scatterLinearXLinearY(range(len(devices)), firstOnOffRatios, 'b', 'First Run', 6)
	scatterLinearXLinearY(range(len(devices)), lastOnOffRatios, 'r', 'Most Recent Run', 4)
	plt.ylabel('On/Off Ratio, $log_{10}(I_{on}/I_{off})$ (Orders of Magnitude)')
	plt.xticks(range(len(devices)), devices, rotation='vertical')
	plt.tight_layout(rect=[0,0,0.8,0.95])
	

# ***** Figures *****

def figure(type):
	fig = plt.figure(figures[type], figsize = (10,6))
	fig.suptitle(titles[type])
	return fig

def show():
	plt.legend(loc='center right', bbox_to_anchor=(1.25,0.5))
	plt.show()

def rgbFade(i, numberOfLines):
	r = 0.9 - 0.9*((i+1)/(numberOfLines))**2
	g = 0.9 - 0.9*((i+1)/(numberOfLines))**2
	b = 0.9 - 0.9*((i+1)/(numberOfLines))**2
	return (r,g,b)

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

def plotGateSweep(jsonData, lineColor):
	scatterLinearXLogY(jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$I_{on}/I_{off}$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])), 3)
	#errorBarsLinearXLogY(jsonData['gateVoltages'], abs(np.array(jsonData['current1s'])), lineColor, '$I_{on}/I_{off}$'+': {:.1f}'.format(np.log10(jsonData['onOffRatio'])))
	plt.xlabel('Gate Voltage, $V_{gs}$ [V]')
	plt.ylabel('Drain Current, $I_D$ [A]')
	plt.tight_layout(rect=[0,0,0.8,0.95])

def plotBurnOut(jsonData, lineColor):
	ax1 = plt.subplot(1,2,1)
	plotLinearXLinearY(jsonData['voltage1s'], jsonData['current1s'], lineColor, '')
	currentThreshold = np.percentile(np.array(jsonData['current1s']), 90) * jsonData['thresholdProportion']
	ax1.plot([0, jsonData['voltage1s'][-1]], [currentThreshold, currentThreshold], color=lineColor, label='', linestyle='--', linewidth=1)
	ax1.set_xlabel('Drain Voltage, $V_{ds}$ [V]')
	ax1.set_ylabel('Drain Current, $I_d$ [A]')

	ax2 = plt.subplot(1,2,2)
	plotTimeLinearY(jsonData['timestamps'], jsonData['current1s'], lineColor, '')	
	ax2.set_xlabel('Time, $t$ [sec]')
	ax2.set_ylabel('Drain Current, $I_d$ [A]')

def plotLinearXLogY(x, y, lineColor, lineLabel):
	ax = plt.gca()
	ax.plot(x, y, color=lineColor, label=lineLabel)
	ax.set_yscale('log')

def errorBarsLinearXLogY(x, y, lineColor, lineLabel):
	ax = plt.gca()
	x_unique, avg, std = avgAndStdAtEveryPoint(x, y)
	ax.errorbar(x_unique, avg, yerr=std, color=lineColor, label=lineLabel, capsize=2, capthick=1)
	ax.set_yscale('log')

def scatterLinearXLogY(x, y, lineColor, lineLabel, markerSize):
	ax = plt.gca()
	ax.plot(x, y, color=lineColor, label=lineLabel, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)
	ax.set_yscale('log')

def plotLinearXLinearY(x, y, lineColor, lineLabel):
	ax = plt.gca()
	ax.plot(x, y, color=lineColor, label=lineLabel)

def scatterLinearXLinearY(x, y, lineColor, lineLabel, markerSize):
	ax = plt.gca()
	ax.plot(x, y, color=lineColor, label=lineLabel, marker='o', markersize=markerSize, markeredgecolor='none', linewidth=0)

def plotTimeLogY(timestamps, y, lineColor, lineLabel):
	zeroed_timestamps = list(np.array(timestamps) - np.array(timestamps)[0])
	ax = plt.gca()
	ax.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel)
	ax.set_yscale('log')

def plotTimeLinearY(timestamps, y, lineColor, lineLabel):
	zeroed_timestamps = list(np.array(timestamps) - np.array(timestamps)[0])
	ax = plt.gca()
	ax.plot(zeroed_timestamps, y, color=lineColor, label=lineLabel)







