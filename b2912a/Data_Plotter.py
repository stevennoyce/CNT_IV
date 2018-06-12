from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu

jsondata = dlu.loadJSON('data/C139/D/1-2', 'GateSweep')
parameters = dict(jsondata)
parameters.pop('Results', None)
dpu.plotJSON(jsonData, parameters, 'b')
