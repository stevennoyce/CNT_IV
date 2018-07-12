import io
import os
import sys
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
	# plt.plot([1,2,3,4,5],[2,1,3,4,6])
	experiment = int(experiment)
	filebuf = io.BytesIO()
	try:
		DH.makePlots(defaults.get(), wafer, chip, device, fileName=filebuf, startExperimentNumber=experiment, endExperimentNumber=experiment, specificPlot=plotType, save=True, showFigures=False)
		# plt.savefig(filebuf, format='png')
		
		import shutil

		filebuf.seek(0)
		with open('myfile.png', 'wb') as f:
			shutil.copyfileobj(filebuf, f, length=131072)
		
		
		filebuf.seek(0)
		return flask.send_file(filebuf, attachment_filename='plot.png')
	finally:
		filebuf.close()

if __name__ == '__main__':
	# DH.makePlots(defaults.get(), 'C127', 'X', '15-16',  startExperimentNumber=1, endExperimentNumber=5, specificPlot='FullSubthresholdCurveHistory', save=False)
	# DH.makePlots(defaults.get(), 'C127', 'X', '15-16', 3, 3, 'FullSubthresholdCurveHistory', (2.2,2.2), '', 'Figure 2a - ', False, mode_parameters={'publication_mode':True})
	
	url = 'http://127.0.0.1:5000/ui/index.html'
	webbrowser.open_new(url)
	app.run(debug=True)
