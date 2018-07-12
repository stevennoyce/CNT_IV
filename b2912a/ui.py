import io
import flask
import webbrowser
from matplotlib import pyplot as plt

app = flask.Flask(__name__, static_url_path='', static_folder='ui')

@app.route('/')
def root():
	return flask.redirect('/ui/index.html')

@app.route('/ui/<path:path>')
def sendStatic(path):
	return flask.send_from_directory('ui', path)

@app.route('/plots/<wafer>/<chip>/<device>/<plotType>')
def sendPlot(wafer, chip, device, plotType):
	plt.plot([1,2,3,4,5],[2,1,3,4,6])
	filebuf = io.BytesIO()
	try:
		plt.savefig(filebuf, format='png')
		filebuf.seek(0)
		return flask.send_file(filebuf, attachment_filename='plot.png')
	finally:
		filebuf.close()

if __name__ == '__main__':
	url = 'http://127.0.0.1:5000/ui/index.html'
	webbrowser.open_new(url)
	app.run(debug=True)
