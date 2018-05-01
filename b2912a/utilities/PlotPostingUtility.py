import base64
import requests
import glob

def postPlots(parameters):
	print('When entering postPlots(), parameters is:')
	print(parameters)
	
	if not parameters['postFigures']:
		return
	
	try:
		plotFileNames = glob.glob(parameters['plotsFolder'] + '*.png')
		
		for plotFileName in plotFileNames:
			with open(plotFileName, "rb") as plotFile:
				encodedImage = base64.b64encode(plotFile.read())
			
			postURL = 'https://script.google.com/macros/s/AKfycbzflDpYVTV3NGAEEaC-hfyQTN94JhZbr75dEh_czd7XXN5mDA/exec'
			
			postData = parameters
			postData['encodedImage'] = encodedImage
			postData['imageName'] = plotFileName.split('.')[0]
			
			print('Posting plot to web service...')
			response = requests.post(postURL, data = postData)
			# response = requests.post(postURL, json = postData)
			
			print('Server response is: ')
			print(response)
			print(response.text)
	
	except e:
		print('Failed to post plots')
		print(e)



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
