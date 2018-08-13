import io
import os
import sys
import glob
import flask
import json
import copy
import webbrowser
from matplotlib import pyplot as plt
import defaults
from control_scripts import Device_History as DH
from utilities import DataLoggerUtility as dlu

if __name__ == '__main__':
	os.chdir(sys.path[0])

app = flask.Flask(__name__, static_url_path='', static_folder='ui')

@app.route('/')
def root():
	return flask.redirect('/ui/index.html')

@app.route('/ui/<path:path>')
def sendStatic(path):
	return flask.send_from_directory('ui', path)

default_makePlot_parameters = {
	'startExperimentNumber': None,
	'endExperimentNumber': None,
	'specificPlot': '',
	'figureSize': None,
	'dataFolder': None,
	'saveFolder': None,
	'plotSaveName': '',
	'saveFigures': False,
	'showFigures': True,
	'sweepDirection': 'both',
	'plotInRealTime': True,
	'startRelativeIndex': 0,
	'endRelativeIndex': 1e10,
	'plot_mode_parameters': None
}

@app.route('/plots/<user>/<project>/<wafer>/<chip>/<device>/<experiment>/<plotType>')
def sendPlot(user, project, wafer, chip, device, experiment, plotType):
	experiment = int(experiment)
	
	plotSettings = copy.deepcopy(default_makePlot_parameters)
	receivedPlotSettings = json.loads(flask.request.args.get('plotSettings'))
	plotSettings.update(receivedPlotSettings)
	
	filebuf = io.BytesIO()
	
	if plotSettings['startExperimentNumber'] == None:
		plotSettings['startExperimentNumber'] = experiment
	
	if plotSettings['endExperimentNumber'] == None:
		plotSettings['endExperimentNumber'] = experiment
	
	plotSettings['plotSaveName'] = filebuf
	plotSettings['saveFigures'] = True
	plotSettings['showFigures'] = False
	plotSettings['specificPlot'] = plotType
	
	DH.makePlots(user, project, wafer, chip, device, **plotSettings)
	# plt.savefig(mode_parameters['plotSaveName'], transparent=True, dpi=pngDPI, format='png')
	filebuf.seek(0)
	return flask.send_file(filebuf, attachment_filename='plot.png')

# @app.route('/defaultPlotSettings.json')
# def defaultPlotSettings():
# 	settings = 
# 	return json.dumps(settings)

@app.route('/users.json')
def users():
	paths = glob.glob('data/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	return json.dumps(names)

@app.route('/<user>/projects.json')
def projects(user):
	paths = glob.glob('data/' + user + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	
	projects = [{'name': n} for n in names]
	
	return json.dumps(projects)

@app.route('/<user>/<project>/indexes.json')
def indexes(user, project):
	indexObject = {}
	
	waferPaths = glob.glob('data/' + user + '/' + project + '/*/')
	waferNames = [os.path.basename(os.path.dirname(p)) for p in waferPaths]
	
	for waferPath, waferName in zip(waferPaths, waferNames):
		indexObject[waferName] = {}
		chipPaths = glob.glob(waferPath + '/*/')
		chipNames = [os.path.basename(os.path.dirname(p)) for p in chipPaths]
		
		for chipPath, chipName in zip(chipPaths, chipNames):
			indexObject[waferName][chipName] = {}
			devicePaths = glob.glob(chipPath + '/*/index.json')
			deviceNames = [os.path.basename(os.path.dirname(p)) for p in devicePaths]
			
			for devicePath, deviceName in zip(devicePaths, deviceNames):
				indexObject[waferName][chipName][deviceName] = dlu.loadJSONIndex(os.path.dirname(devicePath))
	
	return json.dumps(indexObject)

@app.route('/<user>/<project>/wafers.json')
def wafers(user, project):
	paths = glob.glob('data/' + user + '/' + project + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	chipCounts = [len(glob.glob(p + '/*/')) for p in paths]
	
	indexFileLists = [glob.glob(p + '/**/index.json', recursive=True) for p in paths]
	indexObjectLists = [[dlu.loadJSONIndex(os.path.dirname(indexFile)) for indexFile in indexFileList] for indexFileList in indexFileLists]
	indexCounts = [sum([(i['index'] if 'index' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	experimentCounts = [sum([(i['experimentNumber'] if 'experimentNumber' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	
	wafers = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'chipCount': c, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, c, ic, ec in zip(names, paths, modificationTimes, sizes, chipCounts, indexCounts, experimentCounts)]
	
	return json.dumps(wafers)

@app.route('/<user>/<project>/<wafer>/chips.json')
def chips(user, project, wafer):
	paths = glob.glob('data/' + user + '/' + project + '/' + wafer + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	subPathsList = [glob.glob(p + '/*/') for p in paths]
	deviceCounts = [len(subPaths) for subPaths in subPathsList]
	
	indexObjectLists = [[dlu.loadJSONIndex(p) for p in subPaths] for subPaths in subPathsList]
	indexCounts = [sum([(i['index'] if 'index' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	experimentCounts = [sum([(i['experimentNumber'] if 'experimentNumber' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	
	chips = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'deviceCount': d, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, d, ic, ec in zip(names, paths, modificationTimes, sizes, deviceCounts, indexCounts, experimentCounts)]
	
	return json.dumps(chips)

@app.route('/<user>/<project>/<wafer>/<chip>/devices.json')
def devices(user, project, wafer, chip):
	paths = glob.glob('data/' + user + '/' + project + '/' + wafer + '/' + chip + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	# modificationTimes = [os.path.getmtime(p) for p in paths]
	modificationTimes = [os.path.getmtime(p+'ParametersHistory.json') if os.path.exists(p+'ParametersHistory.json') else os.path.getmtime(p) for p in paths]
	# sizes = [os.path.getsize(p) for p in paths]
	sizes = [os.path.getsize(p+'ParametersHistory.json') if os.path.exists(p+'ParametersHistory.json') else os.path.getsize(p) for p in paths]
	
	indexObjects = [dlu.loadJSONIndex(p) for p in paths]
	indexCounts = [i['index'] for i in indexObjects]
	experimentCounts = [i['experimentNumber'] for i in indexObjects]
	
	devices = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, ic, ec in zip(names, paths, modificationTimes, sizes, indexCounts, experimentCounts)]
	
	return json.dumps(devices)

@app.route('/<user>/<project>/<wafer>/<chip>/<device>/experiments.json')
def experiments(user, project, wafer, chip, device):
	folder = 'data/' + user + '/' + project + '/' + wafer + '/' + chip + '/' + device + '/'
	files = glob.glob(folder + '*.json')
	fileNames = [os.path.basename(f) for f in files]
	
	parameters = dlu.loadJSON(folder, 'ParametersHistory.json')
	
	for i in range(len(parameters)):
		possiblePlots = DH.getPossiblePlotNames(parameters[i])
		parameters[i]['possiblePlots'] = possiblePlots
	
	# experiments = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return json.dumps(parameters)
	
	# return flask.Response(json.dumps(parameters, allow_nan=False), mimetype='application/json')

@app.route('/default_parameters_description.json')
def parametersDescription():
	# return flask.jsonify(defaults.default_parameters_description)
	return json.dumps(defaults.default_parameters_description)

@app.route('/default_parameters.json')
def defaultParameters():
	return json.dumps(defaults.default_parameters)

# @app.after_request
# def add_header(response):
# 	# response.cache_control.max_age = 300
#	# response.cache_control.no_store = True
#	# if 'Cache-Control' not in response.headers:
#		# response.headers['Cache-Control'] = 'no-store'
#	return response

if __name__ == '__main__':
	url = 'http://127.0.0.1:5000/ui/index.html'
	# webbrowser.open_new(url)
	app.run(debug=True, threaded=False)
