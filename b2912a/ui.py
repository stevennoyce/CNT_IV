import io
import os
import sys
import glob
import flask
import json
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

@app.route('/plots/<wafer>/<chip>/<device>/<experiment>/<plotType>')
def sendPlot(wafer, chip, device, experiment, plotType):
	experiment = int(experiment)
	filebuf = io.BytesIO()
	DH.makePlots('..', 'data0', wafer, chip, device, plotSaveName=filebuf, startExperimentNumber=experiment, endExperimentNumber=experiment, specificPlot=plotType, saveFigures=True, showFigures=False)
	# plt.savefig(mode_parameters['plotSaveName'], transparent=True, dpi=pngDPI, format='png')
	filebuf.seek(0)
	return flask.send_file(filebuf, attachment_filename='plot.png')

@app.route('/wafers.json')
def wafers():
	paths = glob.glob('data0/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	chipCounts = [len(glob.glob(p + '/*/')) for p in paths]
	
	indexFileLists = [glob.glob(p + '/**/index.json', recursive=True) for p in paths]
	
	indexObjectLists = [[dlu.loadJSONIndex(os.path.dirname(indexFile)) for indexFile in indexFileList] for indexFileList in indexFileLists]
	indexCounts = [sum([(i['index'] if 'index' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	experimentCounts = [sum([(i['experimentNumber'] if 'experimentNumber' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	
	wafers = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'chipCount': c, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, c, ic, ec in zip(names, paths, modificationTimes, sizes, chipCounts, indexCounts, experimentCounts)]
	
	return flask.jsonify(wafers)

@app.route('/<wafer>/chips.json')
def chips(wafer):
	paths = glob.glob('data0/' + wafer + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	subPathsList = [glob.glob(p + '/*/') for p in paths]
	deviceCounts = [len(subPaths) for subPaths in subPathsList]
	
	indexObjectLists = [[dlu.loadJSONIndex(p) for p in subPaths] for subPaths in subPathsList]
	indexCounts = [sum([(i['index'] if 'index' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	experimentCounts = [sum([(i['experimentNumber'] if 'experimentNumber' in i else 0) for i in indexObjectList]) for indexObjectList in indexObjectLists]
	
	print('Not yet', file=sys.stderr)
	chips = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'deviceCount': d, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, d, ic, ec in zip(names, paths, modificationTimes, sizes, deviceCounts, indexCounts, experimentCounts)]
	
	return flask.jsonify(chips)

@app.route('/<wafer>/<chip>/devices.json')
def devices(wafer, chip):
	paths = glob.glob('data0/' + wafer + '/' + chip + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	# modificationTimes = [os.path.getmtime(p) for p in paths]
	modificationTimes = [os.path.getmtime(p+'ParametersHistory.json') if os.path.exists(p+'ParametersHistory.json') else os.path.getmtime(p) for p in paths]
	# sizes = [os.path.getsize(p) for p in paths]
	sizes = [os.path.getsize(p+'ParametersHistory.json') if os.path.exists(p+'ParametersHistory.json') else os.path.getsize(p) for p in paths]
	indexObjects = [dlu.loadJSONIndex(p) for p in paths]
	print(indexObjects, file=sys.stderr)
	indexCounts = [i['index'] for i in indexObjects]
	experimentCounts = [i['experimentNumber'] for i in indexObjects]
	
	devices = [{'name': n, 'path': p, 'modificationTime': m, 'size': s, 'indexCount': ic, 'experimentCount': ec} for n, p, m, s, ic, ec in zip(names, paths, modificationTimes, sizes, indexCounts, experimentCounts)]
	
	return flask.jsonify(devices)

@app.route('/<wafer>/<chip>/<device>/experiments.json')
def experiments(wafer, chip, device):
	folder = 'data0/' + wafer + '/' + chip + '/' + device + '/'
	files = glob.glob(folder + '*.json')
	fileNames = [os.path.basename(f) for f in files]
	
	parameters = dlu.loadJSON(folder, 'ParametersHistory.json')
	
	for i in range(len(parameters)):
		possiblePlots = DH.getPossiblePlotNames(parameters[i])
		parameters[i]['possiblePlots'] = possiblePlots
	
	# experiments = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return flask.jsonify(parameters)
	
	# return flask.Response(json.dumps(parameters, allow_nan=False), mimetype='application/json')

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
