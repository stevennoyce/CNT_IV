import io
import os
import sys
import glob
import flask
import webbrowser
from matplotlib import pyplot as plt
import defaults
from control_scripts import Device_History as DH

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
	DH.makePlots(defaults.get(), wafer, chip, device, fileName=filebuf, startExperimentNumber=experiment, endExperimentNumber=experiment, specificPlot=plotType, save=True, showFigures=False)
	
	filebuf.seek(0)
	return flask.send_file(filebuf, attachment_filename='plot.png')

@app.route('/wafers.json')
def wafers():
	paths = glob.glob('data/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	wafers = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return flask.jsonify(wafers)

@app.route('/<wafer>/chips.json')
def chips(wafer):
	paths = glob.glob('data/' + wafer + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	chips = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return flask.jsonify(chips)

@app.route('/<wafer>/<chip>/devices.json')
def devices(wafer, chip):
	paths = glob.glob('data/' + wafer + '/' + chip + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	devices = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return flask.jsonify(devices)

@app.route('/<wafer>/<chip>/<device>/experiments.json')
def experiments(wafer, chip, device):
	paths = glob.glob('data/' + wafer + '/' + chip + '/' + device + '/*/')
	names = [os.path.basename(os.path.dirname(p)) for p in paths]
	modificationTimes = [os.path.getmtime(p) for p in paths]
	sizes = [os.path.getsize(p) for p in paths]
	
	experiments = [{'name': n, 'path': p, 'modificationTime': m, 'size': s} for n, p, m, s in zip(names, paths, modificationTimes, sizes)]
	
	return flask.jsonify(experiments)

if __name__ == '__main__':
	url = 'http://127.0.0.1:5000/ui/index.html'
	webbrowser.open_new(url)
	app.run(debug=True)
