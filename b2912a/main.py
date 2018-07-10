import os
import sys
import platform

import launcher
import defaults

if __name__ == '__main__':
	os.chdir(sys.path[0])

if platform.node() == 'noyce-dell':
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'
	
	# waferID = 'Nick_18051551_TC'
	# chipID = 'W'
	# deviceID = '57-58'
elif platform.node() == 'Steven-Noyce-MacBook-Pro.local':
	waferID = 'C127'
	chipID = 'E'
	deviceID = '14-15'
	
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'
	# Experiments 3 to 4
	# Experiment 57 - 
	# Experiment 65 - 

	waferID = 'C127'
	chipID = 'E'
	deviceID = '15-16'
	# Experiment 6 to 6, many decay curves and subthreshold curves
	# Separate plot, index 11 to 12, one decay curve
	# Separate plot, index 13 to 21, four decay curves
	# Separate plot, index 17 to 18, decent subthreshold curve with error bars
	# Separate plot, experiments 3 to 18, decaying subthreshold curves
	# Separate plot, experiments 3 to 13, stable/slowly decreasing subthreshold and transfer and on/off curves
	
	# waferID = 'C127'
	# chipID = 'P'
	# deviceID = '1-2'
	# # Experiment 8 to 8
	
	waferID = 'C134'
	chipID = 'K'
	deviceID = '15-16'
	
	waferID = 'C134'
	chipID = 'X'
	deviceID = '7-8'
	
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'
	
	waferID = 'C134'
	chipID = 'X'
	deviceID = '7-8'
	
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'
else:
	waferID = 'C134'
	chipID = 'X'
	deviceID = '7-8'
	
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'

id_parameters = {
	'waferID':waferID,
	'chipID':chipID,
	'deviceID':deviceID
}

def main():
	parameters = defaults.get()

	parameters['waferID'] = id_parameters['waferID']
	parameters['chipID'] = id_parameters['chipID']
	parameters['deviceID'] = id_parameters['deviceID']

	launcher.run(parameters)


if(__name__ == '__main__'):
    main()
