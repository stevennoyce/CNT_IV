from utilities import DataLoggerUtility as dlu
from utilities import DataPlotterUtility as dpu
import defaults

# Chip Specifier
waferID = 'C139'
chipID = 'D'
deviceID = '1'

# Model Fit Specifier for Data Range
Transconductance_Lower_Bound = 0
Transconductance_Upper_Bound = 18

# Read data from file
allData = dlu.loadJSON('data/' + waferID + '/' + chipID + '/' + deviceID + '/', 'GateSweep.json')

# Graph and calculate transconductance and threshold voltage
output = ['gm, VT\n']
for run_num in range(0, len(allData)):
	jsonData = allData[run_num]
	parameters = dict(defaults.default_parameters)
	id_data = jsonData['Results']['id_data'][0]
	vgs_data = jsonData['Results']['vgs_data'][0]
	fit = dpu.linearFit(vgs_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound], id_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound]);
	VT = fit['intercept'] / fit['slope']
	output.append(str(fit['slope']) + ', ' + str(VT) + "\n")
	fig, axes = dpu.initFigure(parameters, 1, 1, 'TransferCurve', 'Transfer Curve, Run ' + str(run_num))
	dpu.axisLabels(axes, "$V_{GS}$ (V)", "$I_{D}$ (A)")
	data_line = dpu.scatter(axes, vgs_data, id_data, '#00009c', lineWidth=1)
	dpu.setLabel(data_line, ' $I_{D}$ Data')
	fit_line = dpu.scatter(axes, vgs_data[Transconductance_Lower_Bound:Transconductance_Upper_Bound], fit['fitted_data'], '#ffa500', lineWidth=1)
	dpu.setLabel(fit_line, ' Model')
	axes.legend(loc='best', borderpad=0.15, labelspacing=0.3, handlelength=0.2, handletextpad=0.1)
	saveName = waferID + "_" + chipID + "_" + deviceID + "_Run" + str(run_num) + "_Transfer_Curve"
	dpu.adjustFigure(fig, saveName, parameters, saveFigure=True, showFigure=False)

# Output data as CSV file
file = open("CurrentPlots/" + waferID + "_" + chipID + "_" + deviceID + "_Transconductance_Threshold.csv", "w+")
file.writelines(output)
file.close()


