# === Imports ===
import os
import sys
import platform
import time

from utilities import DataLoggerUtility as dlu
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
	
	waferID = 'C134'
	chipID = 'X'
	deviceID = '7-8'
	
	waferID = 'C127'
	chipID = 'X'
	deviceID = '15-16'
else:
	waferID = 'C127'
	chipID = 'F'
	deviceID = '63-64'



default_additional_parameters = {
	'Identifiers': {
		'user':'stevenjay',
		'project':'BiasStress1',
		'wafer':waferID,
		'chip':chipID,
		'device':deviceID,
		'step':0
	}
}



# === Main ===
def main():
	# Get user's action selection
	choice = selectFromDictionary('Actions: ', runTypes, 'Choose an action (0,1,2,...): ')

	if(choice.isdigit()):
		choice = int(choice)

		additional_parameters = default_additional_parameters.copy()
		if(choice == 0):
			return
		else:
			additional_parameters['runType'] = runTypes[choice]

		# Allow user to confirm the parameters before continuing
		confirmation = str(selectFromDictionary('Parameters: ', additional_parameters, 'Do you want to run with defaults, plus these additional parameters? (y/n): '))
		if(confirmation != 'y'):
			return

		launcher.run(additional_parameters)

	else:
		# File must end in '.json'
		file = choice if(choice[-5:] == '.json') else (choice + '.json')
		schedule_index = 0

		print('Opening schedule file: ' + file)

		while( schedule_index < len(dlu.loadJSON(directory='', loadFileName=file)) ):
			print('Loading line #' + str(schedule_index+1) + ' in schedule file ' + file)
			parameter_list = dlu.loadJSON(directory='', loadFileName=file)

			print('Launching job #' + str(schedule_index+1) + ' of ' + str(len(parameter_list)) + ' in schedule file ' + file)
			print('Schedule contains ' + str(len(parameter_list) - schedule_index - 1) + ' other incomplete jobs.')
			additional_parameters = parameter_list[schedule_index].copy()
			launcher.run(additional_parameters)

			schedule_index += 1
		


# === User Interface ===
runTypes = {
	'text':'schedule file',
	0:'Quit',
	1:'GateSweep',
	2:'BurnOut',
	3:'AutoBurnOut',
	4:'StaticBias',
	5:'AutoGateSweep',
	6:'AutoStaticBias',
	7:'DeviceHistory',
	8:'ChipHistory'
}

# Present a dictionary of options to the user and get their choice.
def selectFromDictionary(titleString, dictionary, promptString):
	print(titleString)
	print_dict(dictionary, 0)
	return input(promptString)

# Print a nicely formatted dictionary.
def print_dict(dictionary, numtabs):
	keys = list(dictionary.keys())
	for i in range(len(keys)):
		if(isinstance(dictionary[keys[i]], dict)):
			print(" '" + str(keys[i])+ "': {")
			print_dict(dictionary[keys[i]], numtabs+1)
		else:
			print(numtabs*'\t'+'  ' + str(keys[i]) + ': ' + str(dictionary[keys[i]]))

def devicesInRange(startContact, endContact, skip=True):
	contactList = set(range(startContact,endContact))
	if(skip):
		omitList = set(range(4,64+1,4))
		contactList = list(contactList-omitList)
	return ['{0:}-{1:}'.format(c, c+1) for c in contactList]





if(__name__ == '__main__'):
    main()
