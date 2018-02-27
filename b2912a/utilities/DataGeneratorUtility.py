import numpy as np

def constValues(value, points):
	return (int(points)*[value])

def rampValues(start, end, points):
	return np.linspace(start, end, points).tolist()

def sweepValues(start, end, points):
	data = rampValues(start, end, points/2)
	return [data, list(reversed(data))]

def stepValues(start, end, increments, pointsPerRamp, pointsPerHold):
	if(increments == 0):
		return rampValues(start, end, pointsPerRamp)
		
	data = rampValues(start, end/increments, pointsPerRamp)
	data += constValues(end/increments, pointsPerHold)
	for i in range(1, increments):
		data += rampValues(i*end/increments, (i+1)*end/increments, pointsPerRamp)
		data += constValues((i+1)*end/increments, pointsPerHold)
	return data

def rampValuesWithDuplicates(start, end, points, duplicates):
	data = np.linspace(start, end, points/duplicates).tolist()
	return sorted(duplicates*data)

def sweepValuesWithDuplicates(start, end, points, duplicates):
	data = rampValuesWithDuplicates(start, end, points/2, duplicates)
	return [data, list(reversed(data))]