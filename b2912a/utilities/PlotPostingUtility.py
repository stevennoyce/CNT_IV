import base64
import requests

def postPlots(parameters):
	return
	if not parameters['postFigures']:
		return
	
	plotFileNames = parameters['figuresSaved']
	
	for plotFileName in plotFileNames:
		with open(plotFileName, "rb") as plotFile:
			encodedImage = base64.b64encode(plotFile.read())
		
		postURL = 'https://script.google.com/macros/s/AKfycbzflDpYVTV3NGAEEaC-hfyQTN94JhZbr75dEh_czd7XXN5mDA/exec'
		
		postData = {
			'chipID': chipID,
			'deviceID': deviceID,
			'experimentNumber': experimentNumber,
			'runType': runType,
			'encodedImage': encodedImage,
			'startIndex': 
			'stopIndex': 
			'imageName': 
		}
		
		response = requests.post(postURL, data = postData)
		
		print('Posting plot to web service...')
		print(response)
		print(response.text)
