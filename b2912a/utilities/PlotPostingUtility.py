import os
import base64
import requests

def makeFolder(folderPath):
	if (not os.path.exists(folderPath)):
		os.makedirs(folderPath)

def postPlots(parameters):
	print('When entering postPlots(), parameters is:')
	print(parameters)
	
	makeFolder('CurrentPlots')
	
	# Exit function while in development so as not to cause errors
	return
	
	if not parameters['postFigures']:
		return
	
	plotFileNames = parameters['figuresSaved']
	
	for plotFileName in plotFileNames:
		with open(plotFileName, "rb") as plotFile:
			encodedImage = base64.b64encode(plotFile.read())
		
		postURL = 'https://script.google.com/macros/s/AKfycbzflDpYVTV3NGAEEaC-hfyQTN94JhZbr75dEh_czd7XXN5mDA/exec'
		
		postData = {
			'chipID': parameters['chipID'],
			'deviceID': parameters['deviceID'],
			#'experimentNumber': ,
			'runType': parameters['runType'],
			'encodedImage': encodedImage,
			#'startIndex': ,
			#'stopIndex': ,
			'imageName': plotFileName.split('.')[0]
		}
		
		response = requests.post(postURL, data = postData)
		
		print('Posting plot to web service...')
		print(response)
		print(response.text)



if __name__ == '__main__':
	parameters = {
		'chipID': 'C127Fake',
		'deviceID': '8-9',
		'experimentNumber': 4,
		'runType': 'AutoGateSweep',
		'figuresSaved': ['../fig1.png'],
		'postFigures': True
	}
	
	postPlots(parameters)
	
	print('Complete')
